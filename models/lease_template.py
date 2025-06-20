from datetime import datetime
from typing import Optional, List, Dict, Any # For JSON content

class LeaseTemplate:
    def __init__(self,
                 template_id: int,
                 name: str,        # e.g., "Standard 12-Month Residential Lease" - Moved up (required)
                 template_content_body: str, # Moved up (required)
                 landlord_id: Optional[int] = None, # FK to User (Landlord). Null if system template.
                 description: Optional[str] = None, # Brief description of the template
                 # Main template body with placeholders like {{tenant_name}}, {{rent_amount}}, {{start_date}} etc.
                 # This could be Markdown, HTML, or plain text.
                 # For Phase 3 refinement: customizable clauses
                 # Example: [{"clause_id": "pet_policy", "title": "Pet Policy",
                 #            "text_template": "Pets are {{pets_allowed_value}}. If allowed, a pet deposit of KES {{pet_deposit_amount}} is required.",
                 #            "is_default": True, "is_editable_by_landlord": True,
                 #            "placeholders": ["pets_allowed_value", "pet_deposit_amount"] }, ...]
                 customizable_clauses_json: Optional[List[Dict[str, Any]]] = None,
                 is_system_template: bool = False, # True if it's a default platform template
                 is_default_for_landlord: bool = False, # If this is the landlord's default template
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.template_id = template_id
        self.landlord_id = landlord_id # If null, it's a system-provided template
        self.name = name
        self.description = description
        self.template_content_body = template_content_body # The main lease text with placeholders

        self.customizable_clauses_json = customizable_clauses_json if customizable_clauses_json is not None else []

        self.is_system_template = is_system_template
        self.is_default_for_landlord = is_default_for_landlord if landlord_id else False # Only applicable if landlord_id is set

        self.created_at = created_at
        self.updated_at = updated_at

# Example usage:
#
# default_pet_clause = {
#     "clause_id": "pet_policy_default",
#     "title": "Pet Policy",
#     "text_template": "No pets are allowed on the premises without prior written consent of the Landlord.",
#     "is_default": True,
#     "is_editable_by_landlord": False # System default might not be editable
# }
#
# customizable_rent_payment_clause = {
#     "clause_id": "rent_payment_instructions",
#     "title": "Rent Payment Instructions",
#     "text_template": "Rent shall be paid via {{preferred_payment_method}} to account/number {{payment_account_details}}.",
#     "is_default": False, # Landlord needs to fill this
#     "is_editable_by_landlord": True,
#     "placeholders": ["preferred_payment_method", "payment_account_details"]
# }
#
# system_lease_template = LeaseTemplate(
#     template_id=1, name="System Standard Residential Lease", is_system_template=True,
#     template_content_body="This Lease Agreement is made and entered into on {{lease_generation_date}} by and between:\n" \
#                           "Landlord: {{landlord_full_name}}\n" \
#                           "Tenant: {{tenant_full_name}}\n" \
#                           "Property: {{property_full_address}}\n" \
#                           "...\n{{custom_clauses_section}}\n...",
#     customizable_clauses_json=[default_pet_clause]
# )
#
# landlord_custom_template = LeaseTemplate(
#     template_id=2, landlord_id=10, name="My Custom Kilimani Lease",
#     template_content_body="LEASE FOR KILIMANI APARTMENTS...\n{{custom_clauses_section}}\n...",
#     customizable_clauses_json=[default_pet_clause, customizable_rent_payment_clause],
#     is_default_for_landlord=True
# )
#
# print(system_lease_template.name)
# print(landlord_custom_template.customizable_clauses_json[1]['title'])
