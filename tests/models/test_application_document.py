import unittest
from datetime import datetime
from models.application_document import ApplicationDocument, ApplicationDocumentType

class TestApplicationDocument(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test basic instantiation with only required fields."""
        now = datetime.utcnow()
        doc = ApplicationDocument(
            app_doc_id=1,
            application_id=101,
            uploader_user_id=201,
            document_type=ApplicationDocumentType.NATIONAL_ID_FRONT,
            file_url="https://example.com/id_front.jpg",
            file_name="id_front.jpg",
            # uploaded_at will be set by default
        )
        self.assertEqual(doc.app_doc_id, 1)
        self.assertEqual(doc.application_id, 101)
        self.assertEqual(doc.uploader_user_id, 201)
        self.assertEqual(doc.document_type, ApplicationDocumentType.NATIONAL_ID_FRONT)
        self.assertEqual(doc.file_url, "https://example.com/id_front.jpg")
        self.assertEqual(doc.file_name, "id_front.jpg")
        self.assertIsNone(doc.file_mime_type)
        self.assertIsNone(doc.file_size_bytes)
        self.assertIsInstance(doc.uploaded_at, datetime)
        # Check if uploaded_at is close to 'now' (within a few seconds)
        self.assertTrue((doc.uploaded_at - now).total_seconds() < 5)

    def test_instantiation_with_all_fields(self):
        """Test instantiation with all required and optional fields."""
        custom_time = datetime(2023, 1, 1, 12, 0, 0)
        doc = ApplicationDocument(
            app_doc_id=2,
            application_id=102,
            uploader_user_id=202,
            document_type=ApplicationDocumentType.PAYSLIP_MONTH_1,
            file_url="https://example.com/payslip.pdf",
            file_name="payslip.pdf",
            file_mime_type="application/pdf",
            file_size_bytes=102400, # 100KB
            uploaded_at=custom_time
        )
        self.assertEqual(doc.app_doc_id, 2)
        self.assertEqual(doc.application_id, 102)
        self.assertEqual(doc.uploader_user_id, 202)
        self.assertEqual(doc.document_type, ApplicationDocumentType.PAYSLIP_MONTH_1)
        self.assertEqual(doc.file_url, "https://example.com/payslip.pdf")
        self.assertEqual(doc.file_name, "payslip.pdf")
        self.assertEqual(doc.file_mime_type, "application/pdf")
        self.assertEqual(doc.file_size_bytes, 102400)
        self.assertEqual(doc.uploaded_at, custom_time)

    def test_document_type_is_enum_instance(self):
        """Test that document_type is an instance of ApplicationDocumentType Enum."""
        doc = ApplicationDocument(
            app_doc_id=3,
            application_id=103,
            uploader_user_id=203,
            document_type=ApplicationDocumentType.PASSPORT_BIO_PAGE,
            file_url="https://example.com/passport.png",
            file_name="passport.png"
        )
        self.assertIsInstance(doc.document_type, ApplicationDocumentType)
        self.assertEqual(doc.document_type, ApplicationDocumentType.PASSPORT_BIO_PAGE)

    def test_uploaded_at_is_datetime_instance(self):
        """Test that uploaded_at is an instance of datetime."""
        # Test with default value
        doc1 = ApplicationDocument(
            app_doc_id=4, application_id=104, uploader_user_id=204,
            document_type=ApplicationDocumentType.EMPLOYMENT_LETTER,
            file_url="https://example.com/letter.pdf", file_name="letter.pdf"
        )
        self.assertIsInstance(doc1.uploaded_at, datetime)

        # Test with provided value
        specific_time = datetime(2022, 5, 10, 10, 30, 0)
        doc2 = ApplicationDocument(
            app_doc_id=5, application_id=105, uploader_user_id=205,
            document_type=ApplicationDocumentType.BANK_STATEMENT_MONTH_1,
            file_url="https://example.com/bank.pdf", file_name="bank.pdf",
            uploaded_at=specific_time
        )
        self.assertIsInstance(doc2.uploaded_at, datetime)
        self.assertEqual(doc2.uploaded_at, specific_time)

if __name__ == '__main__':
    unittest.main()
