from datetime import datetime
from typing import Union, Dict, List, Any # For JSON content

class LeaseTemplate:
    def __init__(self,
                 template_id: int,
                 landlord_id: int, # Foreign Key to User (Landlord who owns this template)
                 name: str,        # e.g., "Standard 12-Month Residential Lease"
                 # content_placeholders can be a structured JSON for easier parsing and filling,
                 # or a raw text string with {{placeholder}} syntax. JSON is often more robust.
                 content_placeholders: Union[str, Dict[str, Any], List[Dict[str, Any]]],
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.template_id = template_id
        self.landlord_id = landlord_id
        self.name = name
        self.content_placeholders = content_placeholders # The template body with placeholders
        self.created_at = created_at
        self.updated_at = updated_at

# Example usage:
#
# Example 1: Simple text-based template
# template_text_content = """
# LEASE AGREEMENT
# Date: {{current_date}}
# Landlord: {{landlord_name}}
# Tenant: {{tenant_name}}
# Property: {{property_address}}
# Rent: ${{rent_amount}} per month, due on the {{rent_due_day}} of each month.
# Start Date: {{start_date}}
# End Date: {{end_date}}
# ... more clauses ...
# """
# text_template = LeaseTemplate(
#     template_id=1, landlord_id=10, name="Basic Text Lease",
#     content_placeholders=template_text_content
# )
# print(text_template.name)

# Example 2: JSON-based template (more structured)
# template_json_content = {
#     "title": "Residential Lease Agreement",
#     "sections": [
#         {"type": "header", "content": "Lease Agreement Details"},
#         {"type": "paragraph", "text": "This lease is entered into on {{current_date}}."},
#         {"type": "field", "label": "Landlord Name", "placeholder": "{{landlord_name}}"},
#         {"type": "field", "label": "Tenant Name", "placeholder": "{{tenant_name}}"},
#         {"type": "group", "title": "Rent Details", "fields": [
#             {"label": "Monthly Rent", "value": "{{rent_amount}}", "unit": "USD"},
#             {"label": "Due Day", "value": "{{rent_due_day}}"}
#         ]},
#         # ... more structured sections
#     ],
#     "signature_section": {
#         "landlord_signature_placeholder": "{{landlord_signature_space}}",
#         "tenant_signature_placeholder": "{{tenant_signature_space}}"
#     }
# }
# json_template = LeaseTemplate(
#     template_id=2, landlord_id=10, name="Structured JSON Lease",
#     content_placeholders=template_json_content
# )
# print(json_template.name)
