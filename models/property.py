from enum import Enum
from datetime import datetime
from typing import List, Optional, Any

# Refined for Phase 1 MVP (with unit_number based on Design Review)
class PropertyType(Enum):
    APARTMENT_UNIT = "APARTMENT_UNIT"
    BEDSITTER = "BEDSITTER"
    SINGLE_ROOM = "SINGLE_ROOM"
    STUDIO_APARTMENT = "STUDIO_APARTMENT"
    TOWNHOUSE = "TOWNHOUSE"
    MAISONETTE = "MAISONETTE"
    BUNGALOW = "BUNGALOW"
    OWN_COMPOUND_HOUSE = "OWN_COMPOUND_HOUSE"
    COMMERCIAL_PROPERTY = "COMMERCIAL_PROPERTY"

class PropertyStatus(Enum):
    VACANT = "VACANT"
    OCCUPIED = "OCCUPIED"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"

class Property:
    def __init__(self,
                 property_id: int,
                 landlord_id: int,
                 address_line_1: str, # Street or building name
                 city: str,
                 county: str,
                 property_type: PropertyType,
                 num_bedrooms: int,
                 num_bathrooms: int,
                 unit_number: Optional[str] = None, # New field: e.g., "A5", "Unit 102", "Shop 3" (Indexed)
                 estate_neighborhood: Optional[str] = None,
                 ward: Optional[str] = None,
                 sub_county: Optional[str] = None,
                 address_line_2: Optional[str] = None, # Further address details if needed beyond unit_number
                 postal_code: Optional[str] = None,
                 size_sqft: Optional[int] = None,
                 amenities: Optional[List[str]] = None,
                 photos_urls: Optional[List[str]] = None,
                 main_photo_url: Optional[str] = None,
                 description: Optional[str] = None,
                 status: PropertyStatus = PropertyStatus.VACANT,
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.property_id = property_id
        self.landlord_id = landlord_id
        self.address_line_1 = address_line_1 # Main address (e.g., Building Name, Street)
        self.unit_number = unit_number # Specific unit identifier within the address_line_1 location
        self.address_line_2 = address_line_2 # Can be used for additional details like floor, specific block if not in unit_number

        self.city = city
        self.county = county
        self.sub_county = sub_county
        self.ward = ward
        self.estate_neighborhood = estate_neighborhood
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

# Example Usage (Refined Phase 1 with unit_number):
# apt_A5 = Property(
#     property_id=1, landlord_id=1, address_line_1="Sunshine Apartments, Ngong Road",
#     unit_number="A5", city="Nairobi", county="Nairobi County",
#     property_type=PropertyType.APARTMENT_UNIT, num_bedrooms=2, num_bathrooms=2
# )
# shop_3 = Property(
#     property_id=2, landlord_id=1, address_line_1="Busy Mall, Moi Avenue",
#     unit_number="Shop G3", city="Nairobi", county="Nairobi County",
#     property_type=PropertyType.COMMERCIAL_PROPERTY, num_bedrooms=0, num_bathrooms=1
# )
# print(apt_A5.address_line_1, apt_A5.unit_number)
