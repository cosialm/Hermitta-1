from typing import List, Optional, Dict, Any
from datetime import datetime
from hermitta_app import db # Import db instance
from models.property import Property, PropertyType, PropertyStatus # Import SQLAlchemy model

class PropertyService:

    def _prepare_property_data(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepares property data for creation or update, handling enums.
        """
        prepared_data = property_data.copy()
        if 'property_type' in prepared_data and isinstance(prepared_data['property_type'], str):
            try:
                prepared_data['property_type'] = PropertyType[prepared_data['property_type'].upper()]
            except KeyError:
                raise ValueError(f"Invalid property_type: {prepared_data['property_type']}")

        if 'status' in prepared_data and isinstance(prepared_data['status'], str):
            try:
                prepared_data['status'] = PropertyStatus[prepared_data['status'].upper()]
            except KeyError:
                 raise ValueError(f"Invalid status: {prepared_data['status']}")
        return prepared_data

    def create_property(self, property_data: Dict[str, Any]) -> Property:
        """
        Creates a new property.
        """
        required_fields = ['landlord_id', 'address_line_1', 'city', 'county', 'property_type', 'num_bedrooms', 'num_bathrooms']
        missing_fields = [field for field in required_fields if field not in property_data or property_data[field] is None]
        if missing_fields:
            # For num_bedrooms/num_bathrooms, 0 is a valid value, so None check is appropriate.
            # If property_type is enum, its presence is enough, _prepare_property_data handles conversion/validation.
            raise ValueError(f"Missing required fields for Property creation: {', '.join(missing_fields)}")

        prepared_data = self._prepare_property_data(property_data)
        # Geocoding for latitude/longitude would happen here or be triggered before this call.
        # For now, assume lat/long are provided if available.
        try:
            new_property = Property(**prepared_data)
            db.session.add(new_property)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error during Property creation: {e}")
        return new_property

    def get_property_by_id(self, property_id: int) -> Optional[Property]:
        """
        Retrieves a property by its ID.
        """
        return Property.query.get(property_id)

    def get_property_by_id_for_landlord(self, property_id: int, landlord_id: int) -> Optional[Property]:
        """
        Retrieves a property by its ID, ensuring it belongs to the specified landlord.
        """
        return Property.query.filter_by(property_id=property_id, landlord_id=landlord_id).first()

    def update_property(self, property_id: int, update_data: Dict[str, Any]) -> Optional[Property]:
        """
        Updates an existing property.
        """
        property_obj = self.get_property_by_id(property_id)
        if not property_obj:
            return None

        prepared_data = self._prepare_property_data(update_data)
        for key, value in prepared_data.items():
            if hasattr(property_obj, key):
                setattr(property_obj, key, value)

        try:
            db.session.add(property_obj) # Re-attach if it was detached, or ensure it's dirty
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # Consider more specific error handling or logging
            raise ValueError(f"Error during Property update: {e}")
        return property_obj

    def delete_property(self, property_id: int) -> bool:
        """
        Deletes a property by its ID.
        """
        property_obj = self.get_property_by_id(property_id)
        if not property_obj:
            return False

        # Add checks here: e.g., if property has active leases, prevent deletion or handle accordingly.
        # from models.lease import Lease, LeaseStatusType # Import inside or at top
        # active_leases = Lease.query.filter_by(property_id=property_obj.property_id, status=LeaseStatusType.ACTIVE).count()
        # if active_leases > 0:
        #     raise ValueError("Cannot delete property with active leases.")
        try:
            db.session.delete(property_obj)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            # Consider more specific error handling or logging
            raise ValueError(f"Error during Property deletion: {e}")
        return False # Should not be reached if exception is raised

    def get_properties_by_landlord(self, landlord_id: int, page: int = 1, per_page: int = 10) -> (List[Property], int):
        """
        Retrieves properties for a given landlord with pagination.
        Returns a tuple of (properties_list, total_properties_count).
        """
        query = Property.query.filter_by(landlord_id=landlord_id)
        # Could add default ordering, e.g., query = query.order_by(Property.created_at.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total


    def get_publicly_listed_properties(self, filters: Optional[Dict[str, Any]] = None,
                                       sort_by: Optional[str] = None,
                                       page: int = 1, per_page: int = 10) -> (List[Property], int):
        """
        Retrieves publicly listed properties with filtering, sorting, and pagination.
        Returns a tuple of (properties_list, total_properties_count).
        """
        query = Property.query

        # Assuming a field `is_publicly_listed` or similar for public filtering
        # For now, let's use status as a proxy if that field isn't on the model yet.
        # query = query.filter_by(is_publicly_listed=True)
        query = query.filter_by(status=PropertyStatus.VACANT) # Example basic filter for "public"

        if filters:
            if 'city' in filters and filters['city']:
                query = query.filter(Property.city.ilike(f"%{filters['city']}%"))
            if 'county' in filters and filters['county']:
                query = query.filter(Property.county.ilike(f"%{filters['county']}%"))
            if 'property_type' in filters and filters['property_type']:
                try:
                    ptype = PropertyType[filters['property_type'].upper()]
                    query = query.filter(Property.property_type == ptype)
                except KeyError:
                    pass # Invalid property type string, ignore or raise error
            if 'min_bedrooms' in filters and filters['min_bedrooms'] is not None:
                query = query.filter(Property.num_bedrooms >= filters['min_bedrooms'])
            # Add more filters: max_bedrooms, price range (requires rent field on Property or linked Lease)

        # TODO: Implement sorting based on 'sort_by' string
        # e.g., if sort_by == "created_at_desc": query = query.order_by(Property.created_at.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total

    def get_property_by_slug(self, slug: str) -> Optional[Property]:
        """
        Placeholder for finding property by a URL slug.
        """
        # TODO: Add a 'slug' field to Property model (e.g., vacancy_listing_url_slug).
        # return Property.query.filter_by(vacancy_listing_url_slug=slug).first()
        # Fallback for now:
        return Property.query.filter(Property.address_line_1.ilike(f"%{slug.replace('-', ' ')}%")).first()


    # Aliases for route test compatibility if needed
    def create_property_record(self, **data) -> Property:
        return self.create_property(data)

    def update_property_record(self, property_id: int, **data) -> Optional[Property]:
        # This alias might need rethinking if update_property now expects an object
        # For now, let's assume it's for direct data updates if property_id is primary way to find.
        # However, the main update_property now takes an object.
        # This alias is likely from an older version of the service.
        # For consistency, routes should fetch the object, check ownership, then pass object to update_property.
        # So, this specific alias might become less relevant or need to replicate that fetch logic.
        # For now, I will comment it out as it conflicts with the refactored update_property.
        # return self.update_property(property_id, data)
        pass

    def add_photo_urls_to_property(self, property_obj: Property, new_photo_urls: List[str]) -> Property:
        """
        Adds new photo URLs to a property's photos_urls list.
        Assumes ownership check has been done by the caller.
        """
        if not isinstance(new_photo_urls, list):
            raise ValueError("new_photo_urls must be a list.")

        # Ensure photos_urls is initialized as a list
        if property_obj.photos_urls is None:
            property_obj.photos_urls = []

        for url in new_photo_urls:
            if isinstance(url, str) and url not in property_obj.photos_urls:
                property_obj.photos_urls.append(url)

        # Important for JSON field changes to be detected by SQLAlchemy
        if db.session.is_modified(property_obj):
             db.session.add(property_obj) # Re-add if modified to ensure flush captures JSON change
        else: # If only the list content changed but not the list object itself, flag manually
            from sqlalchemy.orm.attributes import flag_modified
            flag_modified(property_obj, "photos_urls")

        db.session.commit()
        return property_obj


# Example Usage (would be done in a Flask context with app and db initialized)
# if __name__ == '__main__':
#     from hermitta_app import create_app
#     # Assuming UserService is also refactored and available for creating a landlord
#     # from services.user_service import UserService
#
#     app = create_app('dev')
#     with app.app_context():
#         user_service = UserService() # Assuming it's refactored
#         property_service = PropertyService()
#
#         # Ensure a landlord user exists or create one
#         test_landlord_email = "landlord_for_prop_svc@example.com"
#         landlord = user_service.get_user_by_email(test_landlord_email)
#         if not landlord:
#             landlord = user_service.create_user({
#                 "email": test_landlord_email, "password": "securepassword123",
#                 "first_name": "Landlord", "last_name": "ForProp",
#                 "phone_number": "0711000000", "role": UserRole.LANDLORD, "kra_pin": "A000TESTKRA"
#             })
#             print(f"Created test landlord with ID: {landlord.user_id}")
#
#         sample_data = {
#             "landlord_id": landlord.user_id,
#             "address_line_1": "123 SQLAlchemy Ave",
#             "city": "ORM City",
#             "county": "Database County",
#             "property_type": PropertyType.TOWNHOUSE,
#             "num_bedrooms": 3,
#             "num_bathrooms": 2,
#             "description": "A lovely townhouse managed with SQLAlchemy.",
#             "status": PropertyStatus.VACANT,
#             "amenities": ["garden", "parking"],
#             "unit_number": "Unit 1"
#         }
#         try:
#             prop = property_service.create_property(sample_data)
#             print(f"Created Property ID: {prop.property_id}, Address: {prop.address_line_1}")
#
#             retrieved_prop = property_service.get_property_by_id(prop.property_id)
#             if retrieved_prop:
#                 print(f"Retrieved Property: {retrieved_prop.description}")
#
#                 updated_data = {"description": "An even lovelier, updated townhouse."}
#                 property_service.update_property(prop.property_id, updated_data)
#
#                 updated_retrieved_prop = property_service.get_property_by_id(prop.property_id)
#                 print(f"Updated Description: {updated_retrieved_prop.description}")
#
#             # Example of listing properties for the landlord
#             landlord_props, total = property_service.get_properties_by_landlord(landlord.user_id)
#             print(f"Landlord {landlord.user_id} has {total} properties. Page 1: {[p.property_id for p in landlord_props]}")
#
#             # Example of public listing (very basic)
#             public_props, total_public = property_service.get_publicly_listed_properties(page=1, per_page=5)
#             print(f"Total public properties (basic filter): {total_public}. Page 1: {[p.property_id for p in public_props]}")
#
#             # property_service.delete_property(prop.property_id)
#             # print(f"Property {prop.property_id} deleted status: {property_service.get_property_by_id(prop.property_id) is None}")
#
#         except Exception as e:
#             print(f"An error occurred during PropertyService example: {e}")
#             db.session.rollback()
#
#         print("PropertyService SQLAlchemy example usage complete.")
