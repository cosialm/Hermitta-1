import unittest
from datetime import datetime, timedelta
from services.property_service import PropertyService
from models.property import Property, PropertyType, PropertyStatus
# Decimal is not used as Property model uses float for lat/long

class TestPropertyService(unittest.TestCase):

    def setUp(self):
        self.service = PropertyService()
        self.sample_property_data_full = {
            "landlord_id": 101,
            "address_line_1": "123 Main St",
            "city": "Testville",
            "county": "Test County",
            "property_type": PropertyType.APARTMENT_UNIT,
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
            "status": PropertyStatus.VACANT, # Explicitly set for testing
            "latitude": 1.234, # float
            "longitude": -0.5678 # float
        }
        self.required_property_data = {
            "landlord_id": 102,
            "address_line_1": "456 Oak Ave",
            "city": "Model City",
            "county": "Model County",
            "property_type": PropertyType.TOWNHOUSE,
            "num_bedrooms": 2,
            "num_bathrooms": 1,
        }


    def test_create_property_success(self):
        created_property = self.service.create_property(self.sample_property_data_full.copy())

        self.assertIsInstance(created_property, Property)
        self.assertEqual(created_property.property_id, 1) # First ID
        self.assertEqual(created_property.landlord_id, self.sample_property_data_full["landlord_id"])
        self.assertEqual(created_property.address_line_1, self.sample_property_data_full["address_line_1"])
        self.assertEqual(created_property.city, self.sample_property_data_full["city"])
        self.assertEqual(created_property.property_type, self.sample_property_data_full["property_type"])
        self.assertEqual(created_property.status, self.sample_property_data_full["status"])
        self.assertEqual(created_property.latitude, self.sample_property_data_full["latitude"])
        self.assertEqual(created_property.longitude, self.sample_property_data_full["longitude"])
        self.assertIsInstance(created_property.created_at, datetime)
        self.assertIsInstance(created_property.updated_at, datetime)
        self.assertEqual(len(self.service.properties), 1)
        self.assertEqual(self.service.properties[0], created_property)

    def test_create_property_with_string_enums(self):
        data_with_string_enums = self.required_property_data.copy()
        data_with_string_enums["property_type"] = "STUDIO_APARTMENT" # String value
        data_with_string_enums["status"] = "OCCUPIED" # String value

        created_property = self.service.create_property(data_with_string_enums)
        self.assertIsInstance(created_property, Property)
        self.assertEqual(created_property.property_type, PropertyType.STUDIO_APARTMENT)
        self.assertEqual(created_property.status, PropertyStatus.OCCUPIED)

    def test_create_property_missing_required_fields_handled_by_model(self):
        # This test assumes Property.__init__ will raise TypeError if required fields are missing
        # and the service might wrap it in a ValueError or let it propagate.
        # The service stub currently raises ValueError if Property instantiation fails due to TypeError.
        incomplete_data = {"landlord_id": 1} # Missing many required fields
        with self.assertRaises(ValueError): # Or TypeError if service doesn't catch it
            self.service.create_property(incomplete_data)

    def test_get_property_found(self):
        created_property = self.service.create_property(self.required_property_data.copy())
        found_property = self.service.get_property(created_property.property_id)
        self.assertIsNotNone(found_property)
        self.assertEqual(found_property, created_property)

    def test_get_property_not_found(self):
        found_property = self.service.get_property(999) # Non-existent ID
        self.assertIsNone(found_property)

    def test_update_property_success(self):
        created_property = self.service.create_property(self.required_property_data.copy())
        original_updated_at = created_property.updated_at

        update_data = {
            "description": "Updated description here.",
            "num_bedrooms": 3,
            "status": PropertyStatus.OCCUPIED
        }
        # Allow a small delay for updated_at comparison
        # time.sleep(0.001) # Not ideal in tests, but datetime.utcnow() precision can be an issue

        updated_property = self.service.update_property(created_property.property_id, update_data)

        self.assertIsNotNone(updated_property)
        self.assertEqual(updated_property.description, "Updated description here.")
        self.assertEqual(updated_property.num_bedrooms, 3)
        self.assertEqual(updated_property.status, PropertyStatus.OCCUPIED)
        self.assertTrue(updated_property.updated_at > original_updated_at)

        # Verify in-memory store is updated
        refetched_property = self.service.get_property(created_property.property_id)
        self.assertEqual(refetched_property.description, "Updated description here.")
        self.assertEqual(refetched_property.updated_at, updated_property.updated_at)

    def test_update_property_with_string_status(self):
        created_property = self.service.create_property(self.required_property_data.copy())
        update_data = {"status": "UNDER_MAINTENANCE"} # String value
        updated_property = self.service.update_property(created_property.property_id, update_data)
        self.assertIsNotNone(updated_property)
        self.assertEqual(updated_property.status, PropertyStatus.UNDER_MAINTENANCE)


    def test_update_property_not_found(self):
        update_data = {"description": "This should not apply."}
        updated_property = self.service.update_property(999, update_data) # Non-existent ID
        self.assertIsNone(updated_property)

    def test_delete_property_success(self):
        created_property = self.service.create_property(self.required_property_data.copy())
        self.assertEqual(len(self.service.properties), 1)

        delete_result = self.service.delete_property(created_property.property_id)
        self.assertTrue(delete_result)
        self.assertEqual(len(self.service.properties), 0)

        not_found_property = self.service.get_property(created_property.property_id)
        self.assertIsNone(not_found_property)

    def test_delete_property_not_found(self):
        delete_result = self.service.delete_property(999) # Non-existent ID
        self.assertFalse(delete_result)

if __name__ == '__main__':
    unittest.main()
