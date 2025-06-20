import unittest
from datetime import datetime
from models.landlord_syndication_setting import LandlordSyndicationSetting

class TestLandlordSyndicationSetting(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test LandlordSyndicationSetting instantiation with only required fields."""
        now = datetime.utcnow()
        setting = LandlordSyndicationSetting(
            setting_id=1,
            landlord_id=101,
            platform_id=1 # e.g., Property24
        )

        self.assertEqual(setting.setting_id, 1)
        self.assertEqual(setting.landlord_id, 101)
        self.assertEqual(setting.platform_id, 1)

        # Check defaults
        self.assertFalse(setting.auto_syndicate_new_listings) # Default False
        self.assertTrue(setting.is_enabled_by_landlord)    # Default True
        self.assertIsInstance(setting.created_at, datetime)
        self.assertIsInstance(setting.updated_at, datetime)
        self.assertTrue((setting.created_at - now).total_seconds() < 5)
        self.assertTrue((setting.updated_at - now).total_seconds() < 5)

        # Check other optionals are None
        self.assertIsNone(setting.api_key_encrypted)
        self.assertIsNone(setting.platform_account_id)
        self.assertIsNone(setting.last_successful_sync_at)
        self.assertIsNone(setting.sync_status_message)

    def test_instantiation_with_all_fields(self):
        """Test LandlordSyndicationSetting instantiation with all fields provided."""
        created_ts = datetime(2023, 1, 1, 9, 0, 0)
        updated_ts = datetime(2023, 1, 2, 10, 0, 0)
        last_sync_ts = datetime(2023, 1, 15, 14, 0, 0)

        setting = LandlordSyndicationSetting(
            setting_id=2,
            landlord_id=102,
            platform_id=2, # e.g., Jumia House
            api_key_encrypted="super_secret_encrypted_key",
            platform_account_id="landlord123_on_jumia",
            auto_syndicate_new_listings=True,
            is_enabled_by_landlord=False,
            last_successful_sync_at=last_sync_ts,
            sync_status_message="Authentication successful, last sync OK.",
            created_at=created_ts,
            updated_at=updated_ts
        )

        self.assertEqual(setting.setting_id, 2)
        self.assertEqual(setting.landlord_id, 102)
        self.assertEqual(setting.platform_id, 2)
        self.assertEqual(setting.api_key_encrypted, "super_secret_encrypted_key")
        self.assertEqual(setting.platform_account_id, "landlord123_on_jumia")
        self.assertTrue(setting.auto_syndicate_new_listings)
        self.assertFalse(setting.is_enabled_by_landlord)
        self.assertEqual(setting.last_successful_sync_at, last_sync_ts)
        self.assertIsInstance(setting.last_successful_sync_at, datetime)
        self.assertEqual(setting.sync_status_message, "Authentication successful, last sync OK.")
        self.assertEqual(setting.created_at, created_ts)
        self.assertEqual(setting.updated_at, updated_ts)

    def test_boolean_flag_defaults_and_settings(self):
        """Test the default values and setting of boolean flags."""
        # Defaults checked in test_instantiation_with_required_fields

        # Test setting to non-defaults
        setting_true_false = LandlordSyndicationSetting(1,1,1, auto_syndicate_new_listings=True, is_enabled_by_landlord=False)
        self.assertTrue(setting_true_false.auto_syndicate_new_listings)
        self.assertFalse(setting_true_false.is_enabled_by_landlord)

        setting_false_true = LandlordSyndicationSetting(2,1,1, auto_syndicate_new_listings=False, is_enabled_by_landlord=True)
        self.assertFalse(setting_false_true.auto_syndicate_new_listings)
        self.assertTrue(setting_false_true.is_enabled_by_landlord)

    def test_get_api_key_method(self):
        """Test the get_api_key method."""
        key_val = "encrypted_data_here"
        setting_with_key = LandlordSyndicationSetting(
            setting_id=3, landlord_id=103, platform_id=3,
            api_key_encrypted=key_val
        )
        self.assertEqual(setting_with_key.get_api_key(), key_val)

        setting_without_key = LandlordSyndicationSetting(
            setting_id=4, landlord_id=104, platform_id=4
        )
        self.assertIsNone(setting_without_key.get_api_key())

    def test_datetime_field_types(self):
        """Test types of datetime fields."""
        setting_default_time = LandlordSyndicationSetting(5,1,1)
        self.assertIsInstance(setting_default_time.created_at, datetime)
        self.assertIsInstance(setting_default_time.updated_at, datetime)
        self.assertIsNone(setting_default_time.last_successful_sync_at)

        custom_time = datetime(2023, 5, 5, 5, 5, 5)
        setting_with_sync_time = LandlordSyndicationSetting(
            6,1,1, last_successful_sync_at=custom_time
        )
        self.assertIsInstance(setting_with_sync_time.last_successful_sync_at, datetime)
        self.assertEqual(setting_with_sync_time.last_successful_sync_at, custom_time)

if __name__ == '__main__':
    unittest.main()
