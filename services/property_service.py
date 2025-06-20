from typing import List, Optional, Dict, Any
from datetime import datetime
from models.property import Property, PropertyType, PropertyStatus # Assuming enums are also in models.property

class PropertyService:
    def __init__(self):
        self.properties: List[Property] = []
        self._next_id: int = 1

    def create_property(self, property_data: Dict[str, Any]) -> Property:
        """
        Creates a new property and stores it in memory.
        Ensures all required fields for Property model are present or defaulted.
        """
        # Ensure required fields are present, or rely on Property model's defaults/errors
        # For this stub, we assume property_data is well-formed or Property.__init__ handles it.

        new_property_id = self._next_id

        # Prepare data for Property instantiation
        # The Property model's __init__ expects specific types (e.g., enums)
        # This service method should ensure data is converted if necessary before this point,
        # but for a stub, we'll assume property_data is mostly compliant.

        # Ensure datetime fields are handled if not provided and Property model expects them
        # (Property model has defaults for created_at, updated_at)

        # Handle enums if they are passed as strings
        if 'property_type' in property_data and isinstance(property_data['property_type'], str):
            try:
                property_data['property_type'] = PropertyType[property_data['property_type']]
            except KeyError:
                raise ValueError(f"Invalid property_type: {property_data['property_type']}")

        if 'status' in property_data and isinstance(property_data['status'], str):
            try:
                property_data['status'] = PropertyStatus[property_data['status']]
            except KeyError:
                 raise ValueError(f"Invalid status: {property_data['status']}")
        elif 'status' not in property_data: # Ensure default status if not provided
            property_data['status'] = PropertyStatus.VACANT


        # Add property_id to the data
        full_property_data = {**property_data, "property_id": new_property_id}

        # Create Property instance
        # The Property model's __init__ handles created_at/updated_at defaults
        try:
            property_instance = Property(**full_property_data)
        except TypeError as e:
            # This might happen if required fields are missing and not defaulted by Property model
            raise ValueError(f"Missing required fields or incorrect data for Property creation: {e}")

        self.properties.append(property_instance)
        self._next_id += 1
        return property_instance

    def get_property(self, property_id: int) -> Optional[Property]:
        """
        Retrieves a property by its ID from the in-memory store.
        """
        for prop in self.properties:
            if prop.property_id == property_id:
                return prop
        return None

    def update_property(self, property_id: int, update_data: Dict[str, Any]) -> Optional[Property]:
        """
        Updates an existing property in the in-memory store.
        """
        property_to_update = self.get_property(property_id)
        if property_to_update:
            for key, value in update_data.items():
                # Handle enum conversion for updates as well
                if key == 'property_type' and isinstance(value, str):
                    try:
                        setattr(property_to_update, key, PropertyType[value])
                    except KeyError:
                        raise ValueError(f"Invalid property_type for update: {value}")
                elif key == 'status' and isinstance(value, str):
                    try:
                        setattr(property_to_update, key, PropertyStatus[value])
                    except KeyError:
                        raise ValueError(f"Invalid status for update: {value}")
                elif hasattr(property_to_update, key):
                    setattr(property_to_update, key, value)

            property_to_update.updated_at = datetime.utcnow()
            return property_to_update
        return None

    def delete_property(self, property_id: int) -> bool:
        """
        Deletes a property by its ID from the in-memory store.
        """
        property_to_delete = self.get_property(property_id)
        if property_to_delete:
            self.properties.remove(property_to_delete)
            return True
        return False

    def get_publicly_listed_properties(self, filters=None, sort_by=None, page=1, per_page=10):
        # Dummy implementation for tests in other modules that might import this service
        # In a real scenario, this would have complex filtering, sorting, and pagination logic.
        # For now, just return a slice of the properties list.

        # Simple status filter for 'LISTED' or 'VACANT' if PropertyStatus.VACANT is the default
        # This is a very basic interpretation of "publicly listed" for the stub.
        # A real implementation would use 'is_publicly_listed' field or more robust status checks.

        # Assuming properties are Python objects with a 'status' attribute that is PropertyStatus enum
        # and 'is_publicly_listed' boolean attribute.
        # For this stub, let's assume any 'VACANT' or 'OCCUPIED' (if that means listed sometimes) could be shown.
        # This is highly dependent on actual model and listing logic.

        # For the purpose of other tests that might use this, let's just return a slice
        # without complex filtering based on status for now.

        start_index = (page - 1) * per_page
        end_index = start_index + per_page

        # This is a placeholder. Real filtering would be complex.
        # For now, let's assume it returns all properties for simplicity of stub.
        # Or, if a 'status' filter is expected by other tests:
        # filtered_properties = self.properties
        # if filters and 'status' in filters:
        #     try:
        #         status_filter = PropertyStatus[filters['status'].upper()]
        #         filtered_properties = [p for p in self.properties if p.status == status_filter]
        #     except KeyError: # Invalid status string
        #         pass

        # Let's simplify for the stub to avoid breaking other tests that might not provide valid status strings.
        # The primary purpose here is CRUD testing of PropertyService itself.
        paginated_properties = self.properties[start_index:end_index]
        total_items = len(self.properties) # Or len(filtered_properties) if filtering applied

        return paginated_properties, total_items

    def get_property_by_id(self, property_id: int) -> Optional[Property]:
        # Alias for get_property for consistency with other service methods used in route tests
        return self.get_property(property_id)

    def get_property_by_slug(self, slug: str) -> Optional[Property]:
        # Dummy implementation for tests in other modules.
        # In a real scenario, this would search by a URL slug field on the Property model.
        # For now, just find the first property if any, or based on some other attribute if a slug exists.
        # This is a placeholder.
        if self.properties:
            # Example: if a property has a 'vacancy_listing_url_slug' attribute
            for prop in self.properties:
                if hasattr(prop, 'vacancy_listing_url_slug') and prop.vacancy_listing_url_slug == slug:
                    return prop
                # Fallback for testing if no slug attribute: find by matching description or name to slug
                if hasattr(prop, 'description') and prop.description == slug:
                    return prop
                if hasattr(prop, 'name') and prop.name == slug: # Assuming 'name' field might exist
                    return prop
        return None

    def create_property_record(self, **data) -> Property:
        # Alias for create_property for consistency with other service methods used in route tests
        return self.create_property(data)

    def update_property_record(self, property_id: int, **data) -> Optional[Property]:
        # Alias for update_property for consistency
        return self.update_property(property_id, data)

