import enum
from datetime import datetime, date
from typing import Optional, List, Dict, Any # Keep for type hinting
from decimal import Decimal
from hermitta_app import db # Import db instance

class LeaseSigningStatus(enum.Enum): # From Phase 3
    NOT_STARTED = "NOT_STARTED"
    DRAFT = "DRAFT"
    SENT_FOR_SIGNATURE = "SENT_FOR_SIGNATURE"
    PARTIALLY_SIGNED = "PARTIALLY_SIGNED"
    FULLY_SIGNED_SYSTEM = "FULLY_SIGNED_SYSTEM"
    FULLY_SIGNED_UPLOADED = "FULLY_SIGNED_UPLOADED"
    DECLINED = "DECLINED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    SUPERSEDED = "SUPERSEDED"

# New Enum for overall Lease Status
class LeaseStatusType(enum.Enum):
    DRAFT = "DRAFT"                             # Lease is being prepared, not yet active for signing or occupancy
    PENDING_SIGNATURES = "PENDING_SIGNATURES"   # Sent for signature, or signatures being collected
    ACTIVE_PENDING_MOVE_IN = "ACTIVE_PENDING_MOVE_IN" # Signed, tenant has not yet moved in (start_date might be future)
    ACTIVE = "ACTIVE"                           # Lease is current, tenant has moved in or start_date has passed
    EXPIRED_PENDING_RENEWAL = "EXPIRED_PENDING_RENEWAL" # End date passed, awaiting renewal decision/action
    EXPIRED = "EXPIRED"                         # End date passed, tenant moved out or no renewal
    TERMINATED_EARLY = "TERMINATED_EARLY"       # Lease ended before original end_date by agreement or other cause
    CANCELLED = "CANCELLED"                     # Lease was cancelled before it became active (e.g., during draft/pending signature)
    RENEWED = "RENEWED"                         # This specific lease instance has been superseded by a new renewal lease record
    # Note: `signing_status` tracks the e-signature process; `status` tracks overall lifecycle.

class Lease(db.Model):
    __tablename__ = 'leases'

    lease_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'), nullable=False, index=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True) # Landlord who owns the lease
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True, index=True) # Tenant associated

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    rent_amount = db.Column(db.Numeric(10, 2), nullable=False) # Assuming max 9,999,999.99
    rent_due_day = db.Column(db.Integer, nullable=False) # Day of the month rent is due
    move_in_date = db.Column(db.Date, nullable=False)

    status = db.Column(db.Enum(LeaseStatusType), default=LeaseStatusType.DRAFT, nullable=False)
    signing_status = db.Column(db.Enum(LeaseSigningStatus), default=LeaseSigningStatus.NOT_STARTED, nullable=False)

    tenant_national_id = db.Column(db.String(30), nullable=True)
    tenant_name_manual = db.Column(db.String(100), nullable=True) # If tenant not a system user
    tenant_phone_number_manual = db.Column(db.String(20), nullable=True)
    tenant_email_manual = db.Column(db.String(120), nullable=True)

    rent_start_date = db.Column(db.Date, nullable=True) # Could be different from move_in_date
    security_deposit = db.Column(db.Numeric(10, 2), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    lease_document_url = db.Column(db.String(512), nullable=True) # URL to unsigned/draft document
    lease_document_version = db.Column(db.Integer, default=1, nullable=False)
    lease_document_uploaded_at = db.Column(db.DateTime, nullable=True)
    lease_document_uploaded_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True) # User who uploaded draft

    generated_from_template_id = db.Column(db.Integer, nullable=True) # FK to a potential LeaseTemplate model
    lease_document_content_final = db.Column(db.Text, nullable=True) # Final HTML/text content for e-signature

    signature_requests = db.Column(db.JSON, nullable=True) # List of dicts: {signer_role, email, name, status, signed_at, provider_envelope_id}

    signed_lease_document_id = db.Column(db.Integer, nullable=True) # FK to a Document model for the final signed PDF
    additional_signed_document_ids = db.Column(db.JSON, nullable=True) # List of FKs to Document model

    renewal_notice_reminder_date = db.Column(db.Date, nullable=True)
    termination_notice_reminder_date = db.Column(db.Date, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    property = db.relationship('Property', backref=db.backref('leases', lazy='dynamic'))
    landlord_user = db.relationship('User', foreign_keys=[landlord_id], backref=db.backref('leases_as_landlord', lazy='dynamic'))
    tenant_user = db.relationship('User', foreign_keys=[tenant_id], backref=db.backref('leases_as_tenant', lazy='dynamic'))
    uploader_user = db.relationship('User', foreign_keys=[lease_document_uploaded_by_user_id], backref=db.backref('uploaded_lease_documents', lazy='dynamic'))

    # Relationship to FinancialTransactions (e.g., rent payments)
    # financial_transactions = db.relationship('FinancialTransaction', backref='lease', lazy='dynamic', foreign_keys='FinancialTransaction.lease_id')


    def __repr__(self):
        return f"<Lease {self.lease_id} for Property {self.property_id} (Status: {self.status.value})>"

# Example:
# This would now be done via db.session.add()
# lease_active_data = {
#     "property_id": 1, "landlord_id": 1, "tenant_id": 2,
#     "start_date": date(2024,1,1), "end_date": date(2024,12,31),
#     "rent_amount": Decimal("50000.00"), "rent_due_day": 1, "move_in_date": date(2024,1,1),
#     "status": LeaseStatusType.ACTIVE, "signing_status": LeaseSigningStatus.FULLY_SIGNED_SYSTEM
# }
# lease_active = Lease(**lease_active_data)
# # db.session.add(lease_active)
# # db.session.commit()
