from datetime import datetime
from typing import Optional
from hermitta_app import db
from .enums import GatewayType, GatewayEnvironment # Import from shared enums

class LandlordGatewayConfig(db.Model):
    __tablename__ = 'landlord_gateway_configs'

    config_id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)

    gateway_type = db.Column(db.Enum(GatewayType), nullable=False, index=True)

    # Generic field for primary account identifier with the gateway
    # e.g., Pesapal merchant account ID, Stripe Account ID, Flutterwave merchant ID.
    account_identifier = db.Column(db.String(255), nullable=True)

    # Sensitive credentials - should be encrypted.
    # Stored as strings; application layer handles encryption/decryption.
    # Using generic names; specific gateways might use different terminology (e.g., API Key, Secret Key, Publishable Key)
    # These can be stored in a JSONB field if structure varies greatly, or have multiple nullable fields.
    # For now, using common patterns:
    credential_1_encrypted = db.Column(db.String(512), nullable=True) # e.g., Consumer Key, API Key, Publishable Key
    credential_2_encrypted = db.Column(db.String(512), nullable=True) # e.g., Consumer Secret, Secret Key
    credential_3_encrypted = db.Column(db.String(512), nullable=True) # Additional field if needed

    # Store all other gateway-specific settings as JSON.
    # e.g., webhook secrets, specific API endpoints if different from default, etc.
    additional_settings_encrypted = db.Column(db.JSON, nullable=True)

    environment = db.Column(db.Enum(GatewayEnvironment), default=GatewayEnvironment.SANDBOX, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False, index=True)

    # Similar to MpesaConfig for validation tracking
    last_validation_check_at = db.Column(db.DateTime, nullable=True)
    validation_status = db.Column(db.String(50), nullable=True) # e.g., "VALIDATED", "VALIDATION_FAILED"
    validation_message = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship
    landlord = db.relationship('User', backref=db.backref('gateway_configs', lazy='dynamic')) # A landlord can have multiple configs for different gateways

    # Unique constraint for landlord_id and gateway_type to ensure only one active config per gateway type per landlord.
    # However, a landlord might want to have multiple configurations for the SAME gateway type (e.g. two different Pesapal accounts).
    # If so, this unique constraint should be on a combination that allows this, or removed if 'is_active' handles uniqueness.
    # For now, let's assume a landlord configures a specific GatewayType once.
    __table_args__ = (db.UniqueConstraint('landlord_id', 'gateway_type', name='uq_landlord_gateway_type'),)


    def __repr__(self):
        return f"<LandlordGatewayConfig {self.config_id} for Landlord {self.landlord_id} - Gateway: {self.gateway_type.value}>"

    # Decryption methods would be in a service layer. Example:
    # def get_decrypted_credential_1(self):
    #     from your_app.security import decrypt_value
    #     return decrypt_value(self.credential_1_encrypted) if self.credential_1_encrypted else None
