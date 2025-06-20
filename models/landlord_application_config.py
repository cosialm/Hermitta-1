from datetime import datetime
from typing import Optional, List, Dict, Any # For JSON field
from decimal import Decimal # Moved import to top

class LandlordApplicationConfig:
    def __init__(self,
                 config_id: int,
                 landlord_id: int, # Foreign Key to User (Landlord)
                 # Custom field definitions for the rental application form
                 # Example: [{"name": "reason_for_moving", "label": "Reason for Moving", "type": "TEXTAREA", "required": true, "options": []},
                 #           {"name": "number_of_pets", "label": "Number of Pets", "type": "NUMBER", "required": false, "min": 0},
                 #           {"name": "preferred_move_in_flexibility", "label": "Move-in Date Flexibility", "type": "SELECT",
                 #            "required": true, "options": ["Not Flexible", "Within 1 Week", "Within 2 Weeks"]}]
                 custom_field_definitions: Optional[List[Dict[str, Any]]] = None,
                 # Standard sections to include/require, e.g., employment, references
                 # require_employment_history: bool = True,
                 # require_rental_history: bool = True,
                 # require_references: bool = True,
                 application_fee: Optional[Decimal] = None, # Default application fee for this landlord
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.config_id = config_id
        self.landlord_id = landlord_id # Usually a One-to-One with Landlord User or a default system config
        self.custom_field_definitions = custom_field_definitions if custom_field_definitions is not None else []
        # self.require_employment_history = require_employment_history
        # self.require_rental_history = require_rental_history
        # self.require_references = require_references
        self.application_fee = application_fee # Landlord can set a default fee
        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# config_data_example = [
#     {"name": "current_employer", "label": "Current Employer Name", "type": "TEXT", "required": True},
#     {"name": "current_role", "label": "Current Role/Position", "type": "TEXT", "required": True},
#     {"name": "employment_duration_months", "label": "Duration at Current Role (months)", "type": "NUMBER", "required": True},
#     {"name": "previous_landlord_name", "label": "Previous Landlord Name", "type": "TEXT", "required": False},
#     {"name": "previous_landlord_phone", "label": "Previous Landlord Phone", "type": "PHONE", "required": False},
# ]
#
# landlord_app_config = LandlordApplicationConfig(
#     config_id=1, landlord_id=10,
#     custom_field_definitions=config_data_example,
#     application_fee=Decimal("50.00") # Example fee in KES or other currency
# )
#
# # To use this, the RentalApplication.custom_fields_data would store answers against the 'name' from these definitions.
# # e.g., {"current_employer": "ABC Corp", "current_role": "Software Engineer", ...}
#
# print(landlord_app_config.landlord_id, landlord_app_config.custom_field_definitions[0]['label'])

# Need to import Decimal for the application_fee
# from decimal import Decimal # Removed from here
