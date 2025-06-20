import unittest
from datetime import datetime
from decimal import Decimal
from models.landlord_application_config import LandlordApplicationConfig

class TestLandlordApplicationConfig(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test LandlordApplicationConfig instantiation with only required fields."""
        now = datetime.utcnow()
        config = LandlordApplicationConfig(
            config_id=1,
            landlord_id=101
        )

        self.assertEqual(config.config_id, 1)
        self.assertEqual(config.landlord_id, 101)

        # Check defaults
        self.assertEqual(config.custom_field_definitions, [])
        self.assertIsInstance(config.custom_field_definitions, list)
        self.assertIsNone(config.application_fee)
        self.assertIsInstance(config.created_at, datetime)
        self.assertIsInstance(config.updated_at, datetime)
        self.assertTrue((config.created_at - now).total_seconds() < 5)
        self.assertTrue((config.updated_at - now).total_seconds() < 5)

    def test_instantiation_with_all_fields(self):
        """Test LandlordApplicationConfig instantiation with all fields provided."""
        custom_fields_data = [
            {"name": "reason_for_moving", "label": "Reason for Moving", "type": "TEXTAREA", "required": True},
            {"name": "number_of_pets", "label": "Number of Pets", "type": "NUMBER", "required": False}
        ]
        app_fee = Decimal("25.00")
        created_ts = datetime(2023, 1, 1, 9, 0, 0)
        updated_ts = datetime(2023, 1, 2, 10, 0, 0)

        config = LandlordApplicationConfig(
            config_id=2,
            landlord_id=102,
            custom_field_definitions=custom_fields_data,
            application_fee=app_fee,
            created_at=created_ts,
            updated_at=updated_ts
        )

        self.assertEqual(config.config_id, 2)
        self.assertEqual(config.landlord_id, 102)
        self.assertEqual(config.custom_field_definitions, custom_fields_data)
        self.assertIsInstance(config.custom_field_definitions, list)
        self.assertEqual(config.application_fee, app_fee)
        self.assertIsInstance(config.application_fee, Decimal)
        self.assertEqual(config.created_at, created_ts)
        self.assertEqual(config.updated_at, updated_ts)

    def test_custom_field_definitions_defaults_to_empty_list(self):
        """Test that custom_field_definitions defaults to an empty list if None is passed or omitted."""
        config1 = LandlordApplicationConfig(
            config_id=3, landlord_id=103, custom_field_definitions=None
        )
        self.assertEqual(config1.custom_field_definitions, [])
        self.assertIsInstance(config1.custom_field_definitions, list)

        config2 = LandlordApplicationConfig(config_id=4, landlord_id=104) # Omitted
        self.assertEqual(config2.custom_field_definitions, [])
        self.assertIsInstance(config2.custom_field_definitions, list)

    def test_decimal_and_datetime_types(self):
        """Test types of Decimal and datetime fields."""
        config_default_fee = LandlordApplicationConfig(config_id=5, landlord_id=105)
        self.assertIsNone(config_default_fee.application_fee)
        self.assertIsInstance(config_default_fee.created_at, datetime)
        self.assertIsInstance(config_default_fee.updated_at, datetime)

        config_with_fee = LandlordApplicationConfig(
            config_id=6, landlord_id=106, application_fee=Decimal("10.50")
        )
        self.assertIsInstance(config_with_fee.application_fee, Decimal)
        self.assertEqual(config_with_fee.application_fee, Decimal("10.50"))

if __name__ == '__main__':
    unittest.main()
