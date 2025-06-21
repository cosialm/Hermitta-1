import enum
from datetime import datetime, date
from typing import Optional # Keep for type hinting
from decimal import Decimal
from hermitta_app import db # Import db instance

class FinancialTransactionType(enum.Enum): # Should be consistent with UserFinancialCategory
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class RecurrenceFrequency(enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    ANNUALLY = "ANNUALLY"
    BI_ANNUALLY = "BI_ANNUALLY" # Every 6 months
    EVERY_TWO_MONTHS = "EVERY_TWO_MONTHS"
    # Add more as needed

class FinancialTransaction(db.Model):
    __tablename__ = 'financial_transactions'

    transaction_id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)

    type = db.Column(db.Enum(FinancialTransactionType), nullable=False)
    # TODO: category_id will be FK to UserFinancialCategory.user_financial_category_id when that model is defined
    category_id = db.Column(db.Integer, nullable=False, index=True)

    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False) # Max 9,999,999,999.99. Always positive.
    transaction_date = db.Column(db.Date, nullable=False, index=True)

    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'), nullable=True, index=True)
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.lease_id'), nullable=True, index=True)

    # TODO: related_payment_id will be FK to Payment.payment_id (if Payment model is distinct or part of this)
    related_payment_id = db.Column(db.Integer, nullable=True, index=True)
    # TODO: maintenance_request_id will be FK to MaintenanceRequest.request_id
    maintenance_request_id = db.Column(db.Integer, nullable=True, index=True)
    # TODO: document_id will be FK to Document.document_id
    document_id = db.Column(db.Integer, nullable=True, index=True)

    vendor_name = db.Column(db.String(100), nullable=True) # For expenses, if not linked to a Vendor User
    sub_category = db.Column(db.String(100), nullable=True)

    # Recurrence fields
    is_recurring = db.Column(db.Boolean, default=False, nullable=False)
    recurrence_frequency = db.Column(db.Enum(RecurrenceFrequency), nullable=True)
    recurrence_end_date = db.Column(db.Date, nullable=True)
    next_due_date = db.Column(db.Date, nullable=True, index=True) # For the master recurring transaction record

    parent_recurring_transaction_id = db.Column(db.Integer, db.ForeignKey('financial_transactions.transaction_id'), nullable=True)

    is_tax_deductible_candidate = db.Column(db.Boolean, default=False, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    landlord = db.relationship('User', backref=db.backref('financial_transactions', lazy='dynamic'))
    property = db.relationship('Property', backref=db.backref('financial_transactions', lazy='dynamic'))
    lease = db.relationship('Lease', backref=db.backref('financial_transactions', lazy='dynamic'))

    # Relationship to the Payment model
    # A financial transaction can be directly related to a specific payment record.
    related_payment = db.relationship('Payment',
                                      foreign_keys=[related_payment_id],
                                      backref=db.backref('financial_entries', lazy='dynamic'))

    # Self-referential relationship for recurring transactions
    child_transactions = db.relationship('FinancialTransaction',
                                         backref=db.backref('parent_transaction', remote_side=[transaction_id]),
                                         lazy='dynamic')

    # TODO: Add relationships for category, maintenance_request, document when those models are converted/confirmed.

    def __repr__(self):
        return f"<FinancialTransaction {self.transaction_id}: {self.description} ({self.type.value} {self.amount})>"

# Example Usage (would be done via db.session)
# master_bill_data = {
#     "landlord_id": 1, "type": FinancialTransactionType.EXPENSE, "category_id": 5,
#     "description": "Property XYZ Internet Bill (Safaricom Fiber)", "amount": Decimal("5000.00"),
#     "transaction_date": date(2024,1,10), "property_id": 1,
#     "is_recurring": True, "recurrence_frequency": RecurrenceFrequency.MONTHLY,
#     "next_due_date": date(2024,2,10)
# }
# master_bill = FinancialTransaction(**master_bill_data)
# # db.session.add(master_bill)
# # db.session.commit() # to get master_bill.transaction_id
#
# feb_bill_data = {
#     "landlord_id": 1, "type": FinancialTransactionType.EXPENSE, "category_id": 5,
#     "description": "Property XYZ Internet Bill (Safaricom Fiber) - Feb 2024", "amount": Decimal("5000.00"),
#     "transaction_date": date(2024,2,10), "property_id": 1,
#     # "parent_recurring_transaction_id": master_bill.transaction_id, # after commit
#     "document_id": 201
# }
# feb_bill = FinancialTransaction(**feb_bill_data)
# # db.session.add(feb_bill)
# # db.session.commit()
