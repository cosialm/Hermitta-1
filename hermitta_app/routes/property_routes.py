from flask import Blueprint, request, jsonify, current_app # Added current_app
from services.property_service import PropertyService
from models.property import PropertyType, PropertyStatus # For input validation
from decimal import Decimal # For handling decimal fields if any in request
from enum import Enum as PyEnum # For generic Enum type check, aliased to avoid clash if needed
from functools import wraps # For placeholder decorator

property_bp = Blueprint('property_bp', __name__, url_prefix='/api/v1/properties')
property_service = PropertyService()

# --- Placeholder Auth ---
# In a real app, this would use Flask-Login, Flask-JWT-Extended, etc.
def get_current_user_id_placeholder():
    # Simulate getting user ID, e.g., from a header or a test default
    # For testing, you might set a specific ID or get from request.
    # IMPORTANT: THIS IS NOT SECURE FOR PRODUCTION.
    user_id = request.headers.get("X-Test-User-Id")
    if user_id:
        try:
            return int(user_id)
        except ValueError:
            return None # Or raise an error
    # Fallback for testing if no header is set, DO NOT USE IN PROD
    # return 1 # Assuming user 1 is a landlord for testing
    return None # Default to no user if not provided for testing

def auth_required_placeholder(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_current_user_id_placeholder()
        if user_id is None:
            return jsonify({"message": "Authentication required"}), 401
        # Add user_id to kwargs or g for routes to use
        kwargs['current_user_id'] = user_id
        return f(*args, **kwargs)
    return decorated_function
# --- End Placeholder Auth ---


@property_bp.route('', methods=['POST'])
@auth_required_placeholder
def create_property_route(current_user_id: int): # Added current_user_id from decorator
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    # landlord_id is now from the authenticated user, not request body
    required_fields = ['address_line_1', 'city', 'county', 'property_type', 'num_bedrooms', 'num_bathrooms']
    missing_fields = [field for field in required_fields if field not in data or not data.get(field)]
    if missing_fields:
        return jsonify({"message": f"Missing or empty required fields: {', '.join(missing_fields)}"}), 400

    data['landlord_id'] = current_user_id # Set landlord_id from authenticated user

    # Add more comprehensive validation for other fields like amenities, photos_urls, etc.
    # Example:
    # if 'amenities' in data and not isinstance(data['amenities'], list):
    #     return jsonify({"message": "Amenities must be a list"}), 400
    # if 'photos_urls' in data and not isinstance(data['photos_urls'], list):
    #     return jsonify({"message": "photos_urls must be a list"}), 400


    try:
        # PropertyService's _prepare_property_data handles enum conversion
        new_property = property_service.create_property(property_data=data)
        prop_dict = {column.name: getattr(new_property, column.name) for column in new_property.__table__.columns}

        # Convert Enums and Decimals to string for JSON
        for key, value in prop_dict.items():
            if isinstance(value, PyEnum): # Use aliased PyEnum
                prop_dict[key] = value.value
            elif isinstance(value, Decimal):
                prop_dict[key] = str(value)

        return jsonify(prop_dict), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        # Log error e
        return jsonify({"message": "An internal error occurred"}), 500

@property_bp.route('/<int:property_id>', methods=['GET'])
@auth_required_placeholder
def get_property_route(current_user_id: int, property_id: int): # Added current_user_id
    # Use the service method that checks ownership
    prop = property_service.get_property_by_id_for_landlord(property_id, current_user_id)
    if prop:
        prop_dict = {column.name: getattr(prop, column.name) for column in prop.__table__.columns}
        # Convert Enums and Decimals to string for JSON
        for key, value in prop_dict.items():
            if isinstance(value, PyEnum): # Use aliased PyEnum
                prop_dict[key] = value.value
            elif isinstance(value, Decimal):
                prop_dict[key] = str(value)
        return jsonify(prop_dict), 200
    # If not found for this landlord, it's either not their property or doesn't exist
    return jsonify({"message": "Property not found or access denied"}), 404

@property_bp.route('', methods=['GET']) # Changed route from /landlord/<landlord_id>
@auth_required_placeholder
def get_properties_by_landlord_route(current_user_id: int): # Uses current_user_id
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        # Use current_user_id from auth context
        properties, total_items = property_service.get_properties_by_landlord(current_user_id, page, per_page)

        results = []
        for prop in properties:
            prop_dict = {column.name: getattr(prop, column.name) for column in prop.__table__.columns}
            for key, value in prop_dict.items():
                if isinstance(value, PyEnum): # Correctly use aliased PyEnum
                    prop_dict[key] = value.value
                elif isinstance(value, Decimal):
                    prop_dict[key] = str(value)
            results.append(prop_dict)

        return jsonify({
            "properties": results,
            "total_items": total_items,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_items + per_page - 1) // per_page
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error in get_properties_by_landlord_route: {e}", exc_info=True) # Explicit log
        return jsonify({"message": "An error occurred while fetching properties."}), 500

# --- Update Property ---
@property_bp.route('/<int:property_id>', methods=['PUT'])
@auth_required_placeholder
def update_property_route(current_user_id: int, property_id: int):
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    # Fetch property and verify ownership
    property_to_update = property_service.get_property_by_id_for_landlord(property_id, current_user_id)
    if not property_to_update:
        return jsonify({"message": "Property not found or access denied"}), 404

    # Prevent landlord_id from being changed via this route
    if 'landlord_id' in data and data['landlord_id'] != current_user_id:
        return jsonify({"message": "Cannot change landlord_id"}), 403

    # Ensure landlord_id is not accidentally removed or set to something else if not provided
    data.pop('landlord_id', None) # Remove if present, or ensure it's not in update_data if service expects it not

    try:
        updated_property = property_service.update_property(property_obj=property_to_update, update_data=data)
        prop_dict = {column.name: getattr(updated_property, column.name) for column in updated_property.__table__.columns}
        # Convert Enums and Decimals
        for key, value in prop_dict.items():
            if isinstance(value, PyEnum):
                prop_dict[key] = value.value
            elif isinstance(value, Decimal):
                prop_dict[key] = str(value)
        return jsonify(prop_dict), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        # Log error e
        return jsonify({"message": "An internal error occurred during property update"}), 500

# --- Delete Property ---
@property_bp.route('/<int:property_id>', methods=['DELETE'])
@auth_required_placeholder
def delete_property_route(current_user_id: int, property_id: int):
    # Fetch property and verify ownership
    property_to_delete = property_service.get_property_by_id_for_landlord(property_id, current_user_id)
    if not property_to_delete:
        return jsonify({"message": "Property not found or access denied"}), 404

    # Check for active leases (simplified check, a more robust check might be needed in service)
    from models.lease import Lease, LeaseStatusType # Corrected import for LeaseStatusType

    # This is a basic check. A more robust solution might involve checking LeaseStatusType.ACTIVE, etc.
    # The actual definition of "active" lease might vary.
    # Using a conceptual active status for now.
    active_leases_count = Lease.query.filter_by(property_id=property_id, status=LeaseStatusType.ACTIVE).count() # Example
    if active_leases_count > 0:
        return jsonify({"message": "Cannot delete property with active leases. Please terminate or reassign leases first."}), 409 # Conflict

    try:
        property_service.delete_property(property_obj=property_to_delete)
        return jsonify({"message": "Property deleted successfully"}), 200 # Or 204 No Content
    except ValueError as e: # Catch specific errors from service if any (like lease check if moved to service)
        return jsonify({"message": str(e)}), 409 # Conflict or Bad Request depending on error
    except Exception as e:
        # Log error e
        return jsonify({"message": "An internal error occurred during property deletion"}), 500

# --- Upload Property Photos ---
@property_bp.route('/<int:property_id>/photos', methods=['POST'])
@auth_required_placeholder
def upload_property_photos_route(current_user_id: int, property_id: int):
    # Fetch property and verify ownership
    property_to_update = property_service.get_property_by_id_for_landlord(property_id, current_user_id)
    if not property_to_update:
        return jsonify({"message": "Property not found or access denied"}), 404

    # Actual file handling (multipart/form-data) is complex and platform-dependent.
    # This is a conceptual placeholder for how one might receive photo URLs.
    # In a real app:
    # 1. Receive files via request.files.
    # 2. Save them to a configured storage (local disk, S3, etc.).
    # 3. Get the URLs of the saved files.
    # For this conceptual route, we'll assume the request body directly provides a list of new photo URLs.

    data = request.get_json()
    if not data or 'photo_urls' not in data:
        return jsonify({"message": "Missing 'photo_urls' list in request body"}), 400

    new_photo_urls = data.get('photo_urls')
    if not isinstance(new_photo_urls, list) or not all(isinstance(url, str) for url in new_photo_urls):
        return jsonify({"message": "'photo_urls' must be a list of strings"}), 400

    try:
        updated_property = property_service.add_photo_urls_to_property(
            property_obj=property_to_update,
            new_photo_urls=new_photo_urls
        )
        # Prepare response
        prop_dict = {column.name: getattr(updated_property, column.name) for column in updated_property.__table__.columns}
        for key, value in prop_dict.items():
            if isinstance(value, PyEnum):
                prop_dict[key] = value.value
            elif isinstance(value, Decimal):
                prop_dict[key] = str(value)
        return jsonify(prop_dict), 200

    except ValueError as e: # Catch errors from service like invalid input type
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        # Log error e
        return jsonify({"message": "An internal error occurred during photo upload processing"}), 500
