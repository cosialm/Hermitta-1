from enum import Enum
from datetime import datetime
from typing import Optional

class MaintenanceAttachmentFileType(Enum):
    IMAGE = "IMAGE"     # e.g., JPG, PNG of the issue or completed work
    VIDEO = "VIDEO"     # e.g., MP4 showing the issue
    DOCUMENT = "DOCUMENT" # e.g., PDF invoice from vendor, warranty document
    AUDIO = "AUDIO"       # e.g., Voice note describing the issue
    OTHER = "OTHER"

class MaintenanceAttachment:
    def __init__(self,
                 attachment_id: int,
                 maintenance_request_id: int, # Foreign Key to MaintenanceRequest
                 uploader_user_id: int, # Foreign Key to User (Tenant, Landlord, Staff, or Vendor)
                 file_url: str, # URL to the stored file
                 file_name: str, # Original file name
                 file_type: MaintenanceAttachmentFileType,
                 description: Optional[str] = None, # Optional caption or description for the attachment
                 file_mime_type: Optional[str] = None,
                 file_size_bytes: Optional[int] = None,
                 uploaded_at: datetime = datetime.utcnow()):

        self.attachment_id = attachment_id
        self.maintenance_request_id = maintenance_request_id
        self.uploader_user_id = uploader_user_id
        self.file_url = file_url
        self.file_name = file_name
        self.file_type = file_type
        self.description = description
        self.file_mime_type = file_mime_type
        self.file_size_bytes = file_size_bytes
        self.uploaded_at = uploaded_at

# Example Usage:
# image_of_leak = MaintenanceAttachment(
#     attachment_id=1, maintenance_request_id=501, uploader_user_id=201, # Tenant uploaded
#     file_url="https://storage.example.com/maintenance/req501/leak_photo1.jpg",
#     file_name="leak_photo1.jpg",
#     file_type=MaintenanceAttachmentFileType.IMAGE,
#     description="Photo of the ceiling leak in the living room.",
#     file_mime_type="image/jpeg"
# )
#
# vendor_invoice_pdf = MaintenanceAttachment(
#     attachment_id=2, maintenance_request_id=501, uploader_user_id=301, # Vendor or Landlord uploaded
#     file_url="https://storage.example.com/maintenance/req501/vendor_invoice_plumbing.pdf",
#     file_name="plumbing_invoice_ABX_corp.pdf",
#     file_type=MaintenanceAttachmentFileType.DOCUMENT,
#     description="Invoice from ABX Plumbing for fixing the leak.",
#     file_mime_type="application/pdf"
# )
# print(image_of_leak.file_name, image_of_leak.file_type)
