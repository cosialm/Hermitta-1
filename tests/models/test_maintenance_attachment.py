import unittest
from datetime import datetime
from models.maintenance_attachment import MaintenanceAttachment, MaintenanceAttachmentFileType

class TestMaintenanceAttachment(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test MaintenanceAttachment instantiation with only required fields."""
        now = datetime.utcnow()
        attachment = MaintenanceAttachment(
            attachment_id=1,
            maintenance_request_id=101,
            uploader_user_id=201,
            file_url="https://example.com/path/to/image.jpg",
            file_name="image.jpg",
            file_type=MaintenanceAttachmentFileType.IMAGE
        )

        self.assertEqual(attachment.attachment_id, 1)
        self.assertEqual(attachment.maintenance_request_id, 101)
        self.assertEqual(attachment.uploader_user_id, 201)
        self.assertEqual(attachment.file_url, "https://example.com/path/to/image.jpg")
        self.assertEqual(attachment.file_name, "image.jpg")
        self.assertEqual(attachment.file_type, MaintenanceAttachmentFileType.IMAGE)
        self.assertIsInstance(attachment.file_type, MaintenanceAttachmentFileType)

        # Check defaults
        self.assertIsInstance(attachment.uploaded_at, datetime)
        self.assertTrue((attachment.uploaded_at - now).total_seconds() < 5)

        # Check other optionals are None
        self.assertIsNone(attachment.description)
        self.assertIsNone(attachment.file_mime_type)
        self.assertIsNone(attachment.file_size_bytes)

    def test_instantiation_with_all_fields(self):
        """Test MaintenanceAttachment instantiation with all fields provided."""
        custom_uploaded_at = datetime(2023, 1, 1, 10, 0, 0)
        attachment = MaintenanceAttachment(
            attachment_id=2,
            maintenance_request_id=102,
            uploader_user_id=202,
            file_url="https://example.com/path/to/invoice.pdf",
            file_name="invoice.pdf",
            file_type=MaintenanceAttachmentFileType.DOCUMENT,
            description="Invoice for plumbing work.",
            file_mime_type="application/pdf",
            file_size_bytes=102400, # 100KB
            uploaded_at=custom_uploaded_at
        )

        self.assertEqual(attachment.attachment_id, 2)
        self.assertEqual(attachment.maintenance_request_id, 102)
        self.assertEqual(attachment.uploader_user_id, 202)
        self.assertEqual(attachment.file_url, "https://example.com/path/to/invoice.pdf")
        self.assertEqual(attachment.file_name, "invoice.pdf")
        self.assertEqual(attachment.file_type, MaintenanceAttachmentFileType.DOCUMENT)
        self.assertEqual(attachment.description, "Invoice for plumbing work.")
        self.assertEqual(attachment.file_mime_type, "application/pdf")
        self.assertEqual(attachment.file_size_bytes, 102400)
        self.assertEqual(attachment.uploaded_at, custom_uploaded_at)
        self.assertIsInstance(attachment.uploaded_at, datetime)

    def test_enum_and_datetime_types(self):
        """Test types of enum and datetime fields."""
        attachment_image = MaintenanceAttachment(
            attachment_id=3, maintenance_request_id=103, uploader_user_id=203,
            file_url="url1", file_name="file1.png", file_type=MaintenanceAttachmentFileType.IMAGE
        )
        self.assertIsInstance(attachment_image.file_type, MaintenanceAttachmentFileType)
        self.assertIsInstance(attachment_image.uploaded_at, datetime)

        attachment_doc = MaintenanceAttachment(
            attachment_id=4, maintenance_request_id=104, uploader_user_id=204,
            file_url="url2", file_name="file2.mp4", file_type=MaintenanceAttachmentFileType.VIDEO,
            uploaded_at=datetime(2022, 12, 25, 8, 30, 0)
        )
        self.assertIsInstance(attachment_doc.file_type, MaintenanceAttachmentFileType)
        self.assertIsInstance(attachment_doc.uploaded_at, datetime)

if __name__ == '__main__':
    unittest.main()
