import enum # Standard library enum
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal
from hermitta_app import db # Import db instance
# Assuming enums are moved to models.enums or defined here if only local
# from .enums import RentalApplicationStatus, ApplicationFeeStatus

# If enums are not in models.enums, define them here:
class RentalApplicationStatus(enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    AWAITING_DOCUMENTS = "AWAITING_DOCUMENTS"
    AWAITING_FEE_PAYMENT = "AWAITING_FEE_PAYMENT"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    EXPIRED = "EXPIRED"

class ApplicationFeeStatus(enum.Enum):
    NOT_APPLICABLE = "NOT_APPLICABLE"
    PENDING = "PENDING"
    PAID = "PAID"
    WAIVED = "WAIVED"


class RentalApplication(db.Model):
    __tablename__ = 'rental_applications'

    application_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'), nullable=False, index=True)
    applicant_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True, index=True) # Optional: if applicant is existing user

    # Basic applicant info (can be pre-filled if applicant_user_id is set)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone_number = db.Column(db.String(20), nullable=False, index=True)

    # Standard application data (could be a JSON field or specific columns)
    application_data = db.Column(db.JSON, nullable=True) # Main structured data from applicant
    custom_fields_data = db.Column(db.JSON, nullable=True) # For landlord-defined questions/answers

    status = db.Column(db.Enum(RentalApplicationStatus), default=RentalApplicationStatus.DRAFT, nullable=False, index=True)
    submitted_at = db.Column(db.DateTime, nullable=True) # Set when applicant hits submit
    reviewed_at = db.Column(db.DateTime, nullable=True)

    notes_for_landlord = db.Column(db.Text, nullable=True) # By applicant
    internal_notes = db.Column(db.Text, nullable=True) # By landlord for internal review

    # Consent flags
    applicant_consent_data_processing = db.Column(db.Boolean, default=False, nullable=False)
    applicant_consent_background_check = db.Column(db.Boolean, default=False, nullable=False)

    # Application Fee
    application_fee_amount = db.Column(db.Numeric(10, 2), nullable=True) # Amount if applicable
    application_fee_paid_status = db.Column(db.Enum(ApplicationFeeStatus), default=ApplicationFeeStatus.NOT_APPLICABLE, nullable=False)
    # Link to Payment model if fee is paid through system
    # application_fee_payment_id = db.Column(db.Integer, db.ForeignKey('payments.payment_id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    property = db.relationship('Property', backref=db.backref('rental_applications', lazy='dynamic'))
    applicant = db.relationship('User', backref=db.backref('rental_applications', lazy='dynamic'))
    # documents = db.relationship('Document', backref='rental_application', lazy='dynamic') # Defined in Document model via backref
    # application_screenings = db.relationship('ApplicationScreening', backref='rental_application', lazy='dynamic') # Defined in ApplicationScreening via backref

    def __repr__(self):
        return f"<RentalApplication {self.application_id} for Property {self.property_id} by {self.full_name}>"

    # The __init__ method is largely handled by db.Model.
    # Custom logic like auto-setting submitted_at based on status on init might be better handled
    # by SQLAlchemy event listeners (e.g., before_insert, before_update) or in service layer.
    # For simplicity, if you need to retain the exact __init__ behavior for submitted_at:
    # @db.event.listens_for(RentalApplication, 'before_insert')
    # @db.event.listens_for(RentalApplication, 'before_update')
    # def auto_set_submitted_at(mapper, connection, target):
    #     if target.status == RentalApplicationStatus.SUBMITTED and target.submitted_at is None:
    #         target.submitted_at = datetime.utcnow()

    def __init__(self, **kwargs):
        # Handle application_data and custom_fields_data to default to {} if None or not present
        if kwargs.get('application_data') is None:
            kwargs['application_data'] = {}
        if kwargs.get('custom_fields_data') is None:
            kwargs['custom_fields_data'] = {}

        if 'status' not in kwargs:
            kwargs['status'] = RentalApplicationStatus.DRAFT

        if 'application_fee_paid_status' not in kwargs:
            kwargs['application_fee_paid_status'] = ApplicationFeeStatus.NOT_APPLICABLE

        if 'applicant_consent_data_processing' not in kwargs:
            kwargs['applicant_consent_data_processing'] = False
        if 'applicant_consent_background_check' not in kwargs:
            kwargs['applicant_consent_background_check'] = False

        # Conditional default for submitted_at
        current_status = kwargs.get('status', RentalApplicationStatus.DRAFT) # Use DRAFT if status also not in kwargs
        if current_status == RentalApplicationStatus.SUBMITTED and 'submitted_at' not in kwargs:
            kwargs['submitted_at'] = datetime.utcnow()

        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.utcnow()
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = datetime.utcnow()

        super().__init__(**kwargs)

# Example Usage (SQLAlchemy style):
# app_data_example = { "monthly_income": 50000, "current_employer": "Big Corp", "years_at_employer": 3 }
# custom_data_example = { "reason_for_moving": "Closer to work", "number_of_pets": 0 }
#
# application1 = RentalApplication(
#     property_id=101, full_name="Alice Applicant",
#     email="alice@example.com", phone_number="0712345001", applicant_user_id=201,
#     application_data=app_data_example, custom_fields_data=custom_data_example,
#     applicant_consent_data_processing=True, applicant_consent_background_check=True,
#     application_fee_amount=Decimal("50.00"),
#     application_fee_paid_status=ApplicationFeeStatus.PENDING,
#     status=RentalApplicationStatus.SUBMITTED # SQLAlchemy events would handle submitted_at
# )
# db.session.add(application1)
# db.session.commit() # application_id will be auto-populated
# print(application1.full_name, application1.status, application1.custom_fields_data.get("reason_for_moving"))
