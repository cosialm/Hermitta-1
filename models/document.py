from enum import Enum
from datetime import datetime, date # Added date for expiry_date
from typing import Optional, List, Any # Added List for tags (JSON)

class DocumentType(Enum): # From initial Phase 4 outline
    LEASE_AGREEMENT = "LEASE_AGREEMENT"
    LEASE_ADDENDUM = "LEASE_ADDENDUM"
    INSPECTION_REPORT_MOVE_IN = "INSPECTION_REPORT_MOVE_IN"
    INSPECTION_REPORT_MOVE_OUT = "INSPECTION_REPORT_MOVE_OUT"
    RENTAL_APPLICATION_FORM_SUBMITTED = "RENTAL_APPLICATION_FORM_SUBMITTED" # The application PDF itself
    SCREENING_REPORT_CREDIT = "SCREENING_REPORT_CREDIT"
    SCREENING_REPORT_BACKGROUND = "SCREENING_REPORT_BACKGROUND"
    INVOICE_VENDOR = "INVOICE_VENDOR"
    RECEIPT_EXPENSE = "RECEIPT_EXPENSE" # For financial transactions (landlord expense)
    RECEIPT_PAYMENT_FROM_TENANT = "RECEIPT_PAYMENT_FROM_TENANT" # Rent payment receipt issued to tenant
    PROPERTY_PHOTO_GENERAL = "PROPERTY_PHOTO_GENERAL"
    MAINTENANCE_ISSUE_PHOTO = "MAINTENANCE_ISSUE_PHOTO"
    MAINTENANCE_COMPLETION_PHOTO = "MAINTENANCE_COMPLETION_PHOTO"
    MAINTENANCE_INVOICE_RECEIPT = "MAINTENANCE_INVOICE_RECEIPT" # From vendor for maintenance work
    INSURANCE_POLICY_PROPERTY = "INSURANCE_POLICY_PROPERTY"
    NOTICE_TO_TENANT_GENERAL = "NOTICE_TO_TENANT_GENERAL"
    TENANT_ID_DOCUMENT = "TENANT_ID_DOCUMENT" # e.g. National ID uploaded by tenant or landlord
    LANDLORD_KRA_PIN_CERT = "LANDLORD_KRA_PIN_CERT"
    OTHER = "OTHER"

class Document:
    def __init__(self,
                 document_id: int,
                 uploader_user_id: int, # FK to User (who uploaded this doc)
                 document_name: str, # User-friendly name, e.g., "Lease Agreement - John Doe - Unit 5A.pdf"
                 document_type: DocumentType,
                 file_url: str, # URL to the stored file (e.g., S3, Google Cloud Storage)
                 file_mime_type: Optional[str] = None,
                 file_size_bytes: Optional[int] = None,
                 description: Optional[str] = None, # Optional notes about the document
                 # Contextual Links (Optional Foreign Keys)
                 property_id: Optional[int] = None,
                 lease_id: Optional[int] = None,
                 rental_application_id: Optional[int] = None,
                 maintenance_request_id: Optional[int] = None,
                 financial_transaction_id: Optional[int] = None,
                 # Phase 4 Refinements:
                 folder_id: Optional[int] = None, # FK to DocumentFolder
                 tags: Optional[List[str]] = None, # e.g., ["unit-5a", "tax-2023", "invoice"]
                 expiry_date: Optional[date] = None, # For documents like insurance policies
                 reminder_date_for_expiry: Optional[date] = None, # System can notify user before expiry
                 uploaded_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.document_id = document_id
        self.uploader_user_id = uploader_user_id

        self.document_name = document_name
        self.document_type = document_type
        self.file_url = file_url
        self.file_mime_type = file_mime_type
        self.file_size_bytes = file_size_bytes
        self.description = description

        # Contextual links
        self.property_id = property_id
        self.lease_id = lease_id
        self.rental_application_id = rental_application_id
        self.maintenance_request_id = maintenance_request_id
        self.financial_transaction_id = financial_transaction_id

        # Folder, tags, expiry
        self.folder_id = folder_id
        self.tags = tags if tags is not None else []
        self.expiry_date = expiry_date
        self.reminder_date_for_expiry = reminder_date_for_expiry

        self.uploaded_at = uploaded_at
        self.updated_at = updated_at

# Example Usage:
# insurance_doc = Document(
#     document_id=1, uploader_user_id=10, # Landlord
#     document_name="Property_XYZ_Insurance_Policy_2024.pdf",
#     document_type=DocumentType.INSURANCE_POLICY_PROPERTY,
#     file_url="https://storage.example.com/docs/prop_xyz_insurance_2024.pdf",
#     property_id=101,
#     folder_id=20, # e.g., "Property XYZ/Legal Documents" folder
#     tags=["insurance", "property-xyz", "annual"],
#     expiry_date=date(2024, 12, 31),
#     reminder_date_for_expiry=date(2024, 11, 30)
# )
#
# tenant_lease_scan = Document(
#     document_id=2, uploader_user_id=10, # Landlord uploaded scanned copy
#     document_name="Signed_Lease_Unit1A_TenantJane.pdf",
#     document_type=DocumentType.LEASE_AGREEMENT,
#     file_url="...",
#     lease_id=501, property_id=102,
#     folder_id=22, tags=["lease", "unit-1a", "tenant-jane"]
# )
# print(insurance_doc.document_name, insurance_doc.tags, insurance_doc.expiry_date)
