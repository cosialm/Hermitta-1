from datetime import datetime
from typing import Optional
from hermitta_app import db
from .enums import MpesaShortcodeType # Import from shared enums

class LandlordMpesaConfig(db.Model):
    __tablename__ = 'landlord_mpesa_configs'

    config_id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, unique=True, index=True) # One-to-one with Landlord

    shortcode_type = db.Column(db.Enum(MpesaShortcodeType), default=MpesaShortcodeType.NONE, nullable=False)
    paybill_number = db.Column(db.String(20), nullable=True, index=True) # Business PayBill number
    till_number = db.Column(db.String(20), nullable=True, index=True)    # Business Till Number

    # Sensitive credentials - these should be encrypted in the database.
    # The model stores them as strings; application layer handles encryption/decryption.
    consumer_key_encrypted = db.Column(db.String(512), nullable=True)   # Daraja API Consumer Key
    consumer_secret_encrypted = db.Column(db.String(512), nullable=True) # Daraja API Consumer Secret
    passkey_encrypted = db.Column(db.String(512), nullable=True)        # Daraja API Passkey for STK Push

    account_reference_prefix = db.Column(db.String(50), nullable=True) # Optional prefix for account numbers, e.g., "APT"
    callback_url_override = db.Column(db.String(512), nullable=True) # If platform allows per-landlord callback URLs

    is_active = db.Column(db.Boolean, default=False, nullable=False, index=True) # Landlord must explicitly activate

    last_validation_check_at = db.Column(db.DateTime, nullable=True) # Timestamp of last successful credential validation
    validation_status = db.Column(db.String(50), nullable=True) # e.g., "VALIDATED", "VALIDATION_FAILED", "PENDING_VALIDATION"
    validation_message = db.Column(db.Text, nullable=True) # Details from the validation attempt

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship
    landlord = db.relationship('User', backref=db.backref('mpesa_config', uselist=False, lazy='joined'))

    def __repr__(self):
        return f"<LandlordMpesaConfig {self.config_id} for Landlord {self.landlord_id} - Type: {self.shortcode_type.value if self.shortcode_type else 'N/A'}>"

    # Note: Methods for get_consumer_key(), get_consumer_secret(), get_passkey()
    # that handle decryption would be part of a service layer or utility, not directly in the model
    # to keep the model focused on data structure and ORM. Example:
    # from your_app.security import decrypt_value
    # def get_decrypted_consumer_key(self):
    #     return decrypt_value(self.consumer_key_encrypted) if self.consumer_key_encrypted else None
