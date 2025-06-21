# This file ensures that all model modules are imported,
# making them known to SQLAlchemy's metadata.
# Alembic (especially with autogenerate) relies on this metadata.

from .user import User
from .property import Property, PropertyType, PropertyStatus
from .lease import Lease, LeaseStatusType, LeaseSigningStatus # Corrected import
from .lease_template import LeaseTemplate
from .lease_amendment import LeaseAmendment
from .rental_application import RentalApplication, RentalApplicationStatus, ApplicationFeeStatus # Corrected import
from .application_document import ApplicationDocument
from .application_screening import ApplicationScreening, ScreeningStatus, ScreeningType # Corrected import
from .document import Document, DocumentType
from .document_folder import DocumentFolder
from .document_share import DocumentShare, DocumentSharePermission # Corrected import
from .financial_transaction import FinancialTransaction, FinancialTransactionType, RecurrenceFrequency
from .budget import Budget, BudgetItem, BudgetPeriodType # Corrected import
from .maintenance_request import MaintenanceRequest, MaintenancePriority, MaintenanceRequestStatus, MaintenanceRequestCategory # Corrected import
from .maintenance_attachment import MaintenanceAttachment
from .maintenance_communication import MaintenanceCommunication
from .maintenance_request_vendor_assignment import MaintenanceRequestVendorAssignment
from .quote import Quote, QuoteStatus
from .vendor_invoice import VendorInvoice, VendorInvoiceStatus # Corrected import
from .vendor_performance_rating import VendorPerformanceRating
from .landlord_bank_account import LandlordBankAccount
from .landlord_application_config import LandlordApplicationConfig
from .landlord_syndication_setting import LandlordSyndicationSetting
from .syndication_platform import SyndicationPlatform
from .syndication_log import SyndicationLog, SyndicationLogStatus, SyndicationAction # Corrected import
from .prospect_inquiry import ProspectInquiry, ProspectInquiryStatus # Corrected import
from .compliance_note import ComplianceNote, ComplianceArea, ComplianceStatus # Corrected import
from .audit_log import AuditLog
from .user_financial_category import UserFinancialCategory
from .mpesa_payment_log import MpesaPaymentLog # Assuming this is an SQLAlchemy model
# New models and enums related to Payment integration:
from .enums import (
    PaymentMethod, PaymentStatus,
    MessageType, MessageStatus,
    NotificationChannel, NotificationType, NotificationStatus as NotificationState, # Renamed to avoid clash with model
    GeneralStatus, MaintenanceRequestStatus
)
from .payment import Payment
from .gateway_transaction import GatewayTransaction, GatewayTransactionStatus, GatewayType
from .message import Message
from .notification_template import NotificationTemplate # Added for Notification models
from .notification import Notification # Added for Notification models

# It's also common to define db.Model base class here if you have a custom one,
# or re-export db from hermitta_app if models need it directly without importing hermitta_app.
# However, current models seem to import `db` from `hermitta_app` directly.

# Example of what might be needed if alembic env.py needs target_metadata directly from here:
# from hermitta_app import db
# metadata = db.metadata
# __all__ = [ model names and db or metadata ] to control `from models import *` behavior.

# For now, just importing the modules should be sufficient for SQLAlchemy to pick them up
# when the Flask app and db are initialized, as hermitta_app.db.Model is the base.
