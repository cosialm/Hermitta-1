from enum import Enum
from datetime import datetime
from typing import Optional

class MvpDocumentTypeConcept(Enum): # Renamed
    LEASE_AGREEMENT = "LEASE_AGREEMENT"
    LEASE_ADDENDUM = "LEASE_ADDENDUM"
    INSPECTION_REPORT_MOVE_IN = "INSPECTION_REPORT_MOVE_IN"
    INSPECTION_REPORT_MOVE_OUT = "INSPECTION_REPORT_MOVE_OUT"
    RENTAL_APPLICATION_FORM = "RENTAL_APPLICATION_FORM" # The submitted application itself if stored as PDF
    CREDIT_REPORT = "CREDIT_REPORT"
    BACKGROUND_CHECK_REPORT = "BACKGROUND_CHECK_REPORT"
    REFERENCE_DOCUMENT = "REFERENCE_DOCUMENT" # e.g., letter from employer
    INVOICE_VENDOR = "INVOICE_VENDOR" # For maintenance or other services
    RECEIPT_EXPENSE = "RECEIPT_EXPENSE" # For financial transactions
    RECEIPT_PAYMENT = "RECEIPT_PAYMENT" # Rent payment receipt if generated
    PROPERTY_PHOTO = "PROPERTY_PHOTO"
    MAINTENANCE_PHOTO = "MAINTENANCE_PHOTO" # Photo of issue or completed work
    INSURANCE_POLICY_PROPERTY = "INSURANCE_POLICY_PROPERTY"
    NOTICE_TO_TENANT = "NOTICE_TO_TENANT" # e.g., notice of entry, lease violation
    GENERAL_CORRESPONDENCE = "GENERAL_CORRESPONDENCE"
    OTHER = "OTHER"

class MvpDocumentConcept: # Renamed
    def __init__(self,
                 document_id: int,
                 uploader_user_id: int, # FK to User
                 document_name: str,
                 document_type: MvpDocumentTypeConcept, # Or string if more flexibility needed initially
                 file_url: str, # URL to the stored file (e.g., S3, Google Cloud Storage)
                 property_id: Optional[int] = None, # FK to Property
                 lease_id: Optional[int] = None,    # FK to Lease
                 rental_application_id: Optional[int] = None, # FK to RentalApplication
                 maintenance_request_id: Optional[int] = None, # FK to MaintenanceRequest
                 financial_transaction_id: Optional[int] = None, # FK to FinancialTransaction
                 file_mime_type: Optional[str] = None, # e.g., "application/pdf", "image/jpeg"
                 file_size_bytes: Optional[int] = None,
                 description: Optional[str] = None,
                 uploaded_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.document_id = document_id
        self.uploader_user_id = uploader_user_id

        # Contextual links
        self.property_id = property_id
        self.lease_id = lease_id
        self.rental_application_id = rental_application_id
        self.maintenance_request_id = maintenance_request_id
        self.financial_transaction_id = financial_transaction_id

        self.document_name = document_name # User-friendly name for the document
        self.document_type = document_type # Could be DocumentType(document_type).value
        self.file_url = file_url
        self.file_mime_type = file_mime_type
        self.file_size_bytes = file_size_bytes
        self.description = description
        self.uploaded_at = uploaded_at
        self.updated_at = updated_at

# Example usage:
# lease_pdf = Document(
#     document_id=1, uploader_user_id=1, # Landlord uploaded
#     document_name="Signed Lease Agreement - Apt 3B, Tenant John Doe",
#     document_type=DocumentType.LEASE_AGREEMENT,
#     file_url="https://storage.example.com/leases/lease_apt3b_johndoe.pdf",
#     lease_id=101, property_id=20,
#     file_mime_type="application/pdf", file_size_bytes=2048000,
#     description="Final signed lease agreement for John Doe, Apt 3B."
# )
#
# repair_invoice = Document(
#     document_id=2, uploader_user_id=1,
#     document_name="Invoice - Quick Plumbers Inc - Repair Apt 3B Faucet",
#     document_type=DocumentType.INVOICE_VENDOR,
#     file_url="https://storage.example.com/invoices/inv_qpi_123.pdf",
#     maintenance_request_id=55, financial_transaction_id=2, property_id=20,
#     description="Invoice for plumbing work related to maintenance request #55."
# )
# print(lease_pdf.document_name, lease_pdf.document_type)
# print(repair_invoice.document_name, repair_invoice.document_type)
