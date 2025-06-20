# Unit tests for authentication routes (rental_management_mvp/routes/auth_routes.py)

import unittest
from unittest.mock import patch, MagicMock, call

# Import route functions
from rental_management_mvp.routes.auth_routes import (
    register_user_email,
    login_user_email,
    reset_password_email,
    verify_otp,
    register_phone_request_otp,
    verify_phone_otp,
    login_user_phone,
    request_password_reset_email,
    request_password_reset_sms,
    reset_password_sms,
    logout_user # Added for Phase 12
)

class TestAuthRoutes(unittest.TestCase):

    def setUp(self):
        pass

    def test_register_user_email_password_complexity(self):
        """
        Test user registration with various password complexity outcomes.
        Route function: register_user_email(request_data)
        """
        with patch('rental_management_mvp.routes.auth_routes.PasswordValidator', create=True) as MockPasswordValidatorClass, \
             patch('rental_management_mvp.routes.auth_routes.UserService', create=True) as MockUserServiceClass, \
             patch('rental_management_mvp.routes.auth_routes.AuditLogger', create=True) as MockAuditLoggerClass:

            mock_is_password_complex = MockPasswordValidatorClass.is_password_complex_enough
            mock_create_user = MockUserServiceClass.create_user

            sample_request_data_fail = {
                "email": "testfail@example.com", "password": "short",
                "first_name": "Test", "last_name": "UserFail", "role": "TENANT"
            }
            password_errors = ["Password too short.", "Needs an uppercase letter."]
            mock_is_password_complex.return_value = (False, password_errors)

            response, status_code = register_user_email(sample_request_data_fail)

            mock_is_password_complex.assert_called_once_with(sample_request_data_fail["password"])
            mock_create_user.assert_not_called()
            MockAuditLoggerClass.log_event.assert_called_once_with(
                event_type="USER_REGISTRATION_ATTEMPT_FAILURE",
                details={
                    "email": sample_request_data_fail["email"],
                    "reason": "Password not complex", "errors": password_errors
                }
            )
            self.assertEqual(status_code, 400)
            self.assertEqual(response, {"message": "Password validation failed", "errors": password_errors})

            mock_is_password_complex.reset_mock()
            mock_create_user.reset_mock()
            MockAuditLoggerClass.log_event.reset_mock()

            sample_request_data_success = {
                "email": "testsuccess@example.com", "password": "ValidPassword123!",
                "first_name": "Test", "last_name": "UserSuccess", "role": "LANDLORD"
            }
            mock_user_instance = MagicMock(user_id=123)
            mock_is_password_complex.return_value = (True, [])
            mock_create_user.return_value = mock_user_instance

            response, status_code = register_user_email(sample_request_data_success)

            mock_is_password_complex.assert_called_once_with(sample_request_data_success["password"])
            mock_create_user.assert_called_once_with(
                email=sample_request_data_success["email"], password=sample_request_data_success["password"],
                full_name="Test UserSuccess", role=sample_request_data_success["role"]
            )
            MockAuditLoggerClass.log_event.assert_called_once_with(
                event_type="USER_CREATED",
                details={"user_id": 123, "email": sample_request_data_success["email"], "role": sample_request_data_success["role"]}
            )
            self.assertEqual(status_code, 201)
            self.assertEqual(response, {"message": "User registered successfully", "user_id": 123})

    def test_login_audit_logs(self):
        """
        Test audit logs for login success and failure scenarios.
        Route function: login_user_email(request_data)
        """
        with patch('rental_management_mvp.routes.auth_routes.UserService', create=True) as MockUserServiceClass, \
             patch('rental_management_mvp.routes.auth_routes.AuditLogger', create=True) as MockAuditLoggerClass:

            mock_authenticate_user = MockUserServiceClass.authenticate_user
            mock_log_event = MockAuditLoggerClass.log_event

            success_request_data = {"email": "user@example.com", "password": "password123"}
            mock_user_instance = MagicMock(user_id="user_xyz_123", is_mfa_enabled=False)
            mock_authenticate_user.return_value = mock_user_instance

            response, status_code = login_user_email(success_request_data)

            mock_authenticate_user.assert_called_once_with(email="user@example.com", password="password123")
            mock_log_event.assert_called_once_with(
                event_type="USER_LOGIN_SUCCESS",
                details={"user_id": "user_xyz_123", "email": "user@example.com"}
            )
            self.assertEqual(status_code, 200)
            self.assertEqual(response["message"], "Login successful")
            self.assertEqual(response["user_id"], "user_xyz_123")
            self.assertIn("token", response)

            mock_authenticate_user.reset_mock()
            mock_log_event.reset_mock()

            failure_request_data = {"email": "nouser@example.com", "password": "wrongpassword"}
            mock_authenticate_user.return_value = None
            response, status_code = login_user_email(failure_request_data)
            mock_authenticate_user.assert_called_once_with(email="nouser@example.com", password="wrongpassword")
            mock_log_event.assert_called_once_with(
                event_type="USER_LOGIN_FAILURE",
                details={"attempted_email": "nouser@example.com", "reason": "Invalid credentials"}
            )
            self.assertEqual(status_code, 401)
            self.assertEqual(response, {"message": "Invalid credentials"})

    def test_reset_password_complexity_and_audit(self):
        """
        Test password reset scenarios: success, invalid OTP, and password complexity failure.
        Route function: reset_password_email(request_data)
        """
        with patch('rental_management_mvp.routes.auth_routes.OtpService', create=True) as MockOtpServiceClass, \
             patch('rental_management_mvp.routes.auth_routes.PasswordValidator', create=True) as MockPasswordValidatorClass, \
             patch('rental_management_mvp.routes.auth_routes.UserService', create=True) as MockUserServiceClass, \
             patch('rental_management_mvp.routes.auth_routes.AuditLogger', create=True) as MockAuditLoggerClass:

            mock_validate_otp = MockOtpServiceClass.validate_otp
            mock_is_password_complex = MockPasswordValidatorClass.is_password_complex_enough
            mock_reset_password = MockUserServiceClass.reset_password
            mock_log_event = MockAuditLoggerClass.log_event

            sample_email = "user@example.com"
            sample_otp = "123456"
            sample_complex_password = "NewPassword123!"
            sample_simple_password = "weak"

            request_data_success = {"email": sample_email, "otp": sample_otp, "new_password": sample_complex_password}
            mock_validate_otp.return_value = True
            mock_is_password_complex.return_value = (True, [])
            mock_reset_password.return_value = True
            response, status_code = reset_password_email(request_data_success)
            mock_validate_otp.assert_called_once_with(user_identifier=sample_email, otp_code=sample_otp, context="password_reset")
            mock_is_password_complex.assert_called_once_with(sample_complex_password)
            mock_reset_password.assert_called_once_with(email=sample_email, new_password=sample_complex_password)
            mock_log_event.assert_called_once_with(event_type="USER_PASSWORD_RESET_SUCCESS", details={"email": sample_email})
            self.assertEqual(status_code, 200)
            self.assertEqual(response, {"message": "Password reset successfully"})

            mock_validate_otp.reset_mock(); mock_is_password_complex.reset_mock(); mock_reset_password.reset_mock(); mock_log_event.reset_mock()

            request_data_invalid_otp = {"email": sample_email, "otp": "wrongotp", "new_password": sample_complex_password}
            mock_validate_otp.return_value = False
            response, status_code = reset_password_email(request_data_invalid_otp)
            mock_validate_otp.assert_called_once_with(user_identifier=sample_email, otp_code="wrongotp", context="password_reset")
            mock_is_password_complex.assert_not_called()
            mock_reset_password.assert_not_called()
            mock_log_event.assert_called_once_with(event_type="PASSWORD_RESET_OTP_VALIDATION_FAILURE", details={"email": sample_email, "reason": "Invalid or expired OTP"})
            self.assertEqual(status_code, 400)
            self.assertEqual(response, {"message": "Invalid or expired OTP"})

            mock_validate_otp.reset_mock(); mock_log_event.reset_mock()

            request_data_complexity_fail = {"email": sample_email, "otp": sample_otp, "new_password": sample_simple_password}
            password_complexity_errors = ["Too short", "No uppercase"]
            mock_validate_otp.return_value = True
            mock_is_password_complex.return_value = (False, password_complexity_errors)
            response, status_code = reset_password_email(request_data_complexity_fail)
            mock_validate_otp.assert_called_once_with(user_identifier=sample_email, otp_code=sample_otp, context="password_reset")
            mock_is_password_complex.assert_called_once_with(sample_simple_password)
            mock_reset_password.assert_not_called()
            mock_log_event.assert_called_once_with(event_type="PASSWORD_RESET_COMPLEXITY_FAILURE", details={"email": sample_email, "errors": password_complexity_errors})
            self.assertEqual(status_code, 400)
            self.assertEqual(response, {"message": "Password not complex", "errors": password_complexity_errors})

    def test_verify_otp_for_2fa_login(self):
        """
        Test OTP verification logic for various scenarios.
        Route function: verify_otp(request_data)
        """
        with patch('rental_management_mvp.routes.auth_routes.OtpService', create=True) as MockOtpServiceClass, \
             patch('rental_management_mvp.routes.auth_routes.AuditLogger', create=True) as MockAuditLoggerClass, \
             patch('rental_management_mvp.routes.auth_routes.UserService', create=True) as MockUserServiceClass:

            mock_validate_otp = MockOtpServiceClass.validate_otp
            mock_log_event = MockAuditLoggerClass.log_event
            sample_identifier = "user@example.com"; sample_otp_code = "123456"; sample_context = "2fa_login"

            request_data_success = {"identifier": sample_identifier, "otp_code": sample_otp_code, "context": sample_context}
            mock_validate_otp.return_value = True
            response, status_code = verify_otp(request_data_success)
            mock_validate_otp.assert_called_once_with(user_identifier=sample_identifier, otp_code=sample_otp_code, context=sample_context)
            mock_log_event.assert_called_once_with(event_type="OTP_VALIDATION_SUCCESS", details={"identifier": sample_identifier, "context": sample_context})
            self.assertEqual(status_code, 200)
            self.assertEqual(response, {"message": "OTP verified successfully"})

            mock_validate_otp.reset_mock(); mock_log_event.reset_mock()

            request_data_failure = {"identifier": sample_identifier, "otp_code": "wrongotp", "context": sample_context}
            mock_validate_otp.return_value = False
            response, status_code = verify_otp(request_data_failure)
            mock_validate_otp.assert_called_once_with(user_identifier=sample_identifier, otp_code="wrongotp", context=sample_context)
            mock_log_event.assert_called_once_with(event_type="OTP_VALIDATION_FAILURE", details={"identifier": sample_identifier, "context": sample_context, "reason": "Invalid or expired OTP"})
            self.assertEqual(status_code, 400)
            self.assertEqual(response, {"message": "Invalid OTP"})

    def test_register_phone_request_otp(self):
        """ Test requesting OTP for phone registration. """
        with patch('rental_management_mvp.routes.auth_routes.OtpService', create=True) as MockOtpServiceClass, \
             patch('rental_management_mvp.routes.auth_routes.AuditLogger', create=True) as MockAuditLoggerClass:
            mock_generate_and_send_otp = MockOtpServiceClass.generate_and_send_otp
            mock_log_event = MockAuditLoggerClass.log_event
            sample_phone = "+12345678900"

            request_data_success = {"phone_number": sample_phone}
            mock_generate_and_send_otp.return_value = True
            response, status_code = register_phone_request_otp(request_data_success)
            mock_generate_and_send_otp.assert_called_once_with(identifier=sample_phone, context="phone_registration")
            mock_log_event.assert_called_once_with(event_type="OTP_SENT_FOR_PHONE_REGISTRATION", details={"phone_number": sample_phone})
            self.assertEqual(status_code, 200)
            self.assertEqual(response, {"message": "OTP sent to phone for registration"})

            mock_generate_and_send_otp.reset_mock(); mock_log_event.reset_mock()

            request_data_failure = {"phone_number": sample_phone}
            mock_generate_and_send_otp.return_value = False
            response, status_code = register_phone_request_otp(request_data_failure)
            mock_generate_and_send_otp.assert_called_once_with(identifier=sample_phone, context="phone_registration")
            mock_log_event.assert_called_once_with(event_type="OTP_SEND_FAILURE_PHONE_REGISTRATION", details={"phone_number": sample_phone, "error": "OtpService failed to send OTP without explicit exception"})
            self.assertEqual(status_code, 500)
            self.assertEqual(response, {"message": "Failed to send OTP. Please try again later."})

            mock_generate_and_send_otp.reset_mock(); mock_log_event.reset_mock()
            mock_generate_and_send_otp.side_effect = Exception("SMS gateway down")
            response, status_code = register_phone_request_otp(request_data_failure)
            mock_log_event.assert_called_once_with(event_type="OTP_SEND_FAILURE_PHONE_REGISTRATION", details={"phone_number": sample_phone, "error": "SMS gateway down"})
            self.assertEqual(status_code, 500)

            response, status_code = register_phone_request_otp({})
            self.assertEqual(status_code, 400)
            self.assertEqual(response, {"message": "Phone number is required"})

    def test_verify_phone_otp(self):
        """ Test OTP verification for phone numbers. """
        with patch('rental_management_mvp.routes.auth_routes.OtpService', create=True) as MockOtpServiceClass, \
             patch('rental_management_mvp.routes.auth_routes.UserService', create=True) as MockUserServiceClass, \
             patch('rental_management_mvp.routes.auth_routes.AuditLogger', create=True) as MockAuditLoggerClass:
            mock_validate_otp = MockOtpServiceClass.validate_otp
            mock_mark_phone_verified = MockUserServiceClass.mark_phone_as_verified
            mock_log_event = MockAuditLoggerClass.log_event
            sample_phone = "+19876543210"; sample_otp = "654321"; context = "phone_verification"

            request_data_success = {"phone_number": sample_phone, "otp_code": sample_otp}
            mock_validate_otp.return_value = True
            response, status_code = verify_phone_otp(request_data_success)
            mock_validate_otp.assert_called_once_with(user_identifier=sample_phone, otp_code=sample_otp, context=context)
            mock_mark_phone_verified.assert_called_once_with(phone_number=sample_phone)
            mock_log_event.assert_called_once_with(event_type="PHONE_OTP_VALIDATION_SUCCESS", details={"phone_number": sample_phone, "context": context})
            self.assertEqual(status_code, 200)
            self.assertEqual(response, {"message": "Phone verified successfully"})

            mock_validate_otp.reset_mock(); mock_mark_phone_verified.reset_mock(); mock_log_event.reset_mock()

            request_data_failure = {"phone_number": sample_phone, "otp_code": "wrongotp"}
            mock_validate_otp.return_value = False
            response, status_code = verify_phone_otp(request_data_failure)
            mock_validate_otp.assert_called_once_with(user_identifier=sample_phone, otp_code="wrongotp", context=context)
            mock_mark_phone_verified.assert_not_called()
            mock_log_event.assert_called_once_with(event_type="PHONE_OTP_VALIDATION_FAILURE", details={"phone_number": sample_phone, "context": context, "reason": "Invalid or expired OTP"})
            self.assertEqual(status_code, 400)
            self.assertEqual(response, {"message": "Invalid OTP for phone verification"})

            mock_validate_otp.reset_mock(); mock_log_event.reset_mock()
            response, status_code = verify_phone_otp({"otp_code": sample_otp})
            self.assertEqual(status_code, 400); self.assertEqual(response, {"message": "Phone number is required"})
            response, status_code = verify_phone_otp({"phone_number": sample_phone})
            self.assertEqual(status_code, 400); self.assertEqual(response, {"message": "OTP code is required"})

    def test_login_user_phone(self):
        """ Test login with phone number and password. """
        with patch('rental_management_mvp.routes.auth_routes.UserService', create=True) as MockUserServiceClass, \
             patch('rental_management_mvp.routes.auth_routes.AuditLogger', create=True) as MockAuditLoggerClass:
            mock_auth_phone = MockUserServiceClass.authenticate_user_by_phone
            mock_log_event = MockAuditLoggerClass.log_event
            sample_phone = "+1234567890"; sample_pass = "password123"

            request_data_success = {"phone_number": sample_phone, "password": sample_pass}
            mock_user = MagicMock(user_id="phone_user_123")
            mock_auth_phone.return_value = mock_user
            response, status_code = login_user_phone(request_data_success)
            mock_auth_phone.assert_called_once_with(phone_number=sample_phone, password=sample_pass)
            mock_log_event.assert_called_once_with(event_type="USER_LOGIN_SUCCESS_PHONE", details={"user_id": "phone_user_123", "phone_number": sample_phone})
            self.assertEqual(status_code, 200); self.assertEqual(response["message"], "Login successful via phone"); self.assertEqual(response["token"], "dummy_phone_token")

            mock_auth_phone.reset_mock(); mock_log_event.reset_mock()

            request_data_fail = {"phone_number": sample_phone, "password": "wrongpassword"}
            mock_auth_phone.return_value = None
            response, status_code = login_user_phone(request_data_fail)
            mock_auth_phone.assert_called_once_with(phone_number=sample_phone, password="wrongpassword")
            mock_log_event.assert_called_once_with(event_type="USER_LOGIN_FAILURE_PHONE", details={"attempted_phone_number": sample_phone, "reason": "Invalid credentials"})
            self.assertEqual(status_code, 401); self.assertEqual(response, {"message": "Invalid credentials for phone login"})

            mock_auth_phone.reset_mock(); mock_log_event.reset_mock()
            response, status_code = login_user_phone({"password": sample_pass})
            self.assertEqual(status_code, 400); self.assertEqual(response, {"message": "Phone number is required"})
            response, status_code = login_user_phone({"phone_number": sample_phone})
            self.assertEqual(status_code, 400); self.assertEqual(response, {"message": "Password is required"})

    def test_request_password_reset_email(self):
        """ Test requesting a password reset via email. """
        with patch('rental_management_mvp.routes.auth_routes.OtpService', create=True) as MockOtpServiceClass, \
             patch('rental_management_mvp.routes.auth_routes.AuditLogger', create=True) as MockAuditLoggerClass:
            mock_gen_otp = MockOtpServiceClass.generate_and_send_otp
            mock_log_event = MockAuditLoggerClass.log_event
            sample_email = "user@example.com"

            request_data_success = {"email": sample_email}
            mock_gen_otp.return_value = True
            response, status_code = request_password_reset_email(request_data_success)
            mock_gen_otp.assert_called_once_with(identifier=sample_email, context="password_reset_email")
            mock_log_event.assert_called_once_with(event_type="PASSWORD_RESET_REQUEST_EMAIL_SENT", details={"email": sample_email})
            self.assertEqual(status_code, 200); self.assertEqual(response, {"message": "Password reset instructions sent to your email"})

            mock_gen_otp.reset_mock(); mock_log_event.reset_mock()
            response, status_code = request_password_reset_email({})
            self.assertEqual(status_code, 400); self.assertEqual(response, {"message": "Email is required"})
            mock_gen_otp.assert_not_called()

            mock_gen_otp.return_value = False
            response, status_code = request_password_reset_email(request_data_success)
            mock_log_event.assert_called_once_with(event_type="PASSWORD_RESET_REQUEST_EMAIL_FAILURE", details={"email": sample_email, "error": "OtpService failed to send OTP without explicit exception"})
            self.assertEqual(status_code, 500)

            mock_gen_otp.reset_mock(); mock_log_event.reset_mock()
            mock_gen_otp.side_effect = Exception("SMTP error")
            response, status_code = request_password_reset_email(request_data_success)
            mock_log_event.assert_called_once_with(event_type="PASSWORD_RESET_REQUEST_EMAIL_FAILURE", details={"email": sample_email, "error": "SMTP error"})
            self.assertEqual(status_code, 500)

    def test_request_password_reset_sms(self):
        """ Test requesting a password reset OTP via SMS. """
        with patch('rental_management_mvp.routes.auth_routes.OtpService', create=True) as MockOtpServiceClass, \
             patch('rental_management_mvp.routes.auth_routes.AuditLogger', create=True) as MockAuditLoggerClass:
            mock_gen_otp = MockOtpServiceClass.generate_and_send_otp
            mock_log_event = MockAuditLoggerClass.log_event
            sample_phone = "+12345678901"

            request_data_success = {"phone_number": sample_phone}
            mock_gen_otp.return_value = True
            response, status_code = request_password_reset_sms(request_data_success)
            mock_gen_otp.assert_called_once_with(identifier=sample_phone, context="password_reset_sms")
            mock_log_event.assert_called_once_with(event_type="PASSWORD_RESET_REQUEST_SMS_SENT", details={"phone_number": sample_phone})
            self.assertEqual(status_code, 200); self.assertEqual(response, {"message": "Password reset OTP sent to your phone"})

            mock_gen_otp.reset_mock(); mock_log_event.reset_mock()
            response, status_code = request_password_reset_sms({})
            self.assertEqual(status_code, 400); self.assertEqual(response, {"message": "Phone number is required"})
            mock_gen_otp.assert_not_called()

            mock_gen_otp.return_value = False
            response, status_code = request_password_reset_sms(request_data_success)
            mock_log_event.assert_called_once_with(event_type="PASSWORD_RESET_REQUEST_SMS_FAILURE", details={"phone_number": sample_phone, "error": "OtpService failed to send OTP for SMS password reset without explicit exception"})
            self.assertEqual(status_code, 500)

            mock_gen_otp.reset_mock(); mock_log_event.reset_mock()
            mock_gen_otp.side_effect = Exception("SMS error")
            response, status_code = request_password_reset_sms(request_data_success)
            mock_log_event.assert_called_once_with(event_type="PASSWORD_RESET_REQUEST_SMS_FAILURE", details={"phone_number": sample_phone, "error": "SMS error"})
            self.assertEqual(status_code, 500)

    def test_reset_password_sms(self):
        """ Test resetting password using SMS OTP. """
        with patch('rental_management_mvp.routes.auth_routes.OtpService', create=True) as MockOtpServiceClass, \
             patch('rental_management_mvp.routes.auth_routes.PasswordValidator', create=True) as MockPwValClass, \
             patch('rental_management_mvp.routes.auth_routes.UserService', create=True) as MockUserServiceClass, \
             patch('rental_management_mvp.routes.auth_routes.AuditLogger', create=True) as MockAuditLoggerClass:

            mock_validate_otp = MockOtpServiceClass.validate_otp
            mock_is_complex = MockPwValClass.is_password_complex_enough
            mock_reset_pass_phone = MockUserServiceClass.reset_password_for_phone
            mock_log_event = MockAuditLoggerClass.log_event
            sample_phone = "+12345678901"; sample_otp = "112233"; sample_new_pass = "NewSecurePassword1!"; sample_weak_pass = "weak"; context = "password_reset_sms"

            request_data_success = {"phone_number": sample_phone, "otp": sample_otp, "new_password": sample_new_pass}
            mock_validate_otp.return_value = True
            mock_is_complex.return_value = (True, [])
            response, status_code = reset_password_sms(request_data_success)
            mock_validate_otp.assert_called_once_with(user_identifier=sample_phone, otp_code=sample_otp, context=context)
            mock_is_complex.assert_called_once_with(sample_new_pass)
            mock_reset_pass_phone.assert_called_once_with(phone_number=sample_phone, new_password=sample_new_pass)
            mock_log_event.assert_called_once_with(event_type="USER_PASSWORD_RESET_SUCCESS_SMS", details={"phone_number": sample_phone})
            self.assertEqual(status_code, 200); self.assertEqual(response, {"message": "Password reset successfully via SMS"})

            mock_validate_otp.reset_mock(); mock_is_complex.reset_mock(); mock_reset_pass_phone.reset_mock(); mock_log_event.reset_mock()

            request_data_invalid_otp = {"phone_number": sample_phone, "otp": "wrongotp", "new_password": sample_new_pass}
            mock_validate_otp.return_value = False
            response, status_code = reset_password_sms(request_data_invalid_otp)
            mock_validate_otp.assert_called_once_with(user_identifier=sample_phone, otp_code="wrongotp", context=context)
            mock_is_complex.assert_not_called()
            mock_reset_pass_phone.assert_not_called()
            mock_log_event.assert_called_once_with(event_type="PASSWORD_RESET_SMS_OTP_VALIDATION_FAILURE", details={"phone_number": sample_phone, "reason": "Invalid or expired OTP"})
            self.assertEqual(status_code, 400)

            mock_validate_otp.reset_mock(); mock_log_event.reset_mock()

            request_data_weak_pass = {"phone_number": sample_phone, "otp": sample_otp, "new_password": sample_weak_pass}
            errors = ["Too short"]
            mock_validate_otp.return_value = True
            mock_is_complex.return_value = (False, errors)
            response, status_code = reset_password_sms(request_data_weak_pass)
            mock_validate_otp.assert_called_once_with(user_identifier=sample_phone, otp_code=sample_otp, context=context)
            mock_is_complex.assert_called_once_with(sample_weak_pass)
            mock_reset_pass_phone.assert_not_called()
            mock_log_event.assert_called_once_with(event_type="PASSWORD_RESET_SMS_COMPLEXITY_FAILURE", details={"phone_number": sample_phone, "errors": errors})
            self.assertEqual(status_code, 400)

            response, _ = reset_password_sms({"otp": sample_otp, "new_password": sample_new_pass})
            self.assertEqual(response, {"message": "Phone number is required"})
            response, _ = reset_password_sms({"phone_number": sample_phone, "new_password": sample_new_pass})
            self.assertEqual(response, {"message": "OTP is required"})
            response, _ = reset_password_sms({"phone_number": sample_phone, "otp": sample_otp})
            self.assertEqual(response, {"message": "New password is required"})

    def test_logout_user(self):
        """
        Test user logout.
        Route function: logout_user(request_data)
        """
        # Assuming AuthService is patched for token blacklisting
        with patch('rental_management_mvp.routes.auth_routes.AuthService', create=True) as MockAuthServiceClass, \
             patch('rental_management_mvp.routes.auth_routes.AuditLogger', create=True) as MockAuditLoggerClass:

            mock_blacklist_token = MockAuthServiceClass.blacklist_token
            mock_log_event = MockAuditLoggerClass.log_event

            sample_token = "dummy_auth_token_to_blacklist"
            # Conceptual user_id if it were extracted from token
            # In this skeleton, logout_user doesn't extract user_id for logging, but it's a good practice.
            # For the log, we'll just check for the token used.
            # sample_user_id = "user_abc_789"

            # --- Scenario 1: Successful Logout ---
            request_data_success = {"auth_token": sample_token} #, "user_id_from_token": sample_user_id}
            mock_blacklist_token.return_value = True

            response, status_code = logout_user(request_data_success)

            mock_blacklist_token.assert_called_once_with(token=sample_token)
            expected_log_details = {"token_used": sample_token}
            # if "user_id_from_token" in request_data_success: # Add user_id if it was conceptually passed
            #    expected_log_details["user_id"] = request_data_success["user_id_from_token"]
            mock_log_event.assert_called_once_with(
                event_type="USER_LOGOUT_SUCCESS",
                details=expected_log_details
            )
            self.assertEqual(status_code, 200)
            self.assertEqual(response, {"message": "Logout successful"})

            # Reset mocks
            mock_blacklist_token.reset_mock()
            mock_log_event.reset_mock()

            # --- Scenario 2: Token Not Provided ---
            response, status_code = logout_user({})
            self.assertEqual(status_code, 401) # Or 400 depending on desired behavior
            self.assertEqual(response, {"message": "Missing authentication token"})
            mock_blacklist_token.assert_not_called()
            mock_log_event.assert_not_called() # No action, so no log beyond potential framework-level auth fail

            # Reset mocks (though not strictly necessary as they weren't called)
            mock_blacklist_token.reset_mock()
            mock_log_event.reset_mock()

            # --- Scenario 3: Blacklisting Fails (AuthService returns False) ---
            mock_blacklist_token.return_value = False
            response, status_code = logout_user(request_data_success) # Re-use success data for token

            mock_blacklist_token.assert_called_once_with(token=sample_token)
            mock_log_event.assert_called_once_with(
                event_type="USER_LOGOUT_FAILURE",
                details={"token_used": sample_token, "reason": "Token blacklisting failed"}
            )
            self.assertEqual(status_code, 500)
            self.assertEqual(response, {"message": "Logout failed"})

            # Reset mocks
            mock_blacklist_token.reset_mock()
            mock_log_event.reset_mock()

            # --- Scenario 4: Blacklisting Fails (AuthService raises Exception) ---
            mock_blacklist_token.side_effect = Exception("Cache connection down")
            response, status_code = logout_user(request_data_success)

            mock_blacklist_token.assert_called_once_with(token=sample_token)
            mock_log_event.assert_called_once_with(
                event_type="USER_LOGOUT_ERROR",
                details={"token_used": sample_token, "error": "Cache connection down"}
            )
            self.assertEqual(status_code, 500)
            self.assertEqual(response, {"message": "An error occurred during logout"})

if __name__ == '__main__':
    unittest.main()
