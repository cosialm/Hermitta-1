from datetime import datetime
from typing import Optional, List # List for future specific permissions

class DocumentSharePermission(Enum): # More granular if needed in future
    VIEW = "VIEW"
    DOWNLOAD = "DOWNLOAD"
    # EDIT_METADATA = "EDIT_METADATA" # Unlikely for shared docs
    # DELETE = "DELETE"             # Unlikely for shared docs

class DocumentShare:
    def __init__(self,
                 share_id: int,
                 document_id: int, # Foreign Key to Document
                 shared_with_user_id: int, # Foreign Key to User (e.g., a Tenant, Staff, Vendor)
                 shared_by_user_id: int,   # Foreign Key to User (e.g., Landlord who owns/uploaded the doc)
                 # For MVP, simple boolean flags. Could evolve to a list of DocumentSharePermission enums.
                 can_view: bool = True,
                 can_download: bool = True,
                 # can_edit_metadata: bool = False, # Typically false for shared documents
                 # permissions: Optional[List[DocumentSharePermission]] = None, # More granular alternative
                 shared_at: datetime = datetime.utcnow(),
                 expires_at: Optional[datetime] = None, # Optional: if the share link/access should expire
                 access_notes: Optional[str] = None # e.g., "Shared for lease review", "Tenant copy of signed lease"
                 ):

        self.share_id = share_id
        self.document_id = document_id
        self.shared_with_user_id = shared_with_user_id
        self.shared_by_user_id = shared_by_user_id

        self.can_view = can_view
        self.can_download = can_download
        # if permissions is not None:
        #     self.can_view = DocumentSharePermission.VIEW in permissions
        #     self.can_download = DocumentSharePermission.DOWNLOAD in permissions
        # else: # Fallback to booleans if permissions list not used
        #     self.can_view = can_view
        #     self.can_download = can_download

        self.shared_at = shared_at
        self.expires_at = expires_at
        self.access_notes = access_notes

# Example Usage:
# landlord_shares_lease_with_tenant = DocumentShare(
#     share_id=1, document_id=50, # Assuming Document ID 50 is "Signed Lease for Apt 3B"
#     shared_with_user_id=201, # Tenant's User ID
#     shared_by_user_id=10,    # Landlord's User ID
#     can_view=True, can_download=True,
#     access_notes="Your signed lease agreement for Apt 3B."
# )
#
# landlord_shares_invoice_with_staff = DocumentShare(
#     share_id=2, document_id=55, # Assuming Document ID 55 is "Invoice for Plumbing Work Prop X"
#     shared_with_user_id=401, # Staff User ID
#     shared_by_user_id=10,
#     can_view=True, can_download=False, # Staff can view for records, but maybe not download
#     access_notes="FYI - Plumbing invoice for Property X, for your records."
# )
# print(f"Share ID {landlord_shares_lease_with_tenant.share_id} for Document {landlord_shares_lease_with_tenant.document_id}")

# Need to import Enum for DocumentSharePermission
from enum import Enum