# Example Usage (not part of the class, for illustration)
if __name__ == '__main__':
    # This part is for manual testing/illustration if needed, not for unit tests
    service = PropertyService()
    sample_data_1 = {
        "landlord_id": 101,
        "address_line_1": "123 Main St",
        "city": "Anytown",
        "county": "Test County",
        "property_type": PropertyType.APARTMENT_UNIT, # Using actual enum
        "num_bedrooms": 2,
        "num_bathrooms": 1,
        "description": "A nice apartment.",
        "latitude": 1.0, # float
        "longitude": 1.0 # float
        # created_at, updated_at, status will be defaulted by Property model or service
    }
    prop1 = service.create_property(sample_data_1)
    print(f"Created Property 1: {prop1.property_id}, Status: {prop1.status.value}, Lat: {prop1.latitude}")

    sample_data_2 = {
        "landlord_id": 102,
        "address_line_1": "456 Oak Rd",
        "city": "Otherville",
        "county": "Sample County",
        "property_type": "TOWNHOUSE", # String, will be converted by service
        "num_bedrooms": 3,
        "num_bathrooms": 2,
        "status": "OCCUPIED" # String, will be converted
    }
    prop2 = service.create_property(sample_data_2)
    print(f"Created Property 2: {prop2.property_id}, Status: {prop2.status.value}")

    retrieved_prop1 = service.get_property(prop1.property_id)
    if retrieved_prop1:
        print(f"Retrieved Property 1: {retrieved_prop1.description}")

    update_for_prop1 = {"description": "An updated nice apartment.", "status": "OCCUPIED"}
    updated_prop1 = service.update_property(prop1.property_id, update_for_prop1)
    if updated_prop1:
        print(f"Updated Property 1: {updated_prop1.description}, Status: {updated_prop1.status.value}, Updated At: {updated_prop1.updated_at}")

    service.delete_property(prop2.property_id)
    print(f"Properties after deleting prop2: {[p.property_id for p in service.properties]}")

    # Test get_publicly_listed_properties
    listed_props, total = service.get_publicly_listed_properties()
    print(f"Publicly listed (stub): {[p.property_id for p in listed_props]}, Total: {total}")

    # Test get_property_by_slug (dummy)
    prop_by_slug = service.get_property_by_slug("An updated nice apartment.") # Matching description
    if prop_by_slug:
        print(f"Found by slug (description match): {prop_by_slug.property_id}")
