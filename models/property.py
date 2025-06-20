from enum import Enum
from datetime import datetime
from typing import List, Optional, Any

# Phase 4: Enhanced for Vacancy Posting (builds on Phase 1 refined state)
class PropertyType(Enum): # From Phase 1 Refinement
    APARTMENT_UNIT = "APARTMENT_UNIT"
    BEDSITTER = "BEDSITTER"
    SINGLE_ROOM = "SINGLE_ROOM"
    STUDIO_APARTMENT = "STUDIO_APARTMENT"
    TOWNHOUSE = "TOWNHOUSE"
    MAISONETTE = "MAISONETTE"
    BUNGALOW = "BUNGALOW"
    OWN_COMPOUND_HOUSE = "OWN_COMPOUND_HOUSE"
    COMMERCIAL_PROPERTY = "COMMERCIAL_PROPERTY"

class PropertyStatus(Enum): # From Phase 1 Refinement, enhanced for Phase 4
    VACANT = "VACANT"
    OCCUPIED = "OCCUPIED"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"
    LISTED = "LISTED" # Property is vacant AND publicly advertised

class Property:
    def __init__(self,
                 property_id: int,
                 landlord_id: int,
                 address_line_1: str,
                 city: str,
                 county: str,
                 property_type: PropertyType,
                 num_bedrooms: int,
                 num_bathrooms: int,
                 estate_neighborhood: Optional[str] = None,
                 ward: Optional[str] = None,
                 sub_county: Optional[str] = None,
                 address_line_2: Optional[str] = None,
                 postal_code: Optional[str] = None,
                 size_sqft: Optional[int] = None,
                 amenities: Optional[List[str]] = None,
                 photos_urls: Optional[List[str]] = None,
                 main_photo_url: Optional[str] = None,
                 description: Optional[str] = None, # Internal description
                 status: PropertyStatus = PropertyStatus.VACANT,
                 # Vacancy Posting Fields (Phase 4 Enhancements)
                 public_listing_description: Optional[str] = None, # For public ads
                 is_publicly_listed: bool = False,
                 vacancy_listing_url_slug: Optional[str] = None, # Unique, editable slug for public URL
                 public_listing_contact_override_phone: Optional[str] = None, # If different from landlord's main phone
                 public_listing_contact_override_email: Optional[str] = None, # If different from landlord's main email
                 accepting_applications_online: bool = False, # Default to False, true when listed and ready
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.property_id = property_id
        self.landlord_id = landlord_id
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
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

        self.description = description # Landlord's internal description
        self.status = status

        # Vacancy Posting Fields
        self.public_listing_description = public_listing_description
        self.is_publicly_listed = is_publicly_listed
        self.vacancy_listing_url_slug = vacancy_listing_url_slug
        self.public_listing_contact_override_phone = public_listing_contact_override_phone
        self.public_listing_contact_override_email = public_listing_contact_override_email
        if self.is_publicly_listed: # If listed, should accept applications by default
            self.accepting_applications_online = True
            if self.status == PropertyStatus.VACANT: # Auto-update status if vacant and listed
                self.status = PropertyStatus.LISTED
        else:
            self.accepting_applications_online = False
            if self.status == PropertyStatus.LISTED: # Revert status if no longer listed
                self.status = PropertyStatus.VACANT

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage (Phase 4):
# property_for_listing = Property(
#     property_id=2, landlord_id=10, address_line_1="Beach Road", city="Mombasa", county="Mombasa",
#     property_type=PropertyType.APARTMENT_UNIT, num_bedrooms=3, num_bathrooms=2,
#     is_publicly_listed=True, vacancy_listing_url_slug="mombasa-beach-apt-3br",
#     public_listing_description="Stunning 3-bedroom apartment with ocean views. Available immediately!",
#     public_listing_contact_override_phone="+254700112233"
# )
# print(property_for_listing.vacancy_listing_url_slug, property_for_listing.status, property_for_listing.accepting_applications_online)
