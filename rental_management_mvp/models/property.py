from enum import Enum
from datetime import datetime
from typing import List, Optional, Any # Using Any for JSON (amenities)

# Refined for Phase 1 MVP
class PropertyType(Enum):
    APARTMENT_UNIT = "APARTMENT_UNIT" # A unit within a larger apartment block
    BEDSITTER = "BEDSITTER"
    SINGLE_ROOM = "SINGLE_ROOM"
    STUDIO_APARTMENT = "STUDIO_APARTMENT" # Often similar to bedsitter but can be more distinct
    TOWNHOUSE = "TOWNHOUSE"
    MAISONETTE = "MAISONETTE"
    BUNGALOW = "BUNGALOW"
    OWN_COMPOUND_HOUSE = "OWN_COMPOUND_HOUSE"
    COMMERCIAL_PROPERTY = "COMMERCIAL_PROPERTY"
    # Add other types as needed

class PropertyStatus(Enum):
    VACANT = "VACANT"
    OCCUPIED = "OCCUPIED"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"

# Example Kenyan Amenities (can be stored in a JSON field or a Text Array)
# These are illustrative; the actual storage in `amenities` field would be a list of strings.
KENYAN_AMENITIES_EXAMPLES = [
    "BOREHOLE_WATER", "BACKUP_GENERATOR", "PERIMETER_WALL", "ELECTRIC_FENCE",
    "SECURITY_GUARD", "CCTV_SURVEILLANCE", "DSTV_READY", "ZUKU_FIBER_READY",
    "SAFINET_FIBER_READY", "AMPLE_PARKING", "CHILDREN_PLAY_AREA", "SWIMMING_POOL",
    "GYM", "SOLAR_WATER_HEATING"
]

class Property:
    def __init__(self,
                 property_id: int,
                 landlord_id: int, # Foreign Key to User
                 address_line_1: str, # Street address or plot number
                 city: str, # Major town/city, e.g., Nairobi, Mombasa
                 county: str, # Indexed, e.g., Nairobi County
                 estate_neighborhood: Optional[str] = None, # Indexed, e.g., Kilimani, Nyali
                 ward: Optional[str] = None, # Optional, Indexed
                 sub_county: Optional[str] = None, # Optional, Indexed
                 address_line_2: Optional[str] = None, # Apt number, floor, building name
                 postal_code: Optional[str] = None,
                 property_type: PropertyType,
                 num_bedrooms: int, # Use 0 for bedsitters/single rooms where not applicable
                 num_bathrooms: int,
                 size_sqft: Optional[int] = None,
                 amenities: Optional[List[str]] = None, # Flexible list of text strings
                 photos_urls: Optional[List[str]] = None, # List of URLs to images
                 main_photo_url: Optional[str] = None, # Primary photo for the property
                 description: Optional[str] = None, # Detailed description
                 status: PropertyStatus = PropertyStatus.VACANT,
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.property_id = property_id
        self.landlord_id = landlord_id
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city # E.g., Nairobi
        self.county = county # E.g., Nairobi County
        self.sub_county = sub_county # E.g., Westlands
        self.ward = ward # E.g., Parklands/Highridge
        self.estate_neighborhood = estate_neighborhood # E.g., Lavington
        self.postal_code = postal_code

        self.property_type = property_type
        self.num_bedrooms = num_bedrooms
        self.num_bathrooms = num_bathrooms
        self.size_sqft = size_sqft

        self.amenities = amenities if amenities is not None else []
        self.photos_urls = photos_urls if photos_urls is not None else []
        self.main_photo_url = main_photo_url

        self.description = description
        self.status = status

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage (Refined Phase 1):
# nairobi_apartment = Property(
#     property_id=1, landlord_id=1, address_line_1="Argwings Kodhek Rd", city="Nairobi",
#     county="Nairobi County", estate_neighborhood="Hurlingham", ward="Valley Arcade",
#     address_line_2="Apartment C5, Block C", property_type=PropertyType.APARTMENT_UNIT,
#     num_bedrooms=2, num_bathrooms=2, size_sqft=1200,
#     amenities=["BOREHOLE_WATER", "ELECTRIC_FENCE", "AMPLE_PARKING", "INTERNET_READY"],
#     main_photo_url="https://example.com/photos/apt_c5_main.jpg",
#     photos_urls=["https://example.com/photos/apt_c5_1.jpg", "https://example.com/photos/apt_c5_2.jpg"],
#     description="Spacious 2-bedroom apartment in Hurlingham with modern finishes.",
#     status=PropertyStatus.VACANT
# )
# print(nairobi_apartment.county, nairobi_apartment.property_type, nairobi_apartment.amenities)
