import enum
from datetime import datetime
from typing import List, Optional, Any # Keep for type hinting
from hermitta_app import db # Import db instance

# Refined for Phase 1 MVP (with unit_number based on Design Review)
class PropertyType(enum.Enum):
    APARTMENT_UNIT = "APARTMENT_UNIT"
    BEDSITTER = "BEDSITTER"
    SINGLE_ROOM = "SINGLE_ROOM"
    STUDIO_APARTMENT = "STUDIO_APARTMENT"
    TOWNHOUSE = "TOWNHOUSE"
    MAISONETTE = "MAISONETTE"
    BUNGALOW = "BUNGALOW"
    OWN_COMPOUND_HOUSE = "OWN_COMPOUND_HOUSE"
    COMMERCIAL_PROPERTY = "COMMERCIAL_PROPERTY"

class PropertyStatus(enum.Enum):
    VACANT = "VACANT"
    OCCUPIED = "OCCUPIED"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"

class Property(db.Model):
    __tablename__ = 'properties'

    property_id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)

    address_line_1 = db.Column(db.String(255), nullable=False) # Street or building name
    city = db.Column(db.String(100), nullable=False, index=True)
    county = db.Column(db.String(100), nullable=False, index=True)

    property_type = db.Column(db.Enum(PropertyType), nullable=False)
    num_bedrooms = db.Column(db.Integer, nullable=False, default=0)
    num_bathrooms = db.Column(db.Integer, nullable=False, default=0)

    unit_number = db.Column(db.String(50), nullable=True, index=True) # e.g., "A5", "Unit 102", "Shop 3"
    unit_name = db.Column(db.String(100), nullable=True, index=True) # e.g. "Penthouse A", "Ground Floor Shop"
    building_name = db.Column(db.String(100), nullable=True, index=True) # e.g. "Sunrise Tower", "Westwood Mall"
    estate_neighborhood = db.Column(db.String(100), nullable=True, index=True)
    ward = db.Column(db.String(100), nullable=True, index=True)
    sub_county = db.Column(db.String(100), nullable=True, index=True)
    address_line_2 = db.Column(db.String(255), nullable=True) # Further address details
    postal_code = db.Column(db.String(20), nullable=True)

    size_sqft = db.Column(db.Integer, nullable=True)
    amenities = db.Column(db.JSON, nullable=True) # List of strings
    photos_urls = db.Column(db.JSON, nullable=True) # List of URLs
    main_photo_url = db.Column(db.String(512), nullable=True)
    description = db.Column(db.Text, nullable=True)

    status = db.Column(db.Enum(PropertyStatus), default=PropertyStatus.VACANT, nullable=False)

    latitude = db.Column(db.Float, nullable=True)  # For map integration
    longitude = db.Column(db.Float, nullable=True) # For map integration

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to User (Landlord)
    landlord = db.relationship('User', backref=db.backref('properties', lazy=True))

    # Relationship to Leases
    # leases = db.relationship('Lease', backref='property', lazy='dynamic', foreign_keys='Lease.property_id')

    # Relationship to MaintenanceRequests
    # maintenance_requests = db.relationship('MaintenanceRequest', backref='property', lazy='dynamic', foreign_keys='MaintenanceRequest.property_id')


    # __init__ is handled by db.Model
    # Geocoding logic for latitude/longitude would typically be in the service layer.

    def __repr__(self):
        parts = [f"<Property {self.property_id}: {self.address_line_1}"]
        if self.building_name:
            parts.append(f"Building: {self.building_name}")
        if self.unit_name:
            parts.append(f"Unit Name: {self.unit_name}")
        if self.unit_number: # Retaining unit_number for backward compatibility or specific use cases
            parts.append(f"Unit No: {self.unit_number}")
        parts.append(f"({self.property_type.value})>")
        return ", ".join(parts)

# Example Usage (Refined Phase 1 with unit_number)
# This would now be done via db.session.add()
# apt_A5_data = {
#     "landlord_id": 1, "address_line_1": "Sunshine Apartments, Ngong Road",
#     "unit_number": "A5", "city": "Nairobi", "county": "Nairobi County",
#     "property_type": PropertyType.APARTMENT_UNIT, "num_bedrooms": 2, "num_bathrooms": 2
# }
# apt_A5 = Property(**apt_A5_data)
# # db.session.add(apt_A5)
#
# shop_3_data = {
#     "landlord_id": 1, "address_line_1": "Busy Mall, Moi Avenue",
#     "unit_number": "Shop G3", "city": "Nairobi", "county": "Nairobi County",
#     "property_type": PropertyType.COMMERCIAL_PROPERTY, "num_bedrooms": 0, "num_bathrooms": 1
# }
# shop_3 = Property(**shop_3_data)
# # db.session.add(shop_3)
# # db.session.commit()
# # print(apt_A5.address_line_1, apt_A5.unit_number)
