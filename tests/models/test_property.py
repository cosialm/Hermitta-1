# Unit tests for the Property model (models/property.py)
# Assuming a testing framework like unittest or pytest

import unittest
# from decimal import Decimal # No longer needed as lat/long are float
from models.property import Property, PropertyType, PropertyStatus
from datetime import datetime

class TestPropertyModel(unittest.TestCase):

    def setUp(self):
        """Setup basic property instances for testing if needed."""
        # Example:
        # self.property1 = Property(
        #     property_id=1, landlord_id=10, address_line_1="123 Main St",
        #     city="Testville", county="Test County", property_type=PropertyType.APARTMENT_UNIT,
        #     num_bedrooms=2, num_bathrooms=1,
        #     # ... other mandatory fields
        # )
        pass

    def test_property_creation_with_lat_long(self):
        """
        Test that a Property instance can be created with latitude and longitude.
        """
        prop_data = {
            "property_id": 1, "landlord_id": 10, "address_line_1": "Geo St",
            "city": "Localtown", "county": "Geo County",
            "property_type": PropertyType.TOWNHOUSE, "num_bedrooms": 3, "num_bathrooms": 2,
            "latitude": 1.2345, "longitude": -0.5678
        }
        property_with_geo = Property(**prop_data)

        self.assertEqual(property_with_geo.latitude, 1.2345)
        self.assertEqual(property_with_geo.longitude, -0.5678)
        self.assertEqual(property_with_geo.property_id, 1)
        self.assertEqual(property_with_geo.landlord_id, 10)
        self.assertEqual(property_with_geo.address_line_1, "Geo St")
        self.assertEqual(property_with_geo.city, "Localtown")
        self.assertEqual(property_with_geo.county, "Geo County")
        self.assertEqual(property_with_geo.property_type, PropertyType.TOWNHOUSE)
        self.assertEqual(property_with_geo.num_bedrooms, 3)
        self.assertEqual(property_with_geo.num_bathrooms, 2)

    def test_property_lat_long_optional(self):
        """
        Test that latitude and longitude are optional.
        """
        prop_data = {
            "property_id": 2, "landlord_id": 11, "address_line_1": "NoGeo St",
            "city": "Mapless City", "county": "Terra Incognita",
            "property_type": PropertyType.SINGLE_ROOM, "num_bedrooms": 1, "num_bathrooms": 1
            # latitude and longitude are omitted
        }
        property_without_geo = Property(**prop_data)

        self.assertIsNone(property_without_geo.latitude)
        self.assertIsNone(property_without_geo.longitude)
        self.assertEqual(property_without_geo.property_id, 2)
        self.assertEqual(property_without_geo.landlord_id, 11)
        self.assertEqual(property_without_geo.address_line_1, "NoGeo St")
        self.assertEqual(property_without_geo.city, "Mapless City")
        self.assertEqual(property_without_geo.county, "Terra Incognita")
        self.assertEqual(property_without_geo.property_type, PropertyType.SINGLE_ROOM)
        self.assertEqual(property_without_geo.num_bedrooms, 1)
        self.assertEqual(property_without_geo.num_bathrooms, 1)

    def test_setting_lat_long_after_creation(self):
        """
        Test setting latitude and longitude after property instance creation.
        """
        prop_data = {
            "property_id": 3, "landlord_id": 12, "address_line_1": "Later Geo St",
            "city": "Update City", "county": "Change County",
            "property_type": PropertyType.STUDIO_APARTMENT, "num_bedrooms": 1, "num_bathrooms": 1
        }
        prop = Property(**prop_data)
        self.assertIsNone(prop.latitude)
        self.assertIsNone(prop.longitude) # Also check longitude initial state

        prop.latitude = 5.555
        prop.longitude = -2.222

        self.assertEqual(prop.latitude, 5.555)
        self.assertEqual(prop.longitude, -2.222)
        self.assertEqual(prop.property_id, 3) # Add assertions for other fields
        self.assertEqual(prop.landlord_id, 12)
        self.assertEqual(prop.address_line_1, "Later Geo St")
        self.assertEqual(prop.city, "Update City")
        self.assertEqual(prop.county, "Change County")
        self.assertEqual(prop.property_type, PropertyType.STUDIO_APARTMENT)
        self.assertEqual(prop.num_bedrooms, 1)
        self.assertEqual(prop.num_bathrooms, 1)

    def test_property_enums_and_defaults(self):
        """
        Test default enum values and assignment.
        Also tests behavior with invalid enum string (if applicable based on model validation).
        """
        prop_data_minimal = {
            "property_id": 4, "landlord_id": 13, "address_line_1": "Default St",
            "city": "Initial City", "county": "Default County",
            "property_type": PropertyType.APARTMENT_UNIT,
            "num_bedrooms": 2, "num_bathrooms": 1
        }
        prop = Property(**prop_data_minimal)

        # Test default status
        self.assertEqual(prop.status, PropertyStatus.VACANT)

        # Test assigned property_type
        self.assertEqual(prop.property_type, PropertyType.APARTMENT_UNIT)

        # Test providing an invalid string for an enum
        # The Property model's __init__ uses type hints.
        # Python's default behavior for type hints doesn't raise an error at runtime
        # if an incorrect type is passed. It would require explicit validation logic
        # (e.g., isinstance checks or a library like Pydantic) in the model itself.
        # This test will reflect the current behavior.

        # If strict enum validation was in place (e.g. using Pydantic or custom validation):
        # with self.assertRaises(ValueError): # Or TypeError, depending on implementation
        #     prop_data_invalid_enum = {
        #         "property_id": 5, "landlord_id": 14, "address_line_1": "Enum Test St",
        #         "city": "Validation City", "county": "Check County",
        #         "property_type": "INVALID_TYPE", # Invalid enum string
        #         "num_bedrooms": 1, "num_bathrooms": 1
        #     }
        #     Property(**prop_data_invalid_enum)

        # Current behavior: it will assign the string directly if no validation
        prop_data_invalid_enum_direct_assign = {
            "property_id": 5, "landlord_id": 14, "address_line_1": "Enum Test St",
            "city": "Validation City", "county": "Check County",
            "property_type": "INVALID_TYPE", # Invalid enum string
            "num_bedrooms": 1, "num_bathrooms": 1
        }
        prop_invalid = Property(**prop_data_invalid_enum_direct_assign)
        self.assertEqual(prop_invalid.property_type, "INVALID_TYPE")

        # It's also good practice to check that valid enums work as expected for status
        prop_data_occupied = {
            "property_id": 6, "landlord_id": 15, "address_line_1": "Status Test St",
            "city": "State City", "county": "Progress County",
            "property_type": PropertyType.BEDSITTER,
            "num_bedrooms": 1, "num_bathrooms": 1,
            "status": PropertyStatus.OCCUPIED
        }
        prop_occupied = Property(**prop_data_occupied)
        self.assertEqual(prop_occupied.status, PropertyStatus.OCCUPIED)


if __name__ == '__main__':
    unittest.main()
