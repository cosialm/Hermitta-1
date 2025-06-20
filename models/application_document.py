from enum import Enum
from datetime import datetime
from typing import Optional

class ApplicationDocumentType(Enum):
    NATIONAL_ID_FRONT = "NATIONAL_ID_FRONT"
    NATIONAL_ID_BACK = "NATIONAL_ID_BACK"
    PASSPORT_BIO_PAGE = "PASSPORT_BIO_PAGE"
    PAYSLIP_MONTH_1 = "PAYSLIP_MONTH_1"
    PAYSLIP_MONTH_2 = "PAYSLIP_MONTH_2"
    PAYSLIP_MONTH_3 = "PAYSLIP_MONTH_3"
    EMPLOYMENT_LETTER = "EMPLOYMENT_LETTER"
    BANK_STATEMENT_MONTH_1 = "BANK_STATEMENT_MONTH_1"
    BANK_STATEMENT_MONTH_2 = "BANK_STATEMENT_MONTH_2"
    BANK_STATEMENT_MONTH_3 = "BANK_STATEMENT_MONTH_3"
    BUSINESS_REGISTRATION = "BUSINESS_REGISTRATION" # For self-employed
    TAX_COMPLIANCE_CERTIFICATE = "TAX_COMPLIANCE_CERTIFICATE" # Optional
    REFERENCE_LETTER = "REFERENCE_LETTER" # From previous landlord or employer
    OTHER_SUPPORTING_DOCUMENT = "OTHER_SUPPORTING_DOCUMENT"

class ApplicationDocument:
    def __init__(self,
                 app_doc_id: int,
                 application_id: int, # Foreign Key to RentalApplication
                 uploader_user_id: int, # Foreign Key to User (the applicant)
                 document_type: ApplicationDocumentType,
                 file_url: str, # URL to the stored file (e.g., S3)
                 file_name: str, # Original file name from upload
                 file_mime_type: Optional[str] = None, # e.g., "application/pdf", "image/jpeg"
                 file_size_bytes: Optional[int] = None,
                 uploaded_at: datetime = datetime.utcnow(),
                 # Optional: admin/landlord verification status for this document
                 # verification_status: Optional[str] = None, # e.g., 'PENDING_VERIFICATION', 'VERIFIED', 'REJECTED'
                 # verification_notes: Optional[str] = None
                 ):

        self.app_doc_id = app_doc_id
        self.application_id = application_id
        self.uploader_user_id = uploader_user_id # Should match RentalApplication.applicant_user_id
        self.document_type = document_type
        self.file_url = file_url
        self.file_name = file_name
        self.file_mime_type = file_mime_type
        self.file_size_bytes = file_size_bytes
        self.uploaded_at = uploaded_at

# Example Usage:
# id_doc = ApplicationDocument(
#     app_doc_id=1, application_id=101, uploader_user_id=201,
#     document_type=ApplicationDocumentType.NATIONAL_ID_FRONT,
#     file_url="https://storage.example.com/applications/app101/national_id_front.jpg",
#     file_name="national_id_front.jpg", file_mime_type="image/jpeg"
# )
#
# payslip_doc = ApplicationDocument(
#     app_doc_id=2, application_id=101, uploader_user_id=201,
#     document_type=ApplicationDocumentType.PAYSLIP_MONTH_1,
#     file_url="https://storage.example.com/applications/app101/payslip_aug.pdf",
#     file_name="payslip_aug.pdf", file_mime_type="application/pdf"
# )
# print(id_doc.document_type, id_doc.file_name)
