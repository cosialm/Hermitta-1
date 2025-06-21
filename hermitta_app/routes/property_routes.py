from flask import Blueprint, request, jsonify
from services.property_service import PropertyService
from models.property import PropertyType, PropertyStatus # For input validation
from decimal import Decimal # For handling decimal fields if any in request
from enum import Enum # For generic Enum type check

property_bp = Blueprint('property_bp', __name__, url_prefix='/api/v1/properties')
property_service = PropertyService()

@property_bp.route('', methods=['POST'])
def create_property_route():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    required_fields = ['landlord_id', 'address_line_1', 'city', 'county', 'property_type', 'num_bedrooms', 'num_bathrooms']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required field: {field}"}), 400

    try:
        # PropertyService's _prepare_property_data handles enum conversion
        new_property = property_service.create_property(property_data=data)
        prop_dict = {column.name: getattr(new_property, column.name) for column in new_property.__table__.columns}

        # Convert Enums and Decimals to string for JSON
        for key, value in prop_dict.items():
            if isinstance(value, Enum):
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
def get_property_route(property_id: int):
    prop = property_service.get_property_by_id(property_id)
    if prop:
        prop_dict = {column.name: getattr(prop, column.name) for column in prop.__table__.columns}
        # Convert Enums and Decimals to string for JSON
        for key, value in prop_dict.items():
            if isinstance(value, Enum):
                prop_dict[key] = value.value
            elif isinstance(value, Decimal):
                prop_dict[key] = str(value)
        return jsonify(prop_dict), 200
    return jsonify({"message": "Property not found"}), 404

@property_bp.route('/landlord/<int:landlord_id>', methods=['GET'])
def get_properties_by_landlord_route(landlord_id: int):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        properties, total_items = property_service.get_properties_by_landlord(landlord_id, page, per_page)

        results = []
        for prop in properties:
            prop_dict = {column.name: getattr(prop, column.name) for column in prop.__table__.columns}
            for key, value in prop_dict.items():
                if isinstance(value, Enum):
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
        # Log error e
        return jsonify({"message": "An error occurred while fetching properties."}), 500
