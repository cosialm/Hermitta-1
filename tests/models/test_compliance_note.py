import unittest
from datetime import datetime, date
from models.compliance_note import ComplianceNote, ComplianceArea, ComplianceStatus

class TestComplianceNote(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test ComplianceNote instantiation with only required fields."""
        now = datetime.utcnow()
        note = ComplianceNote(
            note_id=1,
            area_of_system=ComplianceArea.DPA_DATA_SECURITY,
            kenyan_regulation_reference="Data Protection Act, 2019",
            system_implication_notes="System must ensure data encryption at rest and in transit."
        )

        self.assertEqual(note.note_id, 1)
        self.assertEqual(note.area_of_system, ComplianceArea.DPA_DATA_SECURITY)
        self.assertIsInstance(note.area_of_system, ComplianceArea)
        self.assertEqual(note.kenyan_regulation_reference, "Data Protection Act, 2019")
        self.assertEqual(note.system_implication_notes, "System must ensure data encryption at rest and in transit.")

        # Check defaults
        self.assertEqual(note.status, ComplianceStatus.IDENTIFIED)
        self.assertIsInstance(note.status, ComplianceStatus)
        self.assertEqual(note.system_components_affected, []) # Default empty list
        self.assertIsInstance(note.system_components_affected, list)

        self.assertIsNone(note.specific_section_clause)
        self.assertIsNone(note.action_taken_summary)
        self.assertIsNone(note.assigned_to_user_id)
        self.assertIsNone(note.next_review_date)

        self.assertIsInstance(note.last_reviewed_at, datetime)
        self.assertIsInstance(note.created_at, datetime)
        self.assertIsInstance(note.updated_at, datetime)

        # Check if timestamps are close to 'now' (within a few seconds)
        self.assertTrue((note.last_reviewed_at - now).total_seconds() < 5)
        self.assertTrue((note.created_at - now).total_seconds() < 5)
        self.assertTrue((note.updated_at - now).total_seconds() < 5)
        self.assertTrue(note.updated_at >= note.created_at)

    def test_instantiation_with_all_fields(self):
        """Test ComplianceNote instantiation with all fields provided."""
        specific_components = ["Auth API", "User Database"]
        created_ts = datetime(2023, 1, 1, 10, 0, 0)
        updated_ts = datetime(2023, 1, 15, 11, 0, 0)
        last_reviewed_ts = datetime(2023, 1, 10, 9, 0, 0)
        next_review_dt = date(2024, 1, 10)

        note = ComplianceNote(
            note_id=2,
            area_of_system=ComplianceArea.TENANCY_SECURITY_DEPOSIT_RULES,
            kenyan_regulation_reference="Rent Restriction Act",
            specific_section_clause="Section 5",
            system_components_affected=specific_components,
            system_implication_notes="Security deposit handling logic needs update.",
            action_taken_summary="Scheduled for review with legal.",
            status=ComplianceStatus.UNDER_REVIEW,
            assigned_to_user_id=101,
            last_reviewed_at=last_reviewed_ts,
            next_review_date=next_review_dt,
            created_at=created_ts,
            updated_at=updated_ts
        )

        self.assertEqual(note.note_id, 2)
        self.assertEqual(note.area_of_system, ComplianceArea.TENANCY_SECURITY_DEPOSIT_RULES)
        self.assertEqual(note.kenyan_regulation_reference, "Rent Restriction Act")
        self.assertEqual(note.specific_section_clause, "Section 5")
        self.assertEqual(note.system_components_affected, specific_components)
        self.assertEqual(note.system_implication_notes, "Security deposit handling logic needs update.")
        self.assertEqual(note.action_taken_summary, "Scheduled for review with legal.")
        self.assertEqual(note.status, ComplianceStatus.UNDER_REVIEW)
        self.assertEqual(note.assigned_to_user_id, 101)
        self.assertEqual(note.last_reviewed_at, last_reviewed_ts)
        self.assertEqual(note.next_review_date, next_review_dt)
        self.assertIsInstance(note.next_review_date, date)
        self.assertEqual(note.created_at, created_ts)
        self.assertEqual(note.updated_at, updated_ts)

    def test_system_components_affected_defaults_to_empty_list(self):
        """Test that system_components_affected defaults to an empty list if None is passed."""
        note1 = ComplianceNote(
            note_id=3, area_of_system=ComplianceArea.SYSTEM_OTHER,
            kenyan_regulation_reference="N/A", system_implication_notes="Test note 1",
            system_components_affected=None # Explicitly pass None
        )
        self.assertEqual(note1.system_components_affected, [])
        self.assertIsInstance(note1.system_components_affected, list)

        note2 = ComplianceNote(
            note_id=4, area_of_system=ComplianceArea.SYSTEM_OTHER,
            kenyan_regulation_reference="N/A", system_implication_notes="Test note 2"
            # system_components_affected is omitted, should also default to []
        )
        self.assertEqual(note2.system_components_affected, [])
        self.assertIsInstance(note2.system_components_affected, list)

    def test_enum_and_datetime_field_types(self):
        """Test types of enum, date, and datetime fields."""
        custom_datetime = datetime(2023, 5, 5, 5, 5, 5)
        custom_date = date(2024, 5, 5)

        note = ComplianceNote(
            note_id=5,
            area_of_system=ComplianceArea.DPA_CONSENT_MANAGEMENT,
            kenyan_regulation_reference="DPA 2019",
            system_implication_notes="Consent flow.",
            status=ComplianceStatus.IMPLEMENTED,
            last_reviewed_at=custom_datetime,
            next_review_date=custom_date,
            created_at=custom_datetime,
            updated_at=custom_datetime
        )
        self.assertIsInstance(note.area_of_system, ComplianceArea)
        self.assertIsInstance(note.status, ComplianceStatus)
        self.assertIsInstance(note.last_reviewed_at, datetime)
        self.assertIsInstance(note.next_review_date, date)
        self.assertIsInstance(note.created_at, datetime)
        self.assertIsInstance(note.updated_at, datetime)

if __name__ == '__main__':
    unittest.main()
