from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from models.lease import Lease, LeaseStatusType, LeaseSigningStatus # Assuming these enums are in models.lease

class LeaseService:
    def __init__(self):
        self.leases: List[Lease] = []
        self._next_id: int = 1

    def _ensure_decimal(self, value: Any, field_name: str) -> Decimal:
        if not isinstance(value, Decimal):
            try:
                return Decimal(str(value))
            except Exception as e:
                raise ValueError(f"Invalid value for Decimal field '{field_name}': {value} - {e}")
        return value

    def _ensure_date(self, value: Any, field_name: str) -> date:
        if isinstance(value, date):
            return value
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except ValueError:
                raise ValueError(f"Invalid date string for '{field_name}': {value}. Use YYYY-MM-DD format.")
        raise ValueError(f"Invalid type for date field '{field_name}': {type(value)}. Expected date or YYYY-MM-DD string.")


    def create_lease(self, lease_data: Dict[str, Any]) -> Lease:
        """
        Creates a new lease and stores it in memory.
        Ensures all required fields for Lease model are present or defaulted.
        Handles type conversions for enums, dates, and Decimals.
        """
        new_lease_id = self._next_id

        processed_data = lease_data.copy()
        processed_data["lease_id"] = new_lease_id

        # Handle enums
        if 'status' in processed_data:
            if isinstance(processed_data['status'], str):
                try:
                    processed_data['status'] = LeaseStatusType[processed_data['status'].upper()]
                except KeyError:
                    raise ValueError(f"Invalid status string: {processed_data['status']}")
        else:
            processed_data['status'] = LeaseStatusType.DRAFT

        if 'signing_status' in processed_data:
            if isinstance(processed_data['signing_status'], str):
                try:
                    processed_data['signing_status'] = LeaseSigningStatus[processed_data['signing_status'].upper()]
                except KeyError:
                    raise ValueError(f"Invalid signing_status string: {processed_data['signing_status']}")
        else:
            processed_data['signing_status'] = LeaseSigningStatus.NOT_STARTED

        # Handle dates
        date_fields = ['start_date', 'end_date', 'move_in_date']
        for field in date_fields:
            if field in processed_data and processed_data[field] is not None:
                processed_data[field] = self._ensure_date(processed_data[field], field)
            # Removed explicit check for missing required date fields here,
            # Lease model's __init__ will handle it.

        # Handle Decimals
        decimal_fields = ['rent_amount', 'security_deposit']
        for field in decimal_fields:
            if field in processed_data and processed_data[field] is not None:
                processed_data[field] = self._ensure_decimal(processed_data[field], field)
            # Removed explicit check for missing required Decimal fields here,
            # Lease model's __init__ will handle it.

        # Ensure all required fields for Lease model are present after processing
        # The Lease model's __init__ will ultimately validate this.
        # created_at, updated_at are defaulted by the Lease model.

        # Remove fields not expected by Lease model before instantiation
        fields_to_remove_if_present = ['currency', 'payment_terms']
        for field_key in fields_to_remove_if_present:
            if field_key in processed_data:
                del processed_data[field_key]

        try:
            lease_instance = Lease(**processed_data)
        except TypeError as e:
            raise ValueError(f"Missing required fields or incorrect data for Lease creation: {e}")
        except Exception as e: # Catch any other model validation errors
            raise ValueError(f"Error during Lease instantiation: {e}")

        self.leases.append(lease_instance)
        self._next_id += 1
        return lease_instance

    def get_lease(self, lease_id: int) -> Optional[Lease]:
        """
        Retrieves a lease by its ID from the in-memory store.
        """
        for lease in self.leases:
            if lease.lease_id == lease_id:
                return lease
        return None

    def update_lease(self, lease_id: int, update_data: Dict[str, Any]) -> Optional[Lease]:
        """
        Updates an existing lease in the in-memory store.
        """
        lease_to_update = self.get_lease(lease_id)
        if lease_to_update:
            processed_update_data = update_data.copy()

            # Handle enums
            if 'status' in processed_update_data and isinstance(processed_update_data['status'], str):
                try:
                    processed_update_data['status'] = LeaseStatusType[processed_update_data['status'].upper()]
                except KeyError:
                    raise ValueError(f"Invalid status string for update: {processed_update_data['status']}")

            if 'signing_status' in processed_update_data and isinstance(processed_update_data['signing_status'], str):
                try:
                    processed_update_data['signing_status'] = LeaseSigningStatus[processed_update_data['signing_status'].upper()]
                except KeyError:
                    raise ValueError(f"Invalid signing_status string for update: {processed_update_data['signing_status']}")

            # Handle dates
            date_fields = ['start_date', 'end_date', 'move_in_date']
            for field in date_fields:
                if field in processed_update_data and processed_update_data[field] is not None:
                    processed_update_data[field] = self._ensure_date(processed_update_data[field], field)

            # Handle Decimals
            decimal_fields = ['rent_amount', 'security_deposit']
            for field in decimal_fields:
                if field in processed_update_data and processed_update_data[field] is not None:
                    processed_update_data[field] = self._ensure_decimal(processed_update_data[field], field)

            # Remove fields not on Lease model before attempting setattr
            fields_to_remove_if_present_on_update = ['currency', 'payment_terms']
            for field_key in fields_to_remove_if_present_on_update:
                if field_key in processed_update_data:
                    del processed_update_data[field_key]

            for key, value in processed_update_data.items():
                if hasattr(lease_to_update, key):
                    setattr(lease_to_update, key, value)

            lease_to_update.updated_at = datetime.utcnow()
            return lease_to_update
        return None

    def delete_lease(self, lease_id: int) -> bool:
        """
        Deletes a lease by its ID from the in-memory store.
        """
        lease_to_delete = self.get_lease(lease_id)
        if lease_to_delete:
            self.leases.remove(lease_to_delete)
            return True
        return False

    # Dummy methods for compatibility with other test modules if they import LeaseService
    def get_lease_details_for_payment(self, lease_id: int): # Used in payment_routes tests
        return self.get_lease(lease_id)

    def create_lease_record(self, **data): # Used in lease_routes tests
        return self.create_lease(data)

    def get_lease_by_id(self, lease_id: int): # Used in lease_routes tests
        return self.get_lease(lease_id)

    def update_lease_details(self, lease_id: int, **data): # Used in lease_routes tests
        return self.update_lease(lease_id, data)

    def initiate_signing_process(self, lease_id: int, **data): # Used in lease_routes tests
        # This is a complex process, just a stub here
        lease = self.get_lease(lease_id)
        if lease:
            lease.signing_status = LeaseSigningStatus.SENT_FOR_SIGNATURE
            lease.updated_at = datetime.utcnow()
            return True
        return False

    def get_signing_status_for_lease(self, lease_id: int): # Used in lease_routes tests
        lease = self.get_lease(lease_id)
        if lease:
            return {"signing_status": lease.signing_status.value, "signature_requests": []} # Dummy response
        return None

    def update_signature_status_from_webhook(self, **data): # Used in lease_routes tests
        # Complex logic, stub
        return True

    def record_in_system_signature(self, lease_id: int, **data): # Used in lease_routes tests
        lease = self.get_lease(lease_id)
        if lease:
            # Simplified: assume one signer, sets to fully signed
            lease.signing_status = LeaseSigningStatus.FULLY_SIGNED_SYSTEM
            lease.updated_at = datetime.utcnow()
            return True
        return False

    def link_signed_document(self, lease_id: int, document_id: int): # Used in lease_routes tests
        lease = self.get_lease(lease_id)
        if lease:
            lease.signed_lease_document_id = document_id
            lease.signing_status = LeaseSigningStatus.FULLY_SIGNED_UPLOADED
            lease.updated_at = datetime.utcnow()
            return True
        return False

    def update_draft_document_link(self, lease_id: int, document_id: int): # Used in lease_routes tests
        lease = self.get_lease(lease_id)
        if lease:
            lease.lease_document_url = f"http://example.com/docs/{document_id}" # Example
            lease.updated_at = datetime.utcnow()
            return True
        return False

    def get_draft_document_details(self, lease_id: int): # Used in lease_routes tests
        lease = self.get_lease(lease_id)
        if lease:
            return {"url": lease.lease_document_url, "name": "Lease Draft"}
        return None

