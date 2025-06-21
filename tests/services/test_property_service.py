import unittest
from datetime import datetime, timedelta
from services.property_service import PropertyService
from models.property import Property, PropertyType, PropertyStatus
# Decimal is not used as Property model uses float for lat/long
# Import User model if landlord_id needs to be validated against existing users
# from models.user import User
from hermitta_app import create_app, db # Import app factory and db instance


class TestPropertyService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('test') # Use test configuration
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all() # Create all tables

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all() # Drop all tables
        cls.app_context.pop()

    def setUp(self):
        self.service = PropertyService()
        # Clear relevant tables before each test
        db.session.rollback()
        Property.query.delete()
        # If User model is involved (e.g. for landlord_id validation by service):
        # User.query.delete()
        db.session.commit()

        self.sample_property_data_full = {
            "landlord_id": 101, # Assume User 101 exists or service doesn't check FK yet
            "address_line_1": "123 Main St",
            "city": "Testville",
            "county": "Test County",
            "property_type": PropertyType.APARTMENT_UNIT, # Actual enum member
            "num_bedrooms": 3,
            "num_bathrooms": 2,
            "unit_number": "A1",
            "estate_neighborhood": "Green Acres",
            "ward": "Central Ward",
            "sub_county": "Test SubCounty",
            "address_line_2": "Block B, Apt 5",
            "postal_code": "12345",
            "size_sqft": 1200,
            "amenities": ["Pool", "Gym"],
            "photos_urls": ["http://example.com/photo1.jpg"],
            "main_photo_url": "http://example.com/main.jpg",
            "description": "A lovely place.",
            "status": PropertyStatus.VACANT, # Actual enum member
            "latitude": 1.234,
            "longitude": -0.5678
        }
        self.required_property_data = { # For tests that use string inputs for conversion
            "landlord_id": 102,
            "address_line_1": "456 Oak Ave",
            "city": "Model City",
            "county": "Model County",
            "property_type": "TOWNHOUSE", # String for service to convert
            "num_bedrooms": 2,
            "num_bathrooms": 1,
        }

    def tearDown(self):
        db.session.rollback()
        Property.query.delete()
        # User.query.delete() # If users are created
        db.session.commit()


    def test_create_property_success(self):
        created_property = self.service.create_property(self.sample_property_data_full.copy())

        self.assertIsInstance(created_property, Property)
        self.assertIsNotNone(created_property.property_id) # Should be set by DB
        self.assertEqual(created_property.landlord_id, self.sample_property_data_full["landlord_id"])
        self.assertEqual(created_property.address_line_1, self.sample_property_data_full["address_line_1"])
        self.assertEqual(created_property.city, self.sample_property_data_full["city"])
        self.assertEqual(created_property.property_type, self.sample_property_data_full["property_type"])
        self.assertEqual(created_property.status, self.sample_property_data_full["status"])
        self.assertEqual(created_property.latitude, self.sample_property_data_full["latitude"])
        self.assertEqual(created_property.longitude, self.sample_property_data_full["longitude"])
        self.assertIsInstance(created_property.created_at, datetime)
        self.assertIsInstance(created_property.updated_at, datetime)
        # self.assertEqual(len(self.service.properties), 1) # Service might not maintain an in-memory list
        # self.assertEqual(self.service.properties[0], created_property)

    def test_create_property_with_string_enums(self):
        data_with_string_enums = self.required_property_data.copy() # required_property_data already uses string for property_type
        # data_with_string_enums["property_type"] = "STUDIO_APARTMENT" # String value
        data_with_string_enums["status"] = "OCCUPIED" # String value

        created_property = self.service.create_property(data_with_string_enums)
        self.assertIsInstance(created_property, Property)
        self.assertEqual(created_property.property_type, PropertyType.TOWNHOUSE) # From required_property_data
        self.assertEqual(created_property.status, PropertyStatus.OCCUPIED) # Assuming service converts

    def test_create_property_missing_required_fields_handled_by_model(self):
        # This test relies on the service layer performing validation before model instantiation
        # or catching TypeErrors from the model and re-raising as ValueError.
        incomplete_data = {"landlord_id": 1} # Missing many required fields
        with self.assertRaisesRegex(ValueError, r"Missing required fields.*address_line_1"):
            self.service.create_property(incomplete_data)

    def test_get_property_found(self):
        created_property = self.service.create_property(self.required_property_data.copy())
        found_property = self.service.get_property_by_id(created_property.property_id) # Renamed for clarity
        self.assertIsNotNone(found_property)
        self.assertEqual(found_property.property_id, created_property.property_id)

    def test_get_property_not_found(self):
        found_property = self.service.get_property_by_id(99999) # Use a clearly non-existent ID
        self.assertIsNone(found_property)

    def test_update_property_success(self):
        created_property = self.service.create_property(self.required_property_data.copy())
        original_updated_at = created_property.updated_at

        update_data = {
            "description": "Updated description here.",
            "num_bedrooms": 3,
            "status": PropertyStatus.OCCUPIED # Actual enum member
        }

        updated_property = self.service.update_property(created_property.property_id, update_data)

        self.assertIsNotNone(updated_property)
        self.assertEqual(updated_property.description, "Updated description here.")
        self.assertEqual(updated_property.num_bedrooms, 3)
        self.assertEqual(updated_property.status, PropertyStatus.OCCUPIED)
        self.assertTrue(updated_property.updated_at > original_updated_at)

        refetched_property = self.service.get_property_by_id(created_property.property_id)
        self.assertEqual(refetched_property.description, "Updated description here.")
        self.assertEqual(refetched_property.updated_at, updated_property.updated_at)

    def test_update_property_with_string_status(self):
        created_property = self.service.create_property(self.required_property_data.copy())
        update_data = {"status": "UNDER_MAINTENANCE"} # String value for enum
        updated_property = self.service.update_property(created_property.property_id, update_data)
        self.assertIsNotNone(updated_property)
        self.assertEqual(updated_property.status, PropertyStatus.UNDER_MAINTENANCE) # Assuming service converts


    def test_update_property_not_found(self):
        update_data = {"description": "This should not apply."}
        updated_property = self.service.update_property(99999, update_data)
        self.assertIsNone(updated_property)

    def test_delete_property_success(self):
        created_property = self.service.create_property(self.required_property_data.copy())
        # self.assertEqual(len(self.service.properties), 1) # Service might not maintain in-memory list

        delete_result = self.service.delete_property(created_property.property_id)
        self.assertTrue(delete_result)
        # self.assertEqual(len(self.service.properties), 0)

        not_found_property = self.service.get_property_by_id(created_property.property_id)
        self.assertIsNone(not_found_property)

    def test_delete_property_not_found(self):
        delete_result = self.service.delete_property(99999)
        self.assertFalse(delete_result)

if __name__ == '__main__':
    unittest.main()
