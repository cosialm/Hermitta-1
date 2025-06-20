from enum import Enum
from datetime import datetime
from typing import Optional

# It's crucial that sensitive fields (consumer_key, consumer_secret, passkey)
# are encrypted in the database and only decrypted in memory when needed.
# The actual encryption/decryption logic is outside the scope of this model definition
# but is a critical implementation detail.

class MpesaShortcodeType(Enum):
    PAYBILL = "PAYBILL"
    TILL_NUMBER = "TILL_NUMBER" # Business Till / Buy Goods Till
    NONE = "NONE" # If landlord isn't configuring M-Pesa for direct collection

class LandlordMpesaConfiguration:
    def __init__(self,
                 config_id: int,
                 landlord_id: int, # Foreign Key to User (Landlord)
                 shortcode_type: MpesaShortcodeType = MpesaShortcodeType.NONE,
                 paybill_number: Optional[str] = None, # Business PayBill number
                 till_number: Optional[str] = None,    # Business Till Number
                 consumer_key: Optional[str] = None,   # Daraja API Consumer Key (Encrypted)
                 consumer_secret: Optional[str] = None,# Daraja API Consumer Secret (Encrypted)
                 passkey: Optional[str] = None,        # Daraja API Passkey for STK Push (Encrypted)
                 # For STK Push, the registered shortcode is used.
                 # For C2B, you might need a specific paybill/till for receiving payments.
                 # The platform might also operate its own central PayBill/Till and then reconcile.
                 # This model assumes landlord wants to use THEIR OWN M-Pesa credentials for STK.
                 account_reference_prefix: Optional[str] = None, # Optional prefix for account numbers, e.g., "APT" -> APT101
                 callback_url_override: Optional[str] = None, # If platform allows per-landlord callback URLs
                 is_active: bool = False, # Landlord must explicitly activate this config
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow(),
                 last_validation_check: Optional[datetime] = None, # Timestamp of last successful credential validation
                 validation_status: Optional[str] = None # e.g., "VALIDATED", "VALIDATION_FAILED"
                 ):

        self.config_id = config_id
        self.landlord_id = landlord_id # Unique or One-to-One with User (Landlord)

        self.shortcode_type = shortcode_type
        self.paybill_number = paybill_number # For STK push, this would be the initiator shortcode
        self.till_number = till_number       # Or this, depending on M-Pesa product used for STK

        # Sensitive credentials - ensure these are handled securely (e.g., Vault, KMS, DB encryption)
        self.consumer_key_encrypted = consumer_key # Store as encrypted
        self.consumer_secret_encrypted = consumer_secret # Store as encrypted
        self.passkey_encrypted = passkey # Store as encrypted

        self.account_reference_prefix = account_reference_prefix
        self.callback_url_override = callback_url_override # If not set, platform default is used

        self.is_active = is_active # Configuration must be active to be used
        self.last_validation_check = last_validation_check
        self.validation_status = validation_status

        self.created_at = created_at
        self.updated_at = updated_at

    # Placeholder methods for handling encrypted fields (actual logic would be elsewhere)
    def get_consumer_key(self) -> Optional[str]:
        # TODO: Implement decryption
        return self.consumer_key_encrypted

    def get_consumer_secret(self) -> Optional[str]:
        # TODO: Implement decryption
        return self.consumer_secret_encrypted

    def get_passkey(self) -> Optional[str]:
        # TODO: Implement decryption
        return self.passkey_encrypted

# Example Usage:
# landlord_mpesa_setup = LandlordMpesaConfiguration(
#     config_id=1, landlord_id=10, shortcode_type=MpesaShortcodeType.PAYBILL,
#     paybill_number="600000", # Example business shortcode
#     consumer_key="encrypted_key_here",
#     consumer_secret="encrypted_secret_here",
#     passkey="encrypted_passkey_here",
#     is_active=True,
#     account_reference_prefix="MYPROPS"
# )
# print(landlord_mpesa_setup.paybill_number, landlord_mpesa_setup.is_active)
