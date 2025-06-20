from enum import Enum
from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal

# Phase 6: Advanced Integrations & Scalability (Builds on Phase 3 state)
class MaintenanceRequestStatus(Enum): # Refined for Vendor Portal workflow
    SUBMITTED_BY_TENANT = "SUBMITTED_BY_TENANT"
    ACKNOWLEDGED_BY_LANDLORD = "ACKNOWLEDGED_BY_LANDLORD" # Landlord/Staff viewed
    PENDING_VENDOR_ASSIGNMENT = "PENDING_VENDOR_ASSIGNMENT" # Landlord to assign to a vendor
    AWAITING_VENDOR_ACCEPTANCE = "AWAITING_VENDOR_ACCEPTANCE" # Assigned, vendor needs to accept job
    VENDOR_ACCEPTED = "VENDOR_ACCEPTED"
    VENDOR_REJECTED = "VENDOR_REJECTED" # Vendor cannot take the job
    AWAITING_QUOTE_SUBMISSION = "AWAITING_QUOTE_SUBMISSION" # Vendor to submit quote
    QUOTE_SUBMITTED_BY_VENDOR = "QUOTE_SUBMITTED_BY_VENDOR"
    QUOTE_APPROVED_BY_LANDLORD = "QUOTE_APPROVED_BY_LANDLORD"
    QUOTE_REJECTED_BY_LANDLORD = "QUOTE_REJECTED_BY_LANDLORD"
    WORK_SCHEDULED = "WORK_SCHEDULED" # Date/time agreed
    WORK_IN_PROGRESS = "WORK_IN_PROGRESS"
    WORK_PAUSED_AWAITING_PARTS = "WORK_PAUSED_AWAITING_PARTS"
    WORK_COMPLETED_BY_VENDOR = "WORK_COMPLETED_BY_VENDOR" # Vendor marks as done
    PENDING_LANDLORD_STAFF_VERIFICATION = "PENDING_LANDLORD_STAFF_VERIFICATION" # Landlord/staff to check vendor's work
    PENDING_TENANT_CONFIRMATION = "PENDING_TENANT_CONFIRMATION" # Tenant to confirm resolution
    COMPLETED_CONFIRMED = "COMPLETED_CONFIRMED" # All parties agree it's done
    INVOICE_SUBMITTED_BY_VENDOR = "INVOICE_SUBMITTED_BY_VENDOR"
    PAYMENT_PROCESSING_FOR_INVOICE = "PAYMENT_PROCESSING_FOR_INVOICE"
    CLOSED_COMPLETED = "CLOSED_COMPLETED" # Final closure, payment done
    CLOSED_CANCELLED = "CLOSED_CANCELLED" # Cancelled at some point
    CLOSED_REJECTED_BY_LANDLORD = "CLOSED_REJECTED_BY_LANDLORD" # Initial request rejected

class MaintenanceRequestCategory(Enum): # From Phase 1/3
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

class MaintenancePriority(Enum): # From Phase 3
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class MaintenanceRequest:
    def __init__(self,
                 request_id: int,
                 property_id: int,
                 tenant_id: Optional[int] = None, # Optional if created by Landlord/Staff directly
                 created_by_user_id: int, # User who created the request (Tenant, Landlord, Staff)
                 description: str,
                 category: MaintenanceRequestCategory,
                 priority: MaintenancePriority = MaintenancePriority.MEDIUM,
                 status: MaintenanceRequestStatus = MaintenanceRequestStatus.SUBMITTED_BY_TENANT,
                 tenant_contact_preference: Optional[str] = None,
                 initial_photo_urls: Optional[List[str]] = None,
                 # Clarified assigned_to_user_id is for a User with VENDOR or STAFF role
                 assigned_to_user_id: Optional[int] = None, # FK to User (Staff or Vendor)
                 assigned_vendor_name_manual: Optional[str] = None, # If vendor not a system user
                 scheduled_date: Optional[date] = None,
                 resolution_notes: Optional[str] = None,
                 actual_cost: Optional[Decimal] = None,
                 tenant_feedback_rating: Optional[int] = None,
                 tenant_feedback_comment: Optional[str] = None,
                 resolved_by_user_id: Optional[int] = None, # User who performed the resolution (Staff/Vendor)
                 # Phase 6 Enhancements:
                 quote_id: Optional[int] = None, # FK to Quote model
                 vendor_invoice_id: Optional[int] = None, # FK to VendorInvoice model
                 submitted_at: datetime = datetime.utcnow(),
                 acknowledged_at: Optional[datetime] = None,
                 vendor_assigned_at: Optional[datetime] = None,
                 vendor_accepted_at: Optional[datetime] = None,
                 quote_approved_at: Optional[datetime] = None,
                 work_started_at: Optional[datetime] = None,
                 work_completed_at: Optional[datetime] = None, # When vendor/staff marks work as done
                 tenant_confirmed_at: Optional[datetime] = None, # When tenant confirms resolution
                 invoice_submitted_at: Optional[datetime] = None,
                 closed_at: Optional[datetime] = None,
                 updated_at: datetime = datetime.utcnow()
                 ):

        self.request_id = request_id
        self.property_id = property_id
        self.tenant_id = tenant_id # User who reported (if a tenant)
        self.created_by_user_id = created_by_user_id # Who actually created the record
        self.description = description
        self.category = category
        self.priority = priority
        self.status = status
        self.tenant_contact_preference = tenant_contact_preference
        self.initial_photo_urls = initial_photo_urls if initial_photo_urls is not None else []

        self.assigned_to_user_id = assigned_to_user_id
        self.assigned_vendor_name_manual = assigned_vendor_name_manual
        self.scheduled_date = scheduled_date
        self.resolution_notes = resolution_notes
        self.actual_cost = actual_cost
        self.tenant_feedback_rating = tenant_feedback_rating
        self.tenant_feedback_comment = tenant_feedback_comment
        self.resolved_by_user_id = resolved_by_user_id

        self.quote_id = quote_id
        self.vendor_invoice_id = vendor_invoice_id

        self.submitted_at = submitted_at
        self.acknowledged_at = acknowledged_at
        self.vendor_assigned_at = vendor_assigned_at
        self.vendor_accepted_at = vendor_accepted_at
        self.quote_approved_at = quote_approved_at
        self.work_started_at = work_started_at
        self.work_completed_at = work_completed_at
        self.tenant_confirmed_at = tenant_confirmed_at
        self.invoice_submitted_at = invoice_submitted_at
        self.closed_at = closed_at
        self.updated_at = updated_at

# Example Usage (Phase 6):
# req_p6 = MaintenanceRequest(request_id=4, property_id=101, tenant_id=201, created_by_user_id=201,
#                             description="No water in bathroom.", category=MaintenanceRequestCategory.PLUMBING,
#                             status=MaintenanceRequestStatus.ACKNOWLEDGED_BY_LANDLORD)
# req_p6.assigned_to_user_id = 301 # Vendor user
# req_p6.status = MaintenanceRequestStatus.AWAITING_VENDOR_ACCEPTANCE
# ...
# req_p6.quote_id = 10 # Link to submitted Quote
# req_p6.status = MaintenanceRequestStatus.QUOTE_SUBMITTED_BY_VENDOR
# ...
# req_p6.vendor_invoice_id = 20 # Link to submitted Invoice
# req_p6.status = MaintenanceRequestStatus.INVOICE_SUBMITTED_BY_VENDOR
# print(req_p6.description, req_p6.status)
