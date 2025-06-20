import unittest
from datetime import datetime
from models.lease_template import LeaseTemplate

class TestLeaseTemplate(unittest.TestCase):

    def test_instantiation_minimal_system_template(self):
        """Test instantiation with minimal fields, implying a system template by omitting landlord_id."""
        now = datetime.utcnow()
        template = LeaseTemplate(
            template_id=1,
            name="Basic System Template",
            template_content_body="Content: {{tenant_name}}"
            # landlord_id is None by default
            # is_system_template defaults to False, but behaviorally it's a system template if landlord_id is None
        )

        self.assertEqual(template.template_id, 1)
        self.assertIsNone(template.landlord_id)
        self.assertEqual(template.name, "Basic System Template")
        self.assertEqual(template.template_content_body, "Content: {{tenant_name}}")
        self.assertIsNone(template.description)
        self.assertEqual(template.customizable_clauses_json, [])
        self.assertIsInstance(template.customizable_clauses_json, list)
        self.assertFalse(template.is_system_template) # Explicitly False by default
        self.assertFalse(template.is_default_for_landlord) # False as landlord_id is None

        self.assertIsInstance(template.created_at, datetime)
        self.assertIsInstance(template.updated_at, datetime)
        self.assertTrue((template.created_at - now).total_seconds() < 5)

    def test_instantiation_explicit_system_template(self):
        """Test instantiation for an explicit system template."""
        clauses = [{"clause_id": "sys_clause_1", "text_template": "System clause text."}]
        template = LeaseTemplate(
            template_id=2,
            name="Official System Template",
            template_content_body="Main body for system.",
            description="A system-wide usable template.",
            customizable_clauses_json=clauses,
            is_system_template=True # Explicitly a system template
            # landlord_id remains None
        )
        self.assertTrue(template.is_system_template)
        self.assertIsNone(template.landlord_id)
        self.assertFalse(template.is_default_for_landlord) # Cannot be default for landlord if no landlord_id
        self.assertEqual(template.customizable_clauses_json, clauses)

    def test_instantiation_landlord_template(self):
        """Test instantiation for a landlord-specific template."""
        clauses_data = [{"clause_id": "landlord_clause_1", "text_template": "Landlord specific terms."}]
        created_ts = datetime(2023,1,1,8,0,0)
        updated_ts = datetime(2023,1,2,9,0,0)

        template = LeaseTemplate(
            template_id=3,
            landlord_id=101,
            name="Landlord John's Preferred Lease",
            description="Custom lease for John's properties.",
            template_content_body="Lease body by John: {{property_address}}",
            customizable_clauses_json=clauses_data,
            is_system_template=False, # Explicitly not a system template
            is_default_for_landlord=True,
            created_at=created_ts,
            updated_at=updated_ts
        )
        self.assertEqual(template.template_id, 3)
        self.assertEqual(template.landlord_id, 101)
        self.assertEqual(template.name, "Landlord John's Preferred Lease")
        self.assertEqual(template.description, "Custom lease for John's properties.")
        self.assertEqual(template.template_content_body, "Lease body by John: {{property_address}}")
        self.assertEqual(template.customizable_clauses_json, clauses_data)
        self.assertFalse(template.is_system_template)
        self.assertTrue(template.is_default_for_landlord)
        self.assertEqual(template.created_at, created_ts)
        self.assertEqual(template.updated_at, updated_ts)

    def test_is_default_for_landlord_logic(self):
        """Test the logic for is_default_for_landlord."""
        # Case 1: landlord_id is None, is_default_for_landlord passed as True (should be False)
        template1 = LeaseTemplate(
            template_id=4, name="Sys Temp Default Attempt",
            template_content_body="...", is_default_for_landlord=True
            # landlord_id is None
        )
        self.assertFalse(template1.is_default_for_landlord, "is_default_for_landlord should be False if landlord_id is None")

        # Case 2: landlord_id is set, is_default_for_landlord is True
        template2 = LeaseTemplate(
            template_id=5, landlord_id=102, name="Landlord Default True",
            template_content_body="...", is_default_for_landlord=True
        )
        self.assertTrue(template2.is_default_for_landlord)

        # Case 3: landlord_id is set, is_default_for_landlord is False
        template3 = LeaseTemplate(
            template_id=6, landlord_id=103, name="Landlord Default False",
            template_content_body="...", is_default_for_landlord=False
        )
        self.assertFalse(template3.is_default_for_landlord)

        # Case 4: landlord_id is set, is_default_for_landlord is omitted (should default to False)
        template4 = LeaseTemplate(
            template_id=7, landlord_id=104, name="Landlord Default Omitted",
            template_content_body="..."
        )
        self.assertFalse(template4.is_default_for_landlord)


    def test_customizable_clauses_json_defaults_to_empty_list(self):
        """Test that customizable_clauses_json defaults to an empty list."""
        template_no_clauses = LeaseTemplate(
            template_id=8, name="No Clauses Template", template_content_body="..."
            # customizable_clauses_json omitted
        )
        self.assertEqual(template_no_clauses.customizable_clauses_json, [])
        self.assertIsInstance(template_no_clauses.customizable_clauses_json, list)

        template_clauses_none = LeaseTemplate(
            template_id=9, name="Clauses None Template", template_content_body="...",
            customizable_clauses_json=None # Explicitly None
        )
        self.assertEqual(template_clauses_none.customizable_clauses_json, [])
        self.assertIsInstance(template_clauses_none.customizable_clauses_json, list)

if __name__ == '__main__':
    unittest.main()
