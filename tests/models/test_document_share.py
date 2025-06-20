import unittest
from datetime import datetime, timedelta
from models.document_share import DocumentShare # DocumentSharePermission can be added if tests evolve

class TestDocumentShare(unittest.TestCase):

    def test_instantiation_with_required_fields_and_defaults(self):
        """Test DocumentShare instantiation with required fields and default permissions."""
        now = datetime.utcnow()
        share = DocumentShare(
            share_id=1,
            document_id=101,
            shared_with_user_id=201,
            shared_by_user_id=301
        )

        self.assertEqual(share.share_id, 1)
        self.assertEqual(share.document_id, 101)
        self.assertEqual(share.shared_with_user_id, 201)
        self.assertEqual(share.shared_by_user_id, 301)

        # Check default permissions and timestamp
        self.assertTrue(share.can_view)
        self.assertTrue(share.can_download)
        self.assertIsInstance(share.shared_at, datetime)
        self.assertTrue((share.shared_at - now).total_seconds() < 5)

        # Check other optionals are None
        self.assertIsNone(share.expires_at)
        self.assertIsNone(share.access_notes)

    def test_instantiation_with_all_fields(self):
        """Test DocumentShare instantiation with all fields provided."""
        custom_shared_at = datetime(2023, 1, 1, 10, 0, 0)
        custom_expires_at = datetime(2024, 1, 1, 10, 0, 0)

        share = DocumentShare(
            share_id=2,
            document_id=102,
            shared_with_user_id=202,
            shared_by_user_id=302,
            can_view=False,
            can_download=True,
            shared_at=custom_shared_at,
            expires_at=custom_expires_at,
            access_notes="Shared for review purposes only."
        )

        self.assertEqual(share.share_id, 2)
        self.assertEqual(share.document_id, 102)
        self.assertEqual(share.shared_with_user_id, 202)
        self.assertEqual(share.shared_by_user_id, 302)
        self.assertFalse(share.can_view)
        self.assertTrue(share.can_download)
        self.assertEqual(share.shared_at, custom_shared_at)
        self.assertEqual(share.expires_at, custom_expires_at)
        self.assertIsInstance(share.expires_at, datetime)
        self.assertEqual(share.access_notes, "Shared for review purposes only.")

    def test_permission_variations(self):
        """Test various combinations of permission flags."""
        share1 = DocumentShare(1, 1, 1, 1, can_view=True, can_download=True)
        self.assertTrue(share1.can_view)
        self.assertTrue(share1.can_download)

        share2 = DocumentShare(2, 1, 1, 1, can_view=False, can_download=True)
        self.assertFalse(share2.can_view)
        self.assertTrue(share2.can_download)

        share3 = DocumentShare(3, 1, 1, 1, can_view=True, can_download=False)
        self.assertTrue(share3.can_view)
        self.assertFalse(share3.can_download)

        share4 = DocumentShare(4, 1, 1, 1, can_view=False, can_download=False)
        self.assertFalse(share4.can_view)
        self.assertFalse(share4.can_download)

    def test_datetime_field_types(self):
        """Test the types of datetime fields."""
        share_default_time = DocumentShare(5,1,1,1)
        self.assertIsInstance(share_default_time.shared_at, datetime)
        self.assertIsNone(share_default_time.expires_at)

        exp_time = datetime.utcnow() + timedelta(days=30)
        share_with_expiry = DocumentShare(6,1,1,1, expires_at=exp_time)
        self.assertIsInstance(share_with_expiry.shared_at, datetime)
        self.assertIsInstance(share_with_expiry.expires_at, datetime)
        self.assertEqual(share_with_expiry.expires_at, exp_time)

    # If an is_expired() method were part of the model, it would be tested here.
    # For example:
    # def test_is_expired_logic(self):
    #     now = datetime.utcnow()
    #     share_active = DocumentShare(1,1,1,1, expires_at=now + timedelta(days=1))
    #     self.assertFalse(share_active.is_expired())
    #
    #     share_expired = DocumentShare(2,1,1,1, expires_at=now - timedelta(days=1))
    #     self.assertTrue(share_expired.is_expired())
    #
    #     share_no_expiry = DocumentShare(3,1,1,1, expires_at=None)
    #     self.assertFalse(share_no_expiry.is_expired())

if __name__ == '__main__':
    unittest.main()
