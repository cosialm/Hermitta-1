import unittest
from datetime import datetime
from models.syndication_platform import SyndicationPlatform

class TestSyndicationPlatform(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test SyndicationPlatform instantiation with only required fields."""
        now = datetime.utcnow()
        platform = SyndicationPlatform(
            platform_id=1,
            name="Example Listing Site"
        )

        self.assertEqual(platform.platform_id, 1)
        self.assertEqual(platform.name, "Example Listing Site")

        # Check defaults
        self.assertIsNone(platform.website_url)
        self.assertIsNone(platform.api_endpoint_url)
        self.assertIsNone(platform.data_format_required)
        self.assertEqual(platform.field_mapping_config, {})
        self.assertIsInstance(platform.field_mapping_config, dict)
        self.assertIsNone(platform.authentication_method)
        self.assertFalse(platform.requires_api_key_per_landlord) # Default False
        self.assertIsNone(platform.listing_duration_days)
        self.assertTrue(platform.is_active) # Default True
        self.assertFalse(platform.is_official_integration) # Default False
        self.assertIsNone(platform.notes_for_admin)
        self.assertIsInstance(platform.created_at, datetime)
        self.assertIsInstance(platform.updated_at, datetime)
        self.assertTrue((platform.created_at - now).total_seconds() < 5)
        self.assertTrue((platform.updated_at - now).total_seconds() < 5)

    def test_instantiation_with_all_fields(self):
        """Test SyndicationPlatform instantiation with all fields provided."""
        mapping_config_data = {"local_field": "platform_field"}
        created_ts = datetime(2023,1,1,8,0,0)
        updated_ts = datetime(2023,1,2,9,0,0)

        platform = SyndicationPlatform(
            platform_id=2,
            name="Advanced Partner Platform",
            website_url="https://advancedpartner.com",
            api_endpoint_url="https://api.advancedpartner.com/v3/listings",
            data_format_required="JSON_API_V3",
            field_mapping_config=mapping_config_data,
            authentication_method="OAUTH2_CLIENT_CREDENTIALS",
            requires_api_key_per_landlord=True,
            listing_duration_days=90,
            is_active=False, # Non-default
            is_official_integration=True, # Non-default
            notes_for_admin="Requires careful setup due to OAuth2.",
            created_at=created_ts,
            updated_at=updated_ts
        )

        self.assertEqual(platform.platform_id, 2)
        self.assertEqual(platform.name, "Advanced Partner Platform")
        self.assertEqual(platform.website_url, "https://advancedpartner.com")
        self.assertEqual(platform.api_endpoint_url, "https://api.advancedpartner.com/v3/listings")
        self.assertEqual(platform.data_format_required, "JSON_API_V3")
        self.assertEqual(platform.field_mapping_config, mapping_config_data)
        self.assertEqual(platform.authentication_method, "OAUTH2_CLIENT_CREDENTIALS")
        self.assertTrue(platform.requires_api_key_per_landlord)
        self.assertEqual(platform.listing_duration_days, 90)
        self.assertFalse(platform.is_active)
        self.assertTrue(platform.is_official_integration)
        self.assertEqual(platform.notes_for_admin, "Requires careful setup due to OAuth2.")
        self.assertEqual(platform.created_at, created_ts)
        self.assertEqual(platform.updated_at, updated_ts)

    def test_boolean_flag_defaults_and_settings(self):
        """Test default values and setting of boolean flags."""
        # Defaults checked in test_instantiation_with_required_fields

        # Test setting to non-defaults
        p_true_false_true = SyndicationPlatform(3, "P1", requires_api_key_per_landlord=True, is_active=False, is_official_integration=True)
        self.assertTrue(p_true_false_true.requires_api_key_per_landlord)
        self.assertFalse(p_true_false_true.is_active)
        self.assertTrue(p_true_false_true.is_official_integration)

        p_false_true_false = SyndicationPlatform(4, "P2", requires_api_key_per_landlord=False, is_active=True, is_official_integration=False)
        self.assertFalse(p_false_true_false.requires_api_key_per_landlord)
        self.assertTrue(p_false_true_false.is_active)
        self.assertFalse(p_false_true_false.is_official_integration)

    def test_field_mapping_config_default(self):
        """Test that field_mapping_config defaults to an empty dict."""
        platform1 = SyndicationPlatform(platform_id=5, name="TestPlatform1", field_mapping_config=None)
        self.assertEqual(platform1.field_mapping_config, {})
        self.assertIsInstance(platform1.field_mapping_config, dict)

        platform2 = SyndicationPlatform(platform_id=6, name="TestPlatform2") # Omitted
        self.assertEqual(platform2.field_mapping_config, {})
        self.assertIsInstance(platform2.field_mapping_config, dict)

if __name__ == '__main__':
    unittest.main()
