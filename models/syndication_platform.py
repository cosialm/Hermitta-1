from datetime import datetime
from typing import Optional, Dict, Any # For JSON field_mapping_config

class SyndicationPlatform:
    def __init__(self,
                 platform_id: int,
                 name: str, # e.g., "Property24 Kenya", "Jumia House Kenya", "Generic XML Feed"
                 website_url: Optional[str] = None, # URL of the listing site
                 api_endpoint_url: Optional[str] = None, # Base URL if they have a listing API
                 data_format_required: Optional[str] = None, # e.g., "JSON_PROPERTY24_V1", "XML_CUSTOM_V2"
                 field_mapping_config: Optional[Dict[str, Any]] = None, # For data transformation
                 authentication_method: Optional[str] = None, # "OAUTH2", "API_KEY_HEADER", "NONE"
                 requires_api_key_per_landlord: bool = False,
                 listing_duration_days: Optional[int] = None,
                 is_active: bool = True, # If available for use in our system
                 is_official_integration: bool = False, # New field: True if we have a formal partnership/API agreement
                 notes_for_admin: Optional[str] = None,
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.platform_id = platform_id
        self.name = name
        self.website_url = website_url
        self.api_endpoint_url = api_endpoint_url
        self.data_format_required = data_format_required
        self.field_mapping_config = field_mapping_config if field_mapping_config is not None else {}
        self.authentication_method = authentication_method
        self.requires_api_key_per_landlord = requires_api_key_per_landlord
        self.listing_duration_days = listing_duration_days
        self.is_active = is_active
        self.is_official_integration = is_official_integration # Indicates a formal vs. best-effort integration
        self.notes_for_admin = notes_for_admin

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# official_partner_platform = SyndicationPlatform(
#     platform_id=1, name="KenyaHomesOfficial.co.ke",
#     api_endpoint_url="https://api.kenyahomesofficial.co.ke/v2/listings",
#     is_official_integration=True,
#     is_active=True
# )
#
# generic_feed = SyndicationPlatform(
#     platform_id=2, name="Generic Partner XML Feed",
#     data_format_required="XML_RENTAL_V1_EXTENDED",
#     is_official_integration=False, # We provide the feed, they consume it
#     is_active=True
# )
# print(official_partner_platform.name, official_partner_platform.is_official_integration)
