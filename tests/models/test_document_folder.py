import unittest
from datetime import datetime
from models.document_folder import DocumentFolder

class TestDocumentFolder(unittest.TestCase):

    def test_instantiation_root_folder(self):
        """Test DocumentFolder instantiation for a root folder (no parent_folder_id)."""
        now = datetime.utcnow()
        folder = DocumentFolder(
            folder_id=1,
            landlord_id=101,
            name="Property Leases"
            # parent_folder_id is omitted, should default to None if model handles it,
            # or be explicitly None if required by constructor for clarity.
            # The current model's __init__ has it as an optional arg defaulting to None.
        )

        self.assertEqual(folder.folder_id, 1)
        self.assertEqual(folder.landlord_id, 101)
        self.assertEqual(folder.name, "Property Leases")
        self.assertIsNone(folder.parent_folder_id) # Default for parent_folder_id

        self.assertIsInstance(folder.created_at, datetime)
        self.assertIsInstance(folder.updated_at, datetime)
        self.assertTrue((folder.created_at - now).total_seconds() < 5)
        self.assertTrue((folder.updated_at - now).total_seconds() < 5)
        self.assertTrue(folder.updated_at >= folder.created_at)

    def test_instantiation_subfolder(self):
        """Test DocumentFolder instantiation for a subfolder (with parent_folder_id)."""
        now = datetime.utcnow()
        parent_id = 1 # Assuming folder_id=1 is a root folder
        folder = DocumentFolder(
            folder_id=2,
            landlord_id=101,
            name="Unit A Leases",
            parent_folder_id=parent_id
        )

        self.assertEqual(folder.folder_id, 2)
        self.assertEqual(folder.landlord_id, 101)
        self.assertEqual(folder.name, "Unit A Leases")
        self.assertEqual(folder.parent_folder_id, parent_id)

        self.assertIsInstance(folder.created_at, datetime)
        self.assertIsInstance(folder.updated_at, datetime)
        self.assertTrue((folder.created_at - now).total_seconds() < 5)
        self.assertTrue((folder.updated_at - now).total_seconds() < 5)

    def test_instantiation_with_explicit_timestamps(self):
        """Test DocumentFolder instantiation with explicit created_at and updated_at."""
        created_ts = datetime(2023, 1, 1, 10, 0, 0)
        updated_ts = datetime(2023, 1, 15, 11, 30, 0)

        folder = DocumentFolder(
            folder_id=3,
            landlord_id=102,
            name="Tax Documents 2023",
            parent_folder_id=None, # Explicit root folder
            created_at=created_ts,
            updated_at=updated_ts
        )

        self.assertEqual(folder.folder_id, 3)
        self.assertEqual(folder.landlord_id, 102)
        self.assertEqual(folder.name, "Tax Documents 2023")
        self.assertIsNone(folder.parent_folder_id)
        self.assertEqual(folder.created_at, created_ts)
        self.assertEqual(folder.updated_at, updated_ts)

    def test_datetime_field_types(self):
        """Test the types of datetime fields."""
        # Test with default datetime fields
        folder1 = DocumentFolder(
            folder_id=4, landlord_id=103, name="Default Time Folder"
        )
        self.assertIsInstance(folder1.created_at, datetime)
        self.assertIsInstance(folder1.updated_at, datetime)

        # Test with specified datetime fields
        custom_created_at = datetime(2023,1,1,0,0,0)
        custom_updated_at = datetime(2023,1,1,1,0,0)
        folder2 = DocumentFolder(
            folder_id=5, landlord_id=104, name="Specific Time Folder",
            created_at=custom_created_at, updated_at=custom_updated_at
        )
        self.assertEqual(folder2.created_at, custom_created_at)
        self.assertIsInstance(folder2.created_at, datetime)
        self.assertEqual(folder2.updated_at, custom_updated_at)
        self.assertIsInstance(folder2.updated_at, datetime)

    def test_parent_folder_id_can_be_none_explicitly(self):
        """Test that parent_folder_id can be explicitly set to None."""
        folder = DocumentFolder(
            folder_id=6,
            landlord_id=101,
            name="Root Folder Explicit None",
            parent_folder_id=None
        )
        self.assertIsNone(folder.parent_folder_id)

if __name__ == '__main__':
    unittest.main()
