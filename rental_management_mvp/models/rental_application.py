from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any # For JSON field

class RentalApplicationStatus(Enum):
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN" # Applicant withdrew their application

class RentalApplication:
    def __init__(self,
                 application_id: int,
                 property_id: int,
                 full_name: str,
                 email: str,
                 phone_number: str,
                 application_data: Dict[str, Any], # Stores customizable form responses
                 applicant_user_id: Optional[int] = None, # FK to User, if applicant is existing user
                 status: RentalApplicationStatus = RentalApplicationStatus.SUBMITTED,
                 submitted_at: datetime = datetime.utcnow(),
                 reviewed_at: Optional[datetime] = None,
                 notes_for_landlord: Optional[str] = None, # By applicant
                 internal_notes: Optional[str] = None, # By landlord
                 updated_at: datetime = datetime.utcnow()): # To track status changes etc.

        self.application_id = application_id
        self.property_id = property_id # Foreign Key to Property
        self.applicant_user_id = applicant_user_id # Optional Foreign Key to User

        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number

        self.application_data = application_data # JSON blob for dynamic fields
        self.status = status
        self.submitted_at = submitted_at
        self.reviewed_at = reviewed_at
        self.notes_for_landlord = notes_for_landlord
        self.internal_notes = internal_notes # For landlord's private notes
        self.updated_at = updated_at


# Example usage:
# app_data = {
#     "employment_status": "Employed",
#     "employer_name": "Tech Corp",
#     "annual_income": 80000,
#     "previous_address": "123 Old Street",
#     "references": [
#         {"name": "Jane Reference", "phone": "555-1234"},
#     ]
# }
#
# application = RentalApplication(
#     application_id=1, property_id=101, full_name="John Applicant",
#     email="john.applicant@example.com", phone_number="555-0000",
#     application_data=app_data, applicant_user_id=201
# )
# print(application.full_name, application.status, application.application_data.get("employer_name"))
