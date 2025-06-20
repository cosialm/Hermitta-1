from datetime import datetime
from typing import Optional, Dict, Any # For JSON field_mapping_config

class SyndicationPlatform:
    def __init__(self,
                 platform_id: int,
                 name: str, # e.g., "Property24 Kenya", "Jumia House Kenya", "Generic XML Feed"
                 website_url: Optional[str] = None, # URL of the listing site
                 api_endpoint_url: Optional[str] = None, # Base URL if they have a listing API
                 # Describes the format needed, e.g., "JSON_PROPERTY24_V1", "XML_CUSTOM_V2", "CSV_STANDARD"
                 data_format_required: Optional[str] = None,
                 # JSON object to map our Property model fields to their required field names/structure
                 # e.g., {"platform_field_A": "our_property_field_X", "platform_category": "our_type_mapping_func(property_type)"}
                 field_mapping_config: Optional[Dict[str, Any]] = None,
                 # Authentication method if API: "OAUTH2", "API_KEY_HEADER", "NONE"
                 authentication_method: Optional[str] = None,
                 requires_api_key_per_landlord: bool = False, # If landlords need their own API key for this platform
                 listing_duration_days: Optional[int] = None, # Default listing duration if applicable
                 is_active: bool = True, # If this platform is available for syndication in our system
                 notes_for_admin: Optional[str] = None, # Internal notes for platform management
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
        self.notes_for_admin = notes_for_admin # e.g., "Contact: person@platform.com for API issues"

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# platform_p24 = SyndicationPlatform(
#     platform_id=1, name="Property24 Kenya", website_url="https://www.property24.co.ke",
#     api_endpoint_url="https://api.property24.co.ke/listings", data_format_required="JSON_P24_V2",
#     authentication_method="API_KEY_HEADER", requires_api_key_per_landlord=True,
#     is_active=True,
#     field_mapping_config = {
#         "title": "property.public_listing_description | truncate(100)",
#         "price": "property.rent_amount_public",
#         "bedrooms": "property.num_bedrooms",
#         "property_type": "map_to_p24_type(property.property_type)"
#         # map_to_p24_type would be a conceptual function for data transformation
#     }
# )
#
# generic_xml_feed = SyndicationPlatform(
#     platform_id=2, name="Generic XML Feed for Partners",
#     data_format_required="XML_RENTAL_V1",
#     is_active=True,
#     notes_for_admin="Partners pull this feed from a specific URL on our side."
# )
# print(platform_p24.name, platform_p24.requires_api_key_per_landlord)
# print(generic_xml_feed.name, generic_xml_feed.data_format_required)
