import enum
from datetime import datetime, date
from typing import Optional, List # Keep for type hinting
from decimal import Decimal
from hermitta_app import db # Import db instance

# Phase 6: Advanced Integrations & Scalability (Builds on Phase 3 state)
class MaintenanceRequestStatus(enum.Enum): # Refined for Vendor Portal workflow
    SUBMITTED_BY_TENANT = "SUBMITTED_BY_TENANT"
    ACKNOWLEDGED_BY_LANDLORD = "ACKNOWLEDGED_BY_LANDLORD"
    PENDING_VENDOR_ASSIGNMENT = "PENDING_VENDOR_ASSIGNMENT"
    AWAITING_VENDOR_ACCEPTANCE = "AWAITING_VENDOR_ACCEPTANCE"
    VENDOR_ACCEPTED = "VENDOR_ACCEPTED"
    VENDOR_REJECTED = "VENDOR_REJECTED"
    AWAITING_QUOTE_SUBMISSION = "AWAITING_QUOTE_SUBMISSION"
    QUOTE_SUBMITTED_BY_VENDOR = "QUOTE_SUBMITTED_BY_VENDOR"
    QUOTE_APPROVED_BY_LANDLORD = "QUOTE_APPROVED_BY_LANDLORD"
    QUOTE_REJECTED_BY_LANDLORD = "QUOTE_REJECTED_BY_LANDLORD"
    WORK_SCHEDULED = "WORK_SCHEDULED"
    WORK_IN_PROGRESS = "WORK_IN_PROGRESS"
    WORK_PAUSED_AWAITING_PARTS = "WORK_PAUSED_AWAITING_PARTS"
    WORK_COMPLETED_BY_VENDOR = "WORK_COMPLETED_BY_VENDOR"
    PENDING_LANDLORD_STAFF_VERIFICATION = "PENDING_LANDLORD_STAFF_VERIFICATION"
    PENDING_TENANT_CONFIRMATION = "PENDING_TENANT_CONFIRMATION"
    COMPLETED_CONFIRMED = "COMPLETED_CONFIRMED" # Corrected typo from CONFIRMRD
    INVOICE_SUBMITTED_BY_VENDOR = "INVOICE_SUBMITTED_BY_VENDOR"
    PAYMENT_PROCESSING_FOR_INVOICE = "PAYMENT_PROCESSING_FOR_INVOICE"
    CLOSED_COMPLETED = "CLOSED_COMPLETED"
    CLOSED_CANCELLED = "CLOSED_CANCELLED"
    CLOSED_REJECTED_BY_LANDLORD = "CLOSED_REJECTED_BY_LANDLORD"

class MaintenanceRequestCategory(enum.Enum): # From Phase 1/3
    PLUMBING = "PLUMBING"
    ELECTRICAL = "ELECTRICAL"
    APPLIANCE_REPAIR = "APPLIANCE_REPAIR"
    STRUCTURAL_ISSUE = "STRUCTURAL_ISSUE"
    PEST_CONTROL = "PEST_CONTROL"
    HVAC = "HVAC"
    PAINTING = "PAINTING"
    LANDSCAPING_GARDENING = "LANDSCAPING_GARDENING"
    COMMON_AREA = "COMMON_AREA"
    OTHER = "OTHER"

class MaintenancePriority(enum.Enum): # From Phase 3
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class MaintenanceRequest(db.Model):
    __tablename__ = 'maintenance_requests'

    request_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'), nullable=False, index=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.Enum(MaintenanceRequestCategory), nullable=False)

    tenant_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True, index=True) # Optional if created by Landlord/Staff
    priority = db.Column(db.Enum(MaintenancePriority), default=MaintenancePriority.MEDIUM, nullable=False)
    status = db.Column(db.Enum(MaintenanceRequestStatus), default=MaintenanceRequestStatus.SUBMITTED_BY_TENANT, nullable=False, index=True)

    tenant_contact_preference = db.Column(db.String(255), nullable=True)
    initial_photo_urls = db.Column(db.JSON, nullable=True) # List of strings

    assigned_to_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True, index=True) # Staff or Vendor
    assigned_vendor_name_manual = db.Column(db.String(100), nullable=True) # If vendor not a system user

    vendor_assigned_at = db.Column(db.DateTime, nullable=True) # Date primary vendor was assigned
    scheduled_date = db.Column(db.Date, nullable=True) # Overall scheduled date

    resolution_notes = db.Column(db.Text, nullable=True)
    actual_cost = db.Column(db.Numeric(10, 2), nullable=True)

    tenant_feedback_rating = db.Column(db.Integer, nullable=True) # e.g., 1-5 stars
    tenant_feedback_comment = db.Column(db.Text, nullable=True)
    resolved_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True, index=True) # User who performed final resolution

    # TODO: quote_id will be FK to Quote.quote_id when that model is defined
    quote_id = db.Column(db.Integer, nullable=True, index=True)
    # TODO: vendor_invoice_id will be FK to VendorInvoice.vendor_invoice_id when that model is defined
    vendor_invoice_id = db.Column(db.Integer, nullable=True, index=True)

    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    acknowledged_at = db.Column(db.DateTime, nullable=True)
    vendor_accepted_at = db.Column(db.DateTime, nullable=True)
    quote_approved_at = db.Column(db.DateTime, nullable=True)
    work_started_at = db.Column(db.DateTime, nullable=True)
    work_completed_at = db.Column(db.DateTime, nullable=True)
    tenant_confirmed_at = db.Column(db.DateTime, nullable=True)
    invoice_submitted_at = db.Column(db.DateTime, nullable=True)
    closed_at = db.Column(db.DateTime, nullable=True)

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    property = db.relationship('Property', backref=db.backref('maintenance_requests', lazy='dynamic'))
    creator_user = db.relationship('User', foreign_keys=[created_by_user_id], backref=db.backref('created_maintenance_requests', lazy='dynamic'))
    tenant_user = db.relationship('User', foreign_keys=[tenant_id], backref=db.backref('reported_maintenance_requests', lazy='dynamic'))
    assigned_user = db.relationship('User', foreign_keys=[assigned_to_user_id], backref=db.backref('assigned_maintenance_tasks', lazy='dynamic'))
    resolver_user = db.relationship('User', foreign_keys=[resolved_by_user_id], backref=db.backref('resolved_maintenance_tasks', lazy='dynamic'))

    # TODO: Add relationships for quote, vendor_invoice when those models are converted.
    # Relationship to FinancialTransactions (e.g., repair costs)
    # financial_transactions = db.relationship('FinancialTransaction', backref='maintenance_request', lazy='dynamic', foreign_keys='FinancialTransaction.maintenance_request_id')

    def __repr__(self):
        return f"<MaintenanceRequest {self.request_id} for Property {self.property_id} ({self.status.value})>"

# Example Usage (Phase 6) - This would now be done via db.session.add()
# req_data = {
#     "property_id": 1, "created_by_user_id": 2, "tenant_id": 2,
#     "description": "No water in bathroom.", "category": MaintenanceRequestCategory.PLUMBING,
#     "status": MaintenanceRequestStatus.ACKNOWLEDGED_BY_LANDLORD,
#     "assigned_to_user_id": 3 # Vendor user
# }
# req_p6 = MaintenanceRequest(**req_data)
# # db.session.add(req_p6)
# # db.session.commit()
# # print(req_p6.description, req_p6.status)
