from datetime import datetime
from typing import Optional

# This model stores landlord's preferences and specific credentials (if any) for each syndication platform.
class LandlordSyndicationSetting:
    def __init__(self,
                 setting_id: int,
                 landlord_id: int, # Foreign Key to User (Landlord)
                 platform_id: int, # Foreign Key to SyndicationPlatform
                 # API key for this landlord for this platform, if SyndicationPlatform.requires_api_key_per_landlord is True.
                 # Must be stored encrypted.
                 api_key_encrypted: Optional[str] = None,
                 # Landlord's specific account ID or username on the platform, if needed for posting.
                 platform_account_id: Optional[str] = None,
                 auto_syndicate_new_listings: bool = False, # Does landlord want new "publicly_listed" properties to auto-syndicate here?
                 is_enabled_by_landlord: bool = True, # Landlord can enable/disable syndication to this platform
                 last_successful_sync_at: Optional[datetime] = None, # Timestamp of last successful syndication to this platform
                 sync_status_message: Optional[str] = None, # e.g., "Active", "Authentication Failed", "Disabled by Admin"
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.setting_id = setting_id
        self.landlord_id = landlord_id
        self.platform_id = platform_id

        self.api_key_encrypted = api_key_encrypted # Store encrypted, handle decryption elsewhere
        self.platform_account_id = platform_account_id

        self.auto_syndicate_new_listings = auto_syndicate_new_listings
        self.is_enabled_by_landlord = is_enabled_by_landlord # Landlord's choice to use this platform

        self.last_successful_sync_at = last_successful_sync_at
        self.sync_status_message = sync_status_message # Provides feedback to landlord

        self.created_at = created_at
        self.updated_at = updated_at

    def get_api_key(self) -> Optional[str]:
        # TODO: Implement decryption logic if api_key_encrypted is used
        return self.api_key_encrypted

# Example Usage:
# landlord1_p24_settings = LandlordSyndicationSetting(
#     setting_id=1, landlord_id=10, platform_id=1, # Platform 1 is Property24
#     api_key_encrypted="encrypted_landlord1_p24_key",
#     platform_account_id="landlord1_agent_id_on_p24",
#     auto_syndicate_new_listings=True,
#     is_enabled_by_landlord=True
# )
#
# landlord1_jumia_settings = LandlordSyndicationSetting(
#     setting_id=2, landlord_id=10, platform_id=2, # Platform 2 is Jumia House
#     # Jumia might not require per-landlord API key if platform integrates centrally
#     auto_syndicate_new_listings=False, # Landlord chooses to manually push to Jumia
#     is_enabled_by_landlord=True
# )
# print(f"Settings for Landlord {landlord1_p24_settings.landlord_id} on Platform {landlord1_p24_settings.platform_id}")
