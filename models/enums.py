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

class NotificationChannel(enum.Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    IN_APP = "IN_APP"
    # PUSH_NOTIFICATION = "PUSH_NOTIFICATION" # Could be a separate channel or part of IN_APP logic

class NotificationType(enum.Enum):
    # General & Account
    WELCOME_MESSAGE = "WELCOME_MESSAGE"
    ACCOUNT_ACTIVATION = "ACCOUNT_ACTIVATION"
    PASSWORD_RESET_REQUEST = "PASSWORD_RESET_REQUEST"
    PASSWORD_CHANGED_CONFIRMATION = "PASSWORD_CHANGED_CONFIRMATION"
    EMAIL_VERIFICATION = "EMAIL_VERIFICATION"
    PROFILE_UPDATE_CONFIRMATION = "PROFILE_UPDATE_CONFIRMATION"
    # Lease Related
    LEASE_AGREEMENT_SHARED = "LEASE_AGREEMENT_SHARED"
    LEASE_SIGNED_CONFIRMATION = "LEASE_SIGNED_CONFIRMATION"
    LEASE_RENEWAL_REMINDER = "LEASE_RENEWAL_REMINDER"
    LEASE_EXPIRATION_REMINDER = "LEASE_EXPIRATION_REMINDER"
    LEASE_TERMINATION_NOTICE = "LEASE_TERMINATION_NOTICE"
    MOVE_IN_REMINDER = "MOVE_IN_REMINDER"
    MOVE_OUT_REMINDER = "MOVE_OUT_REMINDER"
    # Payment Related
    RENT_REMINDER = "RENT_REMINDER"
    RENT_OVERDUE_NOTICE = "RENT_OVERDUE_NOTICE"
    PAYMENT_RECEIVED_CONFIRMATION = "PAYMENT_RECEIVED_CONFIRMATION"
    PAYMENT_FAILED_ALERT = "PAYMENT_FAILED_ALERT"
    INVOICE_GENERATED = "INVOICE_GENERATED" # For utilities, services etc.
    REFUND_PROCESSED = "REFUND_PROCESSED"
    # Maintenance Related
    MAINTENANCE_REQUEST_RECEIVED = "MAINTENANCE_REQUEST_RECEIVED"
    MAINTENANCE_STATUS_UPDATE = "MAINTENANCE_STATUS_UPDATE" # e.g. scheduled, in_progress, completed
    MAINTENANCE_QUOTE_AVAILABLE = "MAINTENANCE_QUOTE_AVAILABLE"
    MAINTENANCE_FEEDBACK_REQUEST = "MAINTENANCE_FEEDBACK_REQUEST"
    # Communication & Document Related
    NEW_MESSAGE_ALERT = "NEW_MESSAGE_ALERT" # User received a new direct message
    NEW_DOCUMENT_SHARED = "NEW_DOCUMENT_SHARED"
    DOCUMENT_EXPIRING_SOON = "DOCUMENT_EXPIRING_SOON" # e.g. compliance docs
    # Property & Prospect Related
    NEW_PROPERTY_LISTING_MATCH = "NEW_PROPERTY_LISTING_MATCH" # For prospects
    PROPERTY_VIEWING_CONFIRMATION = "PROPERTY_VIEWING_CONFIRMATION"
    PROPERTY_VIEWING_REMINDER = "PROPERTY_VIEWING_REMINDER"
    APPLICATION_RECEIVED_CONFIRMATION = "APPLICATION_RECEIVED_CONFIRMATION" # For landlord & applicant
    APPLICATION_STATUS_UPDATE = "APPLICATION_STATUS_UPDATE" # For applicant
    # System & Other
    SYSTEM_ALERT = "SYSTEM_ALERT" # General system alerts
    BROADCAST_ANNOUNCEMENT = "BROADCAST_ANNOUNCEMENT" # To groups of users
    OTHER = "OTHER" # Generic catch-all

class NotificationStatus(enum.Enum):
    SCHEDULED = "SCHEDULED"             # Notification is scheduled for future sending
    PENDING = "PENDING"                 # Queued for immediate sending by the notification dispatcher (renamed from PENDING_SEND)
    SENT = "SENT"                       # Successfully dispatched to the gateway (e.g., email server, SMS provider) (renamed from SENT_SUCCESS)
    FAILED = "FAILED"                   # Failed to dispatch to the gateway (renamed from SENT_FAIL)
    DELIVERED = "DELIVERED"             # Gateway confirmed delivery to recipient's device/server (renamed from DELIVERY_CONFIRMED)
    DELIVERY_FAILURE = "DELIVERY_FAILURE" # Gateway confirmed failure to deliver (renamed from DELIVERY_FAILED)
    READ = "READ"                       # User has marked the notification as read (primarily for IN_APP)
    ARCHIVED = "ARCHIVED"               # User has archived the notification
    CANCELLED = "CANCELLED"             # Scheduled notification was cancelled before sending
    INVALID_ADDRESS = "INVALID_ADDRESS" # e.g. Email bounced, invalid phone for SMS

class GatewayType(enum.Enum): # Centralized GatewayType
    PESAPAL = "PESAPAL"
    STRIPE = "STRIPE"
    FLUTTERWAVE = "FLUTTERWAVE"
    PAYPAL = "PAYPAL"
    MPESA_STK_PUSH = "MPESA_STK_PUSH" # For Daraja STK Push initiated by system/landlord
    # MPESA_C2B = "MPESA_C2B" # If system directly receives C2B notifications for landlord's paybill/till
    # BANK_TRANSFER = "BANK_TRANSFER" # For tracking expected bank transfers
    OTHER_GENERIC_GATEWAY = "OTHER_GENERIC_GATEWAY" # Fallback for other integrated gateways
    MANUAL_BANK_TRANSFER_VERIFICATION = "MANUAL_BANK_TRANSFER_VERIFICATION" # Matches previous use in GatewayTransaction

class MpesaShortcodeType(enum.Enum):
    PAYBILL = "PAYBILL"
    TILL_NUMBER = "TILL_NUMBER" # Business Till / Buy Goods Till
    NONE = "NONE" # If landlord isn't configuring M-Pesa for direct collection or STK

class GatewayEnvironment(enum.Enum):
    SANDBOX = "SANDBOX"
    PRODUCTION = "PRODUCTION"
    TESTING = "TESTING" # Generic testing if not sandbox/prod

class ReminderRuleEvent(enum.Enum):
    RENT_DUE_DATE = "RENT_DUE_DATE"
    LEASE_START_DATE = "LEASE_START_DATE"
    LEASE_END_DATE = "LEASE_END_DATE"
    INVOICE_DUE_DATE = "INVOICE_DUE_DATE" # e.g. for utility bills or other charges
    DOCUMENT_EXPIRY_DATE = "DOCUMENT_EXPIRY_DATE" # e.g. for compliance docs, insurance
    MAINTENANCE_SCHEDULED_DATE = "MAINTENANCE_SCHEDULED_DATE"

class ReminderRecipientType(enum.Enum):
    TENANT = "TENANT" # Primary tenant(s) of a lease
    LANDLORD = "LANDLORD" # The landlord user associated with the rule/property/lease
    PROPERTY_MANAGER = "PROPERTY_MANAGER" # If a distinct role or assigned staff
    OTHER_USER = "OTHER_USER" # Specify a particular system user
    CUSTOM_EMAIL = "CUSTOM_EMAIL" # Send to an email address not tied to a system user

class ReminderTimeUnit(enum.Enum):
    MINUTES = "MINUTES"
    HOURS = "HOURS"
    DAYS = "DAYS"
    WEEKS = "WEEKS"
    MONTHS = "MONTHS"

class GatewayTransactionStatus(enum.Enum):
    PENDING = "PENDING"         # Transaction initiated, awaiting confirmation from gateway
    SUCCESSFUL = "SUCCESSFUL"   # Payment confirmed by the gateway
    FAILED = "FAILED"           # Payment failed or was declined by the gateway
    CANCELLED = "CANCELLED"       # Payment was cancelled by user or system before completion at gateway
    PROCESSING = "PROCESSING"     # Gateway is still processing (e.g., some bank transfers, ACH)
    REQUIRES_ACTION = "REQUIRES_ACTION" # e.g., 3DS authentication, CAPTCHA, or other user step needed
    UNKNOWN = "UNKNOWN"           # Status could not be determined from gateway response
    REFUNDED = "REFUNDED"         # Transaction was successfully refunded via the gateway
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED" # Transaction was partially refunded


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
