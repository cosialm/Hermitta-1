from flask import Blueprint, request, jsonify
from services.user_service import UserService
from models.user import UserRole # For potential input validation if role is string
from decimal import Decimal # For handling decimal fields if any in request

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/v1/users')
user_service = UserService()

@user_bp.route('', methods=['POST'])
def create_user_route():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    # Basic validation (can be expanded with a proper validation library like Marshmallow or Pydantic)
    required_fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required field: {field}"}), 400

    try:
        # The UserService's _prepare_user_data will handle enum conversion if role is string
        # Password will be handled by _prepare_user_data (currently stubbed as direct assignment)
        new_user = user_service.create_user(user_data=data)
        # Exclude password_hash from response for security
        user_dict = {column.name: getattr(new_user, column.name) for column in new_user.__table__.columns if column.name != 'password_hash'}
        if 'role' in user_dict and isinstance(user_dict['role'], UserRole): # Convert enum to string for JSON
            user_dict['role'] = user_dict['role'].value
        if 'preferred_login_method' in user_dict and isinstance(user_dict['preferred_login_method'], Enum):
             user_dict['preferred_login_method'] = user_dict['preferred_login_method'].value
        if 'preferred_language' in user_dict and isinstance(user_dict['preferred_language'], Enum):
             user_dict['preferred_language'] = user_dict['preferred_language'].value


        return jsonify(user_dict), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        # Log the exception e
        return jsonify({"message": "An internal error occurred"}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user_route(user_id: int):
    user = user_service.get_user_by_id(user_id)
    if user:
        # Exclude password_hash from response
        user_dict = {column.name: getattr(user, column.name) for column in user.__table__.columns if column.name != 'password_hash'}
        if 'role' in user_dict and isinstance(user_dict['role'], UserRole): # Convert enum to string for JSON
            user_dict['role'] = user_dict['role'].value
        if 'preferred_login_method' in user_dict and isinstance(user_dict['preferred_login_method'], Enum): # Assuming Enum from stdlib
             user_dict['preferred_login_method'] = user_dict['preferred_login_method'].value
        if 'preferred_language' in user_dict and isinstance(user_dict['preferred_language'], Enum): # Assuming Enum from stdlib
             user_dict['preferred_language'] = user_dict['preferred_language'].value

        # Convert Decimal to string for JSON serialization if an User model has Decimal fields
        for key, value in user_dict.items():
            if isinstance(value, Decimal):
                user_dict[key] = str(value)

        return jsonify(user_dict), 200
    return jsonify({"message": "User not found"}), 404

# Add a simple Enum import for the type check
from enum import Enum
