from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from hermitta_app import db # Import db instance
from models.lease import Lease, LeaseStatusType, LeaseSigningStatus # Import SQLAlchemy model
from models.user import User # Needed for type checking landlord/tenant etc.
from models.property import Property # Needed for type checking property

class LeaseService:

    def _ensure_decimal(self, value: Any, field_name: str) -> Optional[Decimal]:
        if value is None: # Allow optional Decimal fields to be None
            return None
        if not isinstance(value, Decimal):
            try:
                return Decimal(str(value))
            except Exception as e:
                raise ValueError(f"Invalid value for Decimal field '{field_name}': {value} - {e}")
        return value

    def _ensure_date(self, value: Any, field_name: str) -> Optional[date]:
        if value is None: # Allow optional Date fields to be None
            return None
        if isinstance(value, date):
            return value
        if isinstance(value, datetime): # If datetime, convert to date
            return value.date()
        if isinstance(value, str):
            try:
                return date.fromisoformat(value) # Expects YYYY-MM-DD
            except ValueError:
                raise ValueError(f"Invalid date string for '{field_name}': {value}. Use YYYY-MM-DD format.")
        raise ValueError(f"Invalid type for date field '{field_name}': {type(value)}. Expected date or YYYY-MM-DD string.")

    def _prepare_lease_data(self, lease_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepares lease data for creation or update by converting string representations
        of enums, dates, and Decimals to their appropriate types.
        """
        prepared_data = lease_data.copy()

        # Handle enums
        if 'status' in prepared_data and isinstance(prepared_data['status'], str):
            try:
                prepared_data['status'] = LeaseStatusType[prepared_data['status'].upper()]
            except KeyError:
                raise ValueError(f"Invalid status string: {prepared_data['status']}")

        if 'signing_status' in prepared_data and isinstance(prepared_data['signing_status'], str):
            try:
                prepared_data['signing_status'] = LeaseSigningStatus[prepared_data['signing_status'].upper()]
            except KeyError:
                raise ValueError(f"Invalid signing_status string: {prepared_data['signing_status']}")

        # Handle dates
        date_fields = [
            'start_date', 'end_date', 'move_in_date', 'rent_start_date',
            'lease_document_uploaded_at', # This is DateTime in model, but _ensure_date handles it if only date part given
            'renewal_notice_reminder_date', 'termination_notice_reminder_date'
        ]
        for field in date_fields:
            if field in prepared_data: # Only process if field is present
                if field == 'lease_document_uploaded_at' and prepared_data[field] is not None: # This is DateTime
                    if isinstance(prepared_data[field], str):
                        try:
                            prepared_data[field] = datetime.fromisoformat(prepared_data[field].replace('Z', '+00:00'))
                        except ValueError:
                             raise ValueError(f"Invalid datetime string for '{field}': {prepared_data[field]}. Use ISO format.")
                    elif not isinstance(prepared_data[field], datetime):
                        raise ValueError(f"Invalid type for datetime field '{field}': {type(prepared_data[field])}")
                else: # Process as Date
                    prepared_data[field] = self._ensure_date(prepared_data[field], field)

        # Handle Decimals
        decimal_fields = ['rent_amount', 'security_deposit']
        for field in decimal_fields:
            if field in prepared_data: # Only process if field is present
                 prepared_data[field] = self._ensure_decimal(prepared_data[field], field)

        # Remove fields not part of the Lease model if they were passed (e.g. from old version)
        fields_to_remove_if_present = ['currency', 'payment_terms']
        for field_key in fields_to_remove_if_present:
            prepared_data.pop(field_key, None) # Safely remove if exists

        return prepared_data

    def create_lease(self, lease_data: Dict[str, Any]) -> Lease:
        """
        Creates a new lease.
        """
        prepared_data = self._prepare_lease_data(lease_data)

        # Basic validation for FK existence (DB will also enforce this)
        # These checks can be made more robust or rely on DB constraints for final validation
        if not User.query.get(prepared_data.get('landlord_id')):
            raise ValueError(f"Landlord user with ID {prepared_data.get('landlord_id')} not found.")
        if prepared_data.get('tenant_id') and not User.query.get(prepared_data.get('tenant_id')):
            raise ValueError(f"Tenant user with ID {prepared_data.get('tenant_id')} not found.")
        if not Property.query.get(prepared_data.get('property_id')):
            raise ValueError(f"Property with ID {prepared_data.get('property_id')} not found.")
        if prepared_data.get('lease_document_uploaded_by_user_id') and \
           not User.query.get(prepared_data.get('lease_document_uploaded_by_user_id')):
            raise ValueError(f"Uploader user with ID {prepared_data.get('lease_document_uploaded_by_user_id')} not found.")


        new_lease = Lease(**prepared_data)
        db.session.add(new_lease)
        db.session.commit()
        return new_lease

    def get_lease_by_id(self, lease_id: int) -> Optional[Lease]:
        return Lease.query.get(lease_id)

    def update_lease(self, lease_id: int, update_data: Dict[str, Any]) -> Optional[Lease]:
        lease_to_update = self.get_lease_by_id(lease_id)
        if not lease_to_update:
            return None

        prepared_data = self._prepare_lease_data(update_data)
        for key, value in prepared_data.items():
            if hasattr(lease_to_update, key): # Check if attribute exists on model
                setattr(lease_to_update, key, value)

        db.session.commit()
        return lease_to_update

    def delete_lease(self, lease_id: int) -> bool:
        lease_to_delete = self.get_lease_by_id(lease_id)
        if lease_to_delete:
            # TODO: Add more robust business logic, e.g., cannot delete an ACTIVE lease.
            # For now, simple deletion.
            db.session.delete(lease_to_delete)
            db.session.commit()
            return True
        return False

    def get_leases_for_property(self, property_id: int, page: int = 1, per_page: int = 10) -> (List[Lease], int):
        query = Lease.query.filter_by(property_id=property_id).order_by(Lease.start_date.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total

    def get_leases_for_landlord(self, landlord_id: int, page: int = 1, per_page: int = 10) -> (List[Lease], int):
        query = Lease.query.filter_by(landlord_id=landlord_id).order_by(Lease.start_date.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total

    def get_leases_for_tenant(self, tenant_id: int, page: int = 1, per_page: int = 10) -> (List[Lease], int):
        query = Lease.query.filter_by(tenant_id=tenant_id).order_by(Lease.start_date.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total

    # --- Methods related to e-signature and document management (stubs for now) ---

    def initiate_signing_process(self, lease_id: int, signers_data: List[Dict[str, Any]]) -> bool:
        lease = self.get_lease_by_id(lease_id)
        if lease and lease.signing_status in [LeaseSigningStatus.NOT_STARTED, LeaseSigningStatus.DRAFT]:
            # TODO: Actual e-signature provider integration or internal signing logic.
            # Validate lease.lease_document_content_final exists.
            lease.signature_requests = signers_data # This should be structured data
            lease.signing_status = LeaseSigningStatus.SENT_FOR_SIGNATURE
            db.session.commit()
            # TODO: Trigger notifications to signers.
            return True
        return False

    def get_signing_status_for_lease(self, lease_id: int) -> Optional[Dict[str, Any]]:
        lease = self.get_lease_by_id(lease_id)
        if lease:
            return {
                "lease_id": lease.lease_id,
                "signing_status": lease.signing_status.value,
                "signature_requests": lease.signature_requests or [] # Ensure it's a list
            }
        return None

    def update_signature_status_from_webhook(self, lease_id: int, signer_identifier: str, event_type: str) -> bool:
        # Placeholder: This is a complex method that would parse webhook payload
        # and update Lease.signature_requests and Lease.signing_status accordingly.
        # Security (webhook signature verification) is critical here.
        lease = self.get_lease_by_id(lease_id)
        if not lease or not lease.signature_requests:
            return False

        # Example logic (very simplified)
        all_signed = True
        for req in lease.signature_requests:
            # Assuming signer_identifier matches one of the signers (e.g., email)
            if req.get('email') == signer_identifier: # Or some other unique ID for the signer
                if event_type.upper() == 'SIGNED':
                    req['status'] = 'SIGNED'
                    req['signed_at'] = datetime.utcnow().isoformat()
                elif event_type.upper() == 'DECLINED':
                    req['status'] = 'DECLINED'
                    lease.signing_status = LeaseSigningStatus.DECLINED
                    all_signed = False
                    break
            if req.get('status') != 'SIGNED':
                all_signed = False

        if all_signed and lease.signing_status != LeaseSigningStatus.DECLINED:
            lease.signing_status = LeaseSigningStatus.FULLY_SIGNED_SYSTEM # Or provider specific

        db.session.commit()
        return True

    def record_in_system_signature(self, lease_id: int, user_id: int, typed_name: str) -> bool:
        # Placeholder for in-system "typed" signature.
        # Would involve updating signature_requests and checking if all parties signed.
        lease = self.get_lease_by_id(lease_id)
        if lease:
            # Find the user in signature_requests and update their status.
            # For this stub, assume it leads to full signature.
            lease.signing_status = LeaseSigningStatus.FULLY_SIGNED_SYSTEM
            db.session.commit()
            return True
        return False

    def link_signed_document(self, lease_id: int, document_id: int, uploaded_by_user_id: int) -> bool:
        # Assumes document_id refers to an entry in a 'documents' table.
        lease = self.get_lease_by_id(lease_id)
        if lease:
            lease.signed_lease_document_id = document_id
            lease.signing_status = LeaseSigningStatus.FULLY_SIGNED_UPLOADED
            # lease.lease_document_uploaded_by_user_id = uploaded_by_user_id # Or keep original uploader
            db.session.commit()
            return True
        return False

    def update_draft_document_link(self, lease_id: int, document_url: str, version: int, uploaded_by_user_id: int) -> bool:
        lease = self.get_lease_by_id(lease_id)
        if lease:
            lease.lease_document_url = document_url
            lease.lease_document_version = version
            lease.lease_document_uploaded_at = datetime.utcnow()
            lease.lease_document_uploaded_by_user_id = uploaded_by_user_id
            db.session.commit()
            return True
        return False

    def get_draft_document_details(self, lease_id: int) -> Optional[Dict[str, Any]]:
        lease = self.get_lease_by_id(lease_id)
        if lease and lease.lease_document_url:
            return {"url": lease.lease_document_url,
                    "version": lease.lease_document_version,
                    "name": "Lease Draft"} # Name could be more dynamic
        return None

    # Aliases for route test compatibility
    def create_lease_record(self, **data) -> Lease:
        return self.create_lease(data)

    def update_lease_details(self, lease_id: int, **data) -> Optional[Lease]:
        return self.update_lease(lease_id, data)

# Example Usage (would be done in a Flask context)
# if __name__ == '__main__':
#     from hermitta_app import create_app
#     # Assuming UserService and PropertyService are refactored
#     # from services.user_service import UserService
#     # from services.property_service import PropertyService
#     app = create_app('dev')
#     with app.app_context():
#         lease_service = LeaseService()
#         # landlord = UserService().get_user_by_id(1) # Assume user 1 is landlord
#         # tenant = UserService().get_user_by_id(2) # Assume user 2 is tenant
#         # property_ = PropertyService().get_property_by_id(1) # Assume property 1 exists
#         # if landlord and tenant and property_:
#         #     lease_data = {
#         #         "property_id": property_.property_id,
#         #         "landlord_id": landlord.user_id,
#         #         "tenant_id": tenant.user_id,
#         #         "start_date": "2024-08-01",
#         #         "end_date": "2025-07-31",
#         #         "rent_amount": Decimal("25000.00"),
#         #         "rent_due_day": 1,
#         #         "move_in_date": "2024-08-01",
#         #         "status": LeaseStatusType.DRAFT,
#         #         "signing_status": LeaseSigningStatus.NOT_STARTED,
#         #         "security_deposit": Decimal("50000.00")
#         #     }
#         #     try:
#         #         new_lease = lease_service.create_lease(lease_data)
#         #         print(f"Created Lease ID: {new_lease.lease_id}, Status: {new_lease.status.value}")
#         #
#         #         retrieved_l = lease_service.get_lease_by_id(new_lease.lease_id)
#         #         if retrieved_l:
#         #             print(f"Retrieved Lease Rent: {retrieved_l.rent_amount}")
#         #             lease_service.update_lease(new_lease.lease_id, {"notes": "Updated with some notes."})
#         #             updated_l = lease_service.get_lease_by_id(new_lease.lease_id)
#         #             print(f"Updated Lease Notes: {updated_l.notes}")
#         #
#         #         # lease_service.delete_lease(new_lease.lease_id)
#         #         # print(f"Lease {new_lease.lease_id} deleted: {lease_service.get_lease_by_id(new_lease.lease_id) is None}")
#         #
#         #     except Exception as e:
#         #         print(f"Error in LeaseService example: {e}")
#         #         db.session.rollback()
#         # else:
#         #     print("Required landlord, tenant, or property for LeaseService example not found.")
#         print("LeaseService SQLAlchemy example usage placeholder complete.")
