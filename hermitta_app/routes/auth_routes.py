from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from hermitta_app import db
from models import User, AuditLog, Notification, NotificationTemplate # Notification related imports might be for future routes here
# Import enums used by User model directly from User model file
from models.user import UserRole, PreferredLoginMethod, PreferredLanguage
# Import enums used by AuditLog and Notification from the central enums file
from models.enums import AuditLogEvent, NotificationType, NotificationChannel, NotificationStatus as NotificationState

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/v1/auth')

# --- User Registration (Email) ---
@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    required_fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 'role']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return jsonify({"message": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    email = data['email'].lower().strip()
    password = data['password']
    first_name = data['first_name'].strip()
    last_name = data['last_name'].strip()
    phone_number = data['phone_number'].strip()
    role_str = data['role'].upper()

    # TODO: Add more robust email and phone number validation
    if len(password) < 8: # Simple password complexity, can be enhanced
        # Audit log for failed attempt (optional here, more critical on login)
        return jsonify({"message": "Password must be at least 8 characters long"}), 400

    try:
        role_enum = UserRole[role_str]
    except KeyError:
        valid_roles = [r.value for r in UserRole]
        return jsonify({"message": f"Invalid role. Must be one of: {', '.join(valid_roles)}"}), 400

    if db.session.query(User).filter_by(email=email).first():
        return jsonify({"message": "Email address already registered"}), 409 # Conflict

    if db.session.query(User).filter_by(phone_number=phone_number).first():
        return jsonify({"message": "Phone number already registered"}), 409 # Conflict

    hashed_password = generate_password_hash(password)

    new_user = User(
        email=email,
        password_hash=hashed_password,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        role=role_enum,
        is_active=True, # User model uses is_active boolean
        preferred_login_method=PreferredLoginMethod.EMAIL, # Default
        preferred_language=PreferredLanguage.EN_KE # Default, matches enum in User model
    )

    try:
        db.session.add(new_user)
        db.session.flush() # To get new_user.user_id for audit log

        # Audit Log
        audit_log = AuditLog(
            user_id=new_user.user_id, # Action performed on this new user
            event_type=AuditLogEvent.USER_REGISTERED,
            details={
                "registered_user_id": new_user.user_id,
                "email": email,
                "role": role_enum.value
            }
        )
        db.session.add(audit_log)
        db.session.commit()

        # Prepare response (excluding sensitive data)
        user_response = {
            "user_id": new_user.user_id,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "phone_number": new_user.phone_number,
            "role": new_user.role.value,
            "is_active": new_user.is_active, # Reflects the User model field
            "created_at": new_user.created_at.isoformat()
        }
        return jsonify({"message": "User registered successfully", "user": user_response}), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error during user registration: {e}", exc_info=True)
        # Generic audit log for system error during registration
        failed_audit_log = AuditLog(
            event_type=AuditLogEvent.SYSTEM_ERROR,
            details={"error_context": "user_registration", "exception": str(e)}
        )
        db.session.add(failed_audit_log)
        db.session.commit()
        return jsonify({"message": "Registration failed due to an internal error"}), 500

# Placeholder for other auth routes to be implemented
# /login, /logout, /password-reset/request, /password-reset/confirm, /me
# ... (to be added sequentially) ...

# --- User Login (Email) ---
@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    email = data.get('email', '').lower().strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = db.session.query(User).filter_by(email=email).first()

    audit_details = {"attempted_email": email}
    if user and user.password_hash and check_password_hash(user.password_hash, password):
        if not user.is_active:
            audit_details["reason"] = "Account inactive"
            audit_log = AuditLog(event_type=AuditLogEvent.USER_LOGIN_FAILURE, details=audit_details)
            db.session.add(audit_log)
            db.session.commit()
            return jsonify({"message": "Account is inactive. Please contact support."}), 403 # Forbidden

        # TODO: Implement actual token generation (e.g., JWT)
        # For now, a dummy token. In a real app, this token would be tied to the user_id and have an expiry.
        dummy_token = "dummy_jwt_token_for_" + str(user.user_id)

        audit_details["user_id"] = user.user_id
        audit_log = AuditLog(event_type=AuditLogEvent.USER_LOGIN_SUCCESS, details=audit_details, user_id=user.user_id)
        db.session.add(audit_log)
        db.session.commit()

        user_response = {
            "user_id": user.user_id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role.value
        }
        return jsonify({
            "message": "Login successful",
            "user": user_response,
            "access_token": dummy_token
            # "token_type": "bearer" # Standard for JWT
            # "expires_in": 3600 # Example: 1 hour
        }), 200
    else:
        audit_details["reason"] = "Invalid credentials"
        # Check if user exists to avoid different audit logs for invalid email vs invalid password,
        # but don't reveal this in the response to prevent email enumeration.
        if user: # User exists, so password was wrong
             audit_log = AuditLog(event_type=AuditLogEvent.USER_LOGIN_FAILURE, details=audit_details, user_id=user.user_id)
        else: # User (email) does not exist
             audit_log = AuditLog(event_type=AuditLogEvent.USER_LOGIN_FAILURE, details=audit_details)

        db.session.add(audit_log)
        db.session.commit()
        return jsonify({"message": "Invalid email or password"}), 401

# --- User Logout ---
# This is a conceptual endpoint. Actual token invalidation requires a token blacklist
# and a mechanism to check it, which is beyond simple stateless JWTs without extra infrastructure.
# For session-based auth, it would clear the session.
@auth_bp.route('/logout', methods=['POST'])
def logout_user():
    # In a real app, you'd get the token from the Authorization header:
    # auth_header = request.headers.get('Authorization')
    # token = auth_header.split(" ")[1] if auth_header and auth_header.startswith("Bearer ") else None

    # For now, assume token is passed in body or this is a conceptual logout
    # For testing, we can assume a user_id is known (e.g., from a decoded token in a real app)
    # We'll simulate this by expecting a 'user_id' in the request for logging,
    # though in a real scenario, this would come from the authenticated session/token.

    data = request.get_json()
    user_id_for_log = data.get("user_id_for_log_simulated") if data else None # Simulate getting user_id from token

    # TODO: Implement token blacklisting if using JWTs that need server-side invalidation.
    # For now, this endpoint is largely conceptual for completing the logout flow.

    audit_details = {"action": "User initiated logout"}
    if user_id_for_log:
        audit_details["user_id"] = user_id_for_log

    audit_log = AuditLog(
        user_id=user_id_for_log, # Can be None if token is invalid or user not identifiable
        event_type=AuditLogEvent.USER_LOGOUT,
        details=audit_details
    )
    db.session.add(audit_log)
    db.session.commit()

    return jsonify({"message": "Logout successful"}), 200

# --- Request Password Reset (Email) ---
@auth_bp.route('/password-reset/request', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    if not data or not data.get('email'):
        return jsonify({"message": "Email is required"}), 400

    email = data['email'].lower().strip()
    user = db.session.query(User).filter_by(email=email).first()

    audit_details = {"email_provided": email}

    if user:
        # TODO: Generate a secure, unique, time-limited password reset token.
        # Store this token hashed in the DB, associated with user_id and an expiry.
        # For now, we'll simulate a token.
        reset_token_placeholder = "simulated_reset_token_for_" + str(user.user_id)

        # TODO: Determine the actual URL for the password reset link
        # reset_url = f"https://yourfrontend.com/reset-password?token={reset_token_placeholder}"
        reset_url = f"http://localhost:3000/auth/reset-password?token={reset_token_placeholder}&email={user.email}" # Example for local dev

        # Find a suitable notification template or use direct content
        # For simplicity, we'll assume a template exists or create a direct notification content
        # This would ideally look up a NotificationTemplate for PASSWORD_RESET_REQUEST

        notification_content = f"Password reset requested. Click here: {reset_url} or use token: {reset_token_placeholder}"
        notification_subject = "Password Reset Request"

        # Create a Notification record
        # This assumes a NotificationService or direct model interaction would handle sending
        new_notification = Notification(
            user_id=user.user_id,
            notification_type=NotificationType.PASSWORD_RESET_REQUEST,
            channel=NotificationChannel.EMAIL, # Default to email for password reset
            subject=notification_subject,
            content=notification_content,
            status=NotificationState.PENDING # To be picked up by a dispatcher
        )
        db.session.add(new_notification)

        audit_details["user_id"] = user.user_id
        audit_details["action"] = "Password reset token generated and notification created."
        audit_log_event = AuditLogEvent.USER_PASSWORD_RESET_REQUEST

        # In a real scenario, you'd store the token and its expiry with the user record
        # user.password_reset_token = generate_password_hash(reset_token_placeholder) # Store hashed token
        # user.password_reset_token_expires_at = datetime.utcnow() + timedelta(hours=1)
        # db.session.add(user)

    else:
        # User not found. Still log an attempt but don't reveal user existence.
        audit_details["action"] = "Password reset requested for non-existent email."
        audit_log_event = AuditLogEvent.USER_PASSWORD_RESET_REQUEST # Or a more specific "NOT_FOUND" type if desired

    audit_log = AuditLog(
        user_id=user.user_id if user else None,
        event_type=audit_log_event,
        details=audit_details
    )
    db.session.add(audit_log)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in password reset request: {e}", exc_info=True)
        # Log system error
        sys_err_audit = AuditLog(event_type=AuditLogEvent.SYSTEM_ERROR, details={"error_context": "password_reset_request", "exception": str(e)})
        db.session.add(sys_err_audit)
        db.session.commit() # Commit audit log even if main transaction failed
        return jsonify({"message": "An error occurred. Please try again."}), 500

    # Always return a generic success message to prevent email enumeration
    return jsonify({"message": "If your email is registered, you will receive password reset instructions."}), 200

# --- Reset Password (Email) ---
@auth_bp.route('/password-reset/confirm', methods=['POST'])
def reset_password():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    token = data.get('token') # In a real app, this would be a secure, unique token
    email = data.get('email') # Often, email is part of the reset flow or embedded in token
    new_password = data.get('new_password')

    required_fields_msg = "Token, email, and new_password are required"
    if not token or not email or not new_password:
        return jsonify({"message": required_fields_msg}), 400

    email = email.lower().strip()

    # TODO: Implement proper token validation:
    # 1. Find user by email.
    # 2. Check if user.password_reset_token (hashed) matches hash of provided token.
    # 3. Check if token is expired (user.password_reset_token_expires_at).
    # For now, we'll simulate: if token starts with "simulated_reset_token_for_", it's "valid" for that user.

    user = db.session.query(User).filter_by(email=email).first()
    is_token_valid_simulation = user and token.startswith("simulated_reset_token_for_" + str(user.user_id))

    audit_details = {"email": email}

    if not user or not is_token_valid_simulation:
        audit_details["reason"] = "Invalid or expired token"
        if user: audit_details["user_id"] = user.user_id
        audit_log = AuditLog(event_type=AuditLogEvent.USER_PASSWORD_RESET_FAILURE, details=audit_details)
        db.session.add(audit_log)
        db.session.commit()
        return jsonify({"message": "Invalid or expired password reset token."}), 400

    if len(new_password) < 8: # Simple password complexity
        audit_details["user_id"] = user.user_id
        audit_details["reason"] = "New password too short"
        audit_log = AuditLog(event_type=AuditLogEvent.USER_PASSWORD_RESET_FAILURE, details=audit_details)
        db.session.add(audit_log)
        db.session.commit()
        return jsonify({"message": "Password must be at least 8 characters long"}), 400

    try:
        user.password_hash = generate_password_hash(new_password)
        # TODO: Invalidate the reset token after use
        # user.password_reset_token = None
        # user.password_reset_token_expires_at = None
        db.session.add(user)

        audit_details["user_id"] = user.user_id
        audit_log = AuditLog(
            user_id=user.user_id,
            event_type=AuditLogEvent.USER_PASSWORD_RESET_SUCCESS,
            details=audit_details
        )
        db.session.add(audit_log)
        db.session.commit()
        return jsonify({"message": "Password has been reset successfully."}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error during password reset confirmation: {e}", exc_info=True)
        sys_err_audit = AuditLog(event_type=AuditLogEvent.SYSTEM_ERROR, details={"error_context": "password_reset_confirm", "exception": str(e)})
        db.session.add(sys_err_audit)
        db.session.commit()
        return jsonify({"message": "An error occurred while resetting password."}), 500

# --- Get Current Authenticated User (/me) ---
# This route would require authentication (e.g., a valid JWT in Authorization header)
# A decorator like @jwt_required() from Flask-JWT-Extended would typically be used.
@auth_bp.route('/me', methods=['GET'])
def get_me():
    # TODO: Implement actual token validation and user retrieval from token.
    # For now, this is a placeholder.
    # current_user_id = get_jwt_identity() # Example with Flask-JWT-Extended
    # user = db.session.query(User).get(current_user_id)

    # Simulating a user is found for demonstration if we had a way to pass user_id
    simulated_user_id = request.args.get('simulated_user_id_for_me')
    if simulated_user_id:
        try:
            user = db.session.query(User).get(int(simulated_user_id))
            if user:
                user_response = {
                    "user_id": user.user_id, "email": user.email, "first_name": user.first_name,
                    "last_name": user.last_name, "role": user.role.value, "is_active": user.is_active,
                    "phone_number": user.phone_number,
                    "preferred_login_method": user.preferred_login_method.value,
                    "preferred_language": user.preferred_language.value
                }
                return jsonify(user_response), 200
            else:
                 return jsonify({"message": "Simulated user not found"}), 404
        except ValueError:
            return jsonify({"message": "Invalid simulated_user_id_for_me format"}), 400


    return jsonify({"message": "Authentication required to access this endpoint. (Not yet implemented)"}), 401
