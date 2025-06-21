import enum

class PaymentMethod(enum.Enum):
    # Manual methods
    CASH_TO_LANDLORD = "CASH_TO_LANDLORD"
    BANK_DEPOSIT_LANDLORD = "BANK_DEPOSIT_LANDLORD"
    MPESA_TO_LANDLORD_MANUAL = "MPESA_TO_LANDLORD_MANUAL" # Manually recorded by landlord
    OTHER_MANUAL = "OTHER_MANUAL"

    # Online methods
    MPESA_ONLINE_STK = "MPESA_ONLINE_STK" # Tenant initiated via STK Push (Direct M-Pesa)
    # Generic online methods for multi-gateway support
    GATEWAY_CARD = "GATEWAY_CARD" # e.g., Visa/Mastercard via Pesapal, Stripe, Flutterwave
    GATEWAY_MOBILE_MONEY = "GATEWAY_MOBILE_MONEY" # e.g., M-Pesa/Airtel via Pesapal, Flutterwave
    GATEWAY_OTHER = "GATEWAY_OTHER" # Other methods supported by an aggregator

class PaymentStatus(enum.Enum):
    EXPECTED = "EXPECTED"               # Rent is due, payment record created automatically or by landlord as expectation
    PENDING_CONFIRMATION = "PENDING_CONFIRMATION" # Online payment initiated, awaiting callback
    COMPLETED = "COMPLETED"             # Payment confirmed (manual or online)
    PARTIALLY_PAID = "PARTIALLY_PAID"   # If partial payments are allowed and tracked
    FAILED = "FAILED"                   # Online payment failed, or manual entry was erroneous and voided
    OVERDUE = "OVERDUE"                 # Payment was expected but not completed by due date + grace period
    CANCELLED = "CANCELLED"             # E.g. STK push cancelled by user
    PENDING_APPROVAL = "PENDING_APPROVAL" # For payments that require manual approval after being made (e.g. large bank transfers)
    REFUNDED = "REFUNDED"               # Payment was refunded
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED" # Payment was partially refunded
    IN_DISPUTE = "IN_DISPUTE"           # Payment is currently under dispute

class MessageType(enum.Enum):
    DIRECT_MESSAGE = "DIRECT_MESSAGE"         # General user-to-user message
    LEASE_MESSAGE = "LEASE_MESSAGE"           # Message specifically related to a lease
    PROPERTY_INQUIRY_RESPONSE = "PROPERTY_INQUIRY_RESPONSE" # Response to a ProspectInquiry
    MAINTENANCE_COMMUNICATION = "MAINTENANCE_COMMUNICATION" # Related to a maintenance request (distinct from MaintenanceCommunication model for now)
    SYSTEM_NOTIFICATION = "SYSTEM_NOTIFICATION"   # Automated system message (e.g., rent reminder, account update)
    BROADCAST_MESSAGE = "BROADCAST_MESSAGE"     # Message from landlord to multiple tenants (e.g. of a property)

class MessageStatus(enum.Enum):
    SENT = "SENT"                   # Message successfully sent by the system
    DELIVERED_TO_SERVER = "DELIVERED_TO_SERVER" # Confirmed receipt by messaging server (if applicable)
    DELIVERED_TO_RECIPIENT = "DELIVERED_TO_RECIPIENT" # Confirmed receipt by recipient's client (e.g., push notification ack)
    READ = "READ"                   # Recipient has read the message
    FAILED_TO_SEND = "FAILED_TO_SEND"     # System failed to send the message
    ARCHIVED = "ARCHIVED"             # Message archived by sender or receiver
    DELETED_BY_SENDER = "DELETED_BY_SENDER" # Sender soft-deleted their copy
    DELETED_BY_RECEIVER = "DELETED_BY_RECEIVER" # Receiver soft-deleted their copy


# It's good practice to also have general status enums if they are used across multiple models
class GeneralStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"

# Example of a more specific status that might be used elsewhere
class MaintenanceRequestStatus(enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REQUIRES_QUOTE_APPROVAL = "REQUIRES_QUOTE_APPROVAL"

# You can continue adding other shared enums here as the application grows.
# For instance, User roles, Property types (if not already defined elsewhere and needed broadly)
# Ensure enums that are tightly coupled to a single model and not reused can stay within that model's file.
# However, for things like PaymentStatus, which might be referenced by FinancialTransaction or other modules,
# having them here is beneficial.
# The `PropertyType` and `PropertyStatus` are already in `models/property.py`
# and seem specific enough to remain there unless wider use cases emerge.
# Similarly, `FinancialTransactionType` is in `models/financial_transaction.py`.
# If `GatewayTransactionStatus` and `GatewayTypeEnum` from `gateway_transaction.py`
# are only used by that model, they can remain there. If they become widely used (e.g. in UI components, reporting),
# then moving them here would be a good refactor. For now, plan keeps them local.
