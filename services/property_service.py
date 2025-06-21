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
        prepared_data = self._prepare_property_data(property_data)
        # Geocoding for latitude/longitude would happen here or be triggered before this call.
        # For now, assume lat/long are provided if available.
        new_property = Property(**prepared_data)
        db.session.add(new_property)
        db.session.commit()
        return new_property

    def get_property_by_id(self, property_id: int) -> Optional[Property]:
        """
        Retrieves a property by its ID.
        """
        return Property.query.get(property_id)

    def update_property(self, property_id: int, update_data: Dict[str, Any]) -> Optional[Property]:
        """
        Updates an existing property.
        """
        property_to_update = self.get_property_by_id(property_id)
        if property_to_update:
            prepared_data = self._prepare_property_data(update_data)
            # If address fields change, geocoding should be re-triggered.
            for key, value in prepared_data.items():
                if hasattr(property_to_update, key):
                    setattr(property_to_update, key, value)
            db.session.commit()
            return property_to_update
        return None

    def delete_property(self, property_id: int) -> bool:
        """
        Deletes a property by its ID.
        TODO: Consider implications like active leases before deleting.
        """
        property_to_delete = self.get_property_by_id(property_id)
        if property_to_delete:
            # Add checks here: e.g., if property has active leases, prevent deletion or handle accordingly.
            # if property_to_delete.leases.filter_by(status='ACTIVE').count() > 0: # Example check
            #     raise ValueError("Cannot delete property with active leases.")
            db.session.delete(property_to_delete)
            db.session.commit()
            return True
        return False

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
        return self.update_property(property_id, data)


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
