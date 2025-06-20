from datetime import datetime
from typing import Optional

class DocumentFolder:
    def __init__(self,
                 folder_id: int,
                 landlord_id: int, # Foreign Key to User (Landlord who owns this folder structure)
                 name: str,        # Name of the folder, e.g., "Property A Leases", "Tax Documents 2023"
                 parent_folder_id: Optional[int] = None, # FK to self for nested folders (null for root folders)
                 # Optional: Link folder to a specific property if all its contents are property-specific
                 # property_id: Optional[int] = None, # FK to Property
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.folder_id = folder_id
        self.landlord_id = landlord_id # Each landlord manages their own folder structure
        self.name = name # Should be unique within a parent_folder_id for a given landlord
        self.parent_folder_id = parent_folder_id # If null, it's a top-level folder for the landlord
        # self.property_id = property_id # If this folder is exclusively for one property

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# root_folder_leases = DocumentFolder(
#     folder_id=1, landlord_id=10, name="All Lease Agreements"
# )
#
# property_A_folder = DocumentFolder(
#     folder_id=2, landlord_id=10, name="Property A (123 Main St)", parent_folder_id=None
#     # property_id=101 # Could also link directly to property
# )
#
# property_A_leases_subfolder = DocumentFolder(
#     folder_id=3, landlord_id=10, name="Lease Agreements", parent_folder_id=property_A_folder.folder_id
# )
#
# property_A_invoices_subfolder = DocumentFolder(
#     folder_id=4, landlord_id=10, name="Maintenance Invoices", parent_folder_id=property_A_folder.folder_id
# )
#
# print(root_folder_leases.name)
# print(f"Folder '{property_A_leases_subfolder.name}' is inside '{property_A_folder.name}' (ID: {property_A_leases_subfolder.parent_folder_id})")
