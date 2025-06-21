import unittest
from datetime import datetime
from models.audit_log import AuditLog, AuditActionCategory, AuditActionStatus # AuditActionType removed
from models.enums import AuditLogEvent # Import the correct Enum
from hermitta_app import create_app, db # Import app factory and db instance

class TestAuditLog(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('test') # Use test configuration
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        # db.create_all() # Not strictly necessary for model unit tests unless FKs are involved

    @classmethod
    def tearDownClass(cls):
        # db.drop_all()
        cls.app_context.pop()


    def test_instantiation_with_required_fields(self):
        """Test instantiation with only required fields and default values."""
        now = datetime.utcnow()
        log = AuditLog(
            log_id=1,
            timestamp=now,
            event_type=AuditLogEvent.USER_LOGIN_SUCCESS # Changed from action_type
        )
        self.assertEqual(log.log_id, 1)
        self.assertEqual(log.timestamp, now)
        self.assertIsInstance(log.timestamp, datetime)
        self.assertEqual(log.event_type, AuditLogEvent.USER_LOGIN_SUCCESS) # Changed from action_type
        self.assertIsInstance(log.event_type, AuditLogEvent) # Changed from AuditActionType

        # Check default values
        self.assertEqual(log.status, AuditActionStatus.SUCCESS) # Assuming this default is set in model
        self.assertIsInstance(log.status, AuditActionStatus) # Assuming this default is set in model
        self.assertIsNone(log.user_id)
        self.assertIsNone(log.target_entity_type)
        self.assertIsNone(log.target_entity_id)
        # self.assertIsNone(log.details_before) # details_before was removed from model
        # self.assertIsNone(log.details_after) # details_after was removed from model
        self.assertIsNone(log.details) # Check new consolidated field
        self.assertIsNone(log.ip_address)
        self.assertIsNone(log.user_agent)
        # self.assertIsNone(log.failure_reason) # failure_reason was removed from model
        self.assertIsNone(log.action_category) # Assuming this default is set in model or nullable
        # self.assertIsNone(log.notes) # notes was removed from model

    def test_instantiation_with_all_fields(self):
        """Test instantiation with all fields provided."""
        ts = datetime(2023, 10, 26, 10, 0, 0)
        # details_b = {"key_before": "value_before"} # Old fields
        # details_a = {"key_after": "value_after"} # Old fields
        log_details = {"change_summary": "Rent updated", "old_rent": 500, "new_rent": 550}


        log = AuditLog(
            log_id=2,
            timestamp=ts,
            event_type=AuditLogEvent.ENTITY_UPDATED, # Changed from action_type
            user_id=101,
            target_entity_type="Property",
            target_entity_id="505", # Model has String for this ID
            details=log_details, # Using new consolidated field
            ip_address="192.168.0.1",
            user_agent="TestAgent/1.0",
            status=AuditActionStatus.SUCCESS,
            # failure_reason=None, # Removed from model
            action_category=AuditActionCategory.PROPERTY_MANAGEMENT,
            # notes="Property rent was updated." # Removed from model
        )

        self.assertEqual(log.log_id, 2)
        self.assertEqual(log.timestamp, ts)
        self.assertEqual(log.event_type, AuditLogEvent.ENTITY_UPDATED) # Changed from action_type
        self.assertEqual(log.user_id, 101)
        self.assertEqual(log.target_entity_type, "Property")
        self.assertEqual(log.target_entity_id, "505")
        # self.assertEqual(log.details_before, details_b) # Old field
        # self.assertIsInstance(log.details_before, dict) # Old field
        # self.assertEqual(log.details_after, details_a) # Old field
        # self.assertIsInstance(log.details_after, dict) # Old field
        self.assertEqual(log.details, log_details)
        self.assertIsInstance(log.details, dict)
        self.assertEqual(log.ip_address, "192.168.0.1")
        self.assertEqual(log.user_agent, "TestAgent/1.0")
        self.assertEqual(log.status, AuditActionStatus.SUCCESS)
        # self.assertIsNone(log.failure_reason) # Removed from model
        self.assertEqual(log.action_category, AuditActionCategory.PROPERTY_MANAGEMENT)
        self.assertIsInstance(log.action_category, AuditActionCategory)
        # self.assertEqual(log.notes, "Property rent was updated.") # Removed from model

    def test_instantiation_with_failure_status(self):
        """Test instantiation when status is FAILURE."""
        ts = datetime.utcnow()
        log = AuditLog(
            log_id=3,
            timestamp=ts,
            event_type=AuditLogEvent.USER_LOGIN_FAILURE, # Changed
            user_id=None,
            ip_address="203.0.113.10",
            status=AuditActionStatus.FAILURE,
            # failure_reason="Invalid credentials provided.", # Removed from model, should go in details
            details={"reason": "Invalid credentials provided."},
            action_category=AuditActionCategory.AUTHENTICATION
        )
        self.assertEqual(log.log_id, 3)
        self.assertEqual(log.status, AuditActionStatus.FAILURE)
        self.assertIsInstance(log.status, AuditActionStatus)
        # self.assertEqual(log.failure_reason, "Invalid credentials provided.")
        self.assertEqual(log.details, {"reason": "Invalid credentials provided."})
        self.assertEqual(log.action_category, AuditActionCategory.AUTHENTICATION)

    def test_target_entity_id_types(self):
        """Test target_entity_id with int and str types (model uses String)."""
        ts = datetime.utcnow()
        log_int_id_as_str = AuditLog(
            log_id=4, timestamp=ts, event_type=AuditLogEvent.ENTITY_CREATED, # Changed
            target_entity_id="1001" # Stored as string
        )
        self.assertEqual(log_int_id_as_str.target_entity_id, "1001")
        self.assertIsInstance(log_int_id_as_str.target_entity_id, str)

        log_str_id = AuditLog(
            log_id=5, timestamp=ts, event_type=AuditLogEvent.ENTITY_UPDATED, # Changed
            target_entity_id="doc_abc_123"
        )
        self.assertEqual(log_str_id.target_entity_id, "doc_abc_123")
        self.assertIsInstance(log_str_id.target_entity_id, str)

    def test_enum_field_validity(self):
        """Test that enum fields are instances of their respective Enum types."""
        ts = datetime.utcnow()
        log = AuditLog(
            log_id=6,
            timestamp=ts,
            event_type=AuditLogEvent.ENTITY_STATUS_CHANGED, # Changed, assuming a suitable event
            status=AuditActionStatus.PENDING,
            action_category=AuditActionCategory.MAINTENANCE_MANAGEMENT
        )
        self.assertIsInstance(log.event_type, AuditLogEvent) # Changed
        self.assertIsInstance(log.status, AuditActionStatus)
        self.assertIsInstance(log.action_category, AuditActionCategory)

if __name__ == '__main__':
    unittest.main()
