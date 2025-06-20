from enum import Enum
from datetime import datetime
from typing import Optional

class GatewayType(Enum):
    PESAPAL = "PESAPAL"
    STRIPE = "STRIPE"
    FLUTTERWAVE = "FLUTTERWAVE"
    # MPESA_DIRECT = "MPESA_DIRECT" # If MpesaConfiguration is separate and we need to distinguish

class GatewayEnvironment(Enum):
    SANDBOX = "SANDBOX"
    PRODUCTION = "PRODUCTION"

class LandlordGatewayConfig:
    def __init__(self,
                 config_id: int, # PK
                 landlord_id: int, # FK to User model
                 gateway_type: GatewayType,
                 consumer_key_encrypted: str, # Store encrypted credentials
                 consumer_secret_encrypted: str, # Store encrypted credentials
                 api_key_encrypted: Optional[str] = None, # For other gateways like Stripe
                 account_identifier: Optional[str] = None, # e.g., Pesapal merchant account, specific paybill/till
                 environment: GatewayEnvironment = GatewayEnvironment.SANDBOX,
                 is_active: bool = True,
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.config_id = config_id
        self.landlord_id = landlord_id
        self.gateway_type = gateway_type
        self.consumer_key_encrypted = consumer_key_encrypted
        self.consumer_secret_encrypted = consumer_secret_encrypted
        self.api_key_encrypted = api_key_encrypted # General purpose for other potential gateways
        self.account_identifier = account_identifier
        self.environment = environment
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# pesapal_config = LandlordGatewayConfig(
#     config_id=1,
#     landlord_id=10,
#     gateway_type=GatewayType.PESAPAL,
#     consumer_key_encrypted="encrypted_pesapal_key",
#     consumer_secret_encrypted="encrypted_pesapal_secret",
#     account_identifier="PESAPAL_MERCHANT_XYZ",
#     environment=GatewayEnvironment.PRODUCTION,
#     is_active=True
# )
# print(pesapal_config.gateway_type, pesapal_config.account_identifier)