# Example Usage (not part of the class, for illustration)
if __name__ == '__main__':
    service = LeaseService()
    sample_data = {
        "property_id": 1,
        "tenant_id": 1,
        "landlord_id": 101,
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "rent_amount": "1500.50",
        "security_deposit": "3000.00",
        "currency": "KES",
        "payment_terms": "Monthly",
        "status": "ACTIVE", # String, will be converted
        "signing_status": "FULLY_SIGNED_SYSTEM" # String
    }
    try:
        lease1 = service.create_lease(sample_data)
        print(f"Created Lease 1: ID {lease1.lease_id}, Status {lease1.status.value}, Rent {lease1.rent_amount}")
    except ValueError as e:
        print(f"Error creating lease: {e}")

    retrieved_lease1 = service.get_lease(1)
    if retrieved_lease1:
        print(f"Retrieved Lease 1: Start Date {retrieved_lease1.start_date}")

    update_data_for_lease1 = {"rent_amount": "1600.00", "status": "EXPIRED"}
    try:
        updated_lease1 = service.update_lease(1, update_data_for_lease1)
        if updated_lease1:
            print(f"Updated Lease 1: Rent {updated_lease1.rent_amount}, Status {updated_lease1.status.value}, Updated At {updated_lease1.updated_at}")
    except ValueError as e:
        print(f"Error updating lease: {e}")

    service.delete_lease(1)
    print(f"Leases after deleting lease 1: {[l.lease_id for l in service.leases]}")

    # Test with missing required field
    missing_data = {"property_id": 2, "landlord_id": 102}
    try:
        service.create_lease(missing_data)
    except ValueError as e:
        print(f"Error creating lease with missing data: {e}")

    # Test with invalid enum string
    invalid_enum_data = {**sample_data, "status": "INVALID_STATUS_STRING"}
    try:
        service.create_lease(invalid_enum_data)
    except ValueError as e:
        print(f"Error creating lease with invalid enum: {e}")

    # Test with invalid date string
    invalid_date_data = {**sample_data, "start_date": "2024/01/01"} # wrong format
    try:
        service.create_lease(invalid_date_data)
    except ValueError as e:
        print(f"Error creating lease with invalid date: {e}")

    # Test with invalid decimal value
    invalid_decimal_data = {**sample_data, "rent_amount": "abc.xyz"}
    try:
        service.create_lease(invalid_decimal_data)
    except ValueError as e:
        print(f"Error creating lease with invalid decimal: {e}")

    print("Lease service stub testing complete.")
