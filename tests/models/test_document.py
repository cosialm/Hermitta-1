import unittest
from datetime import datetime, date
from models.document import Document, DocumentType

class TestDocument(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test Document instantiation with only required fields."""
        now = datetime.utcnow()
        doc = Document(
            document_id=1,
            uploader_user_id=101,
            document_name="Lease_Agreement_Unit_1A.pdf",
            document_type=DocumentType.LEASE_AGREEMENT,
            file_url="https://example.com/docs/lease_1a.pdf"
        )

        self.assertEqual(doc.document_id, 1)
        self.assertEqual(doc.uploader_user_id, 101)
        self.assertEqual(doc.document_name, "Lease_Agreement_Unit_1A.pdf")
        self.assertEqual(doc.document_type, DocumentType.LEASE_AGREEMENT)
        self.assertIsInstance(doc.document_type, DocumentType)
        self.assertEqual(doc.file_url, "https://example.com/docs/lease_1a.pdf")

        # Check defaults
        self.assertEqual(doc.tags, [])
        self.assertIsInstance(doc.tags, list)
        self.assertIsInstance(doc.uploaded_at, datetime)
        self.assertIsInstance(doc.updated_at, datetime)
        self.assertTrue((doc.uploaded_at - now).total_seconds() < 5)
        self.assertTrue((doc.updated_at - now).total_seconds() < 5)
        self.assertTrue(doc.updated_at >= doc.uploaded_at)

        # Check other optionals are None
        self.assertIsNone(doc.file_mime_type)
        self.assertIsNone(doc.file_size_bytes)
        self.assertIsNone(doc.description)
        self.assertIsNone(doc.property_id)
        self.assertIsNone(doc.lease_id)
        self.assertIsNone(doc.rental_application_id)
        self.assertIsNone(doc.maintenance_request_id)
        self.assertIsNone(doc.financial_transaction_id)
        self.assertIsNone(doc.folder_id)
        self.assertIsNone(doc.expiry_date)
        self.assertIsNone(doc.reminder_date_for_expiry)

    def test_instantiation_with_all_fields(self):
        """Test Document instantiation with all fields provided."""
        created_ts = datetime(2023, 1, 1, 8, 0, 0)
        updated_ts = datetime(2023, 1, 2, 9, 0, 0)
        exp_date = date(2025, 12, 31)
        rem_date = date(2025, 11, 30)
        custom_tags = ["insurance", "property-x"]

        doc = Document(
            document_id=2,
            uploader_user_id=102,
            document_name="Insurance_Policy_XYZ.pdf",
            document_type=DocumentType.INSURANCE_POLICY_PROPERTY,
            file_url="https://example.com/docs/insurance_xyz.pdf",
            file_mime_type="application/pdf",
            file_size_bytes=102400, # 100KB
            description="Annual insurance policy for Property XYZ.",
            property_id=201,
            lease_id=None, # Explicitly None
            rental_application_id=None,
            maintenance_request_id=None,
            financial_transaction_id=301,
            folder_id=401,
            tags=custom_tags,
            expiry_date=exp_date,
            reminder_date_for_expiry=rem_date,
            uploaded_at=created_ts,
            updated_at=updated_ts
        )

        self.assertEqual(doc.document_id, 2)
        self.assertEqual(doc.uploader_user_id, 102)
        self.assertEqual(doc.document_name, "Insurance_Policy_XYZ.pdf")
        self.assertEqual(doc.document_type, DocumentType.INSURANCE_POLICY_PROPERTY)
        self.assertEqual(doc.file_url, "https://example.com/docs/insurance_xyz.pdf")
        self.assertEqual(doc.file_mime_type, "application/pdf")
        self.assertEqual(doc.file_size_bytes, 102400)
        self.assertEqual(doc.description, "Annual insurance policy for Property XYZ.")
        self.assertEqual(doc.property_id, 201)
        self.assertIsNone(doc.lease_id)
        self.assertEqual(doc.financial_transaction_id, 301)
        self.assertEqual(doc.folder_id, 401)
        self.assertEqual(doc.tags, custom_tags)
        self.assertEqual(doc.expiry_date, exp_date)
        self.assertIsInstance(doc.expiry_date, date)
        self.assertEqual(doc.reminder_date_for_expiry, rem_date)
        self.assertIsInstance(doc.reminder_date_for_expiry, date)
        self.assertEqual(doc.uploaded_at, created_ts)
        self.assertEqual(doc.updated_at, updated_ts)

    def test_tags_default_to_empty_list(self):
        """Test that tags defaults to an empty list if None is passed or omitted."""
        doc1 = Document(
            document_id=3, uploader_user_id=1, document_name="Doc1",
            document_type=DocumentType.OTHER, file_url="url1", tags=None
        )
        self.assertEqual(doc1.tags, [])
        self.assertIsInstance(doc1.tags, list)

        doc2 = Document(
            document_id=4, uploader_user_id=1, document_name="Doc2",
            document_type=DocumentType.OTHER, file_url="url2"
        ) # tags omitted
        self.assertEqual(doc2.tags, [])
        self.assertIsInstance(doc2.tags, list)

    def test_date_datetime_enum_types(self):
        """Test types of enum, date, and datetime fields."""
        custom_datetime = datetime(2023, 6, 6, 6, 6, 6)
        custom_date = date(2024, 6, 6)

        doc = Document(
            document_id=5,
            uploader_user_id=105,
            document_name="Type_Test_Doc.doc",
            document_type=DocumentType.TENANT_ID_DOCUMENT,
            file_url="https://example.com/types.doc",
            expiry_date=custom_date,
            reminder_date_for_expiry=custom_date,
            uploaded_at=custom_datetime,
            updated_at=custom_datetime
        )
        self.assertIsInstance(doc.document_type, DocumentType)
        self.assertIsInstance(doc.expiry_date, date)
        self.assertIsInstance(doc.reminder_date_for_expiry, date)
        self.assertIsInstance(doc.uploaded_at, datetime)
        self.assertIsInstance(doc.updated_at, datetime)

if __name__ == '__main__':
    unittest.main()
