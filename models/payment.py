from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from hermitta_app import db # Main SQLAlchemy db instance
from .enums import PaymentMethod, PaymentStatus # Import from new enums file
from .landlord_bank_account import LandlordBankAccount # Explicit import

class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.lease_id'), nullable=False, index=True)

    expected_amount = db.Column(db.Numeric(12, 2), nullable=False) # Amount expected
    due_date = db.Column(db.Date, nullable=True, index=True) # When this payment is due

    payment_method = db.Column(db.Enum(PaymentMethod), nullable=True)
    amount_paid = db.Column(db.Numeric(12, 2), nullable=True) # Actual amount paid
    payment_date = db.Column(db.Date, nullable=True, index=True) # Actual date payment was made/confirmed

    status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.EXPECTED, nullable=False, index=True)

    # Foreign keys for users involved
    recorded_by_landlord_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True, index=True)
    initiated_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True, index=True) # e.g., Tenant or System

    # Link to gateway transaction if applicable
    gateway_transaction_id = db.Column(db.Integer, db.ForeignKey('gateway_transactions.transaction_id'), nullable=True, index=True)

    # Link to landlord's bank account if payment was a direct deposit
    landlord_bank_account_id = db.Column(db.Integer, db.ForeignKey('landlord_bank_accounts.account_id'), nullable=True, index=True)
    bank_transaction_id = db.Column(db.String(255), nullable=True) # Bank's reference for the transaction, if manual deposit

    reference_number = db.Column(db.String(255), nullable=True) # For manual methods or external ref (e.g., cheque number)
    payer_narration = db.Column(db.Text, nullable=True) # Tenant's narration for a transfer, or general notes from payer
    notes = db.Column(db.Text, nullable=True) # Internal notes by landlord/system

    # System-generated unique code that tenant can use for payment, helps in reconciliation
    payment_reference_code = db.Column(db.String(50), nullable=True, unique=True, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    lease = db.relationship('Lease', backref=db.backref('payments', lazy='dynamic'))
    recorded_by_landlord = db.relationship('User', foreign_keys=[recorded_by_landlord_id], backref=db.backref('recorded_payments', lazy='dynamic'))
    initiated_by_user = db.relationship('User', foreign_keys=[initiated_by_user_id], backref=db.backref('initiated_payments', lazy='dynamic'))

    # Relationship to GatewayTransaction (to be defined in gateway_transaction.py)
    # gateway_transaction = db.relationship('GatewayTransaction', backref='payment', uselist=False) # One-to-one or one-to-many if retries create new gtx

    # Relationship to LandlordBankAccount (assuming LandlordBankAccount model exists)
    landlord_bank_account = db.relationship('LandlordBankAccount', backref=db.backref('payments_received', lazy='dynamic'))

    # Relationship to FinancialTransaction (a payment can result in one or more financial transactions)
    # financial_transactions = db.relationship('FinancialTransaction', backref='related_payment_obj', lazy='dynamic', foreign_keys='FinancialTransaction.related_payment_id')


    def __repr__(self):
        return f"<Payment {self.payment_id} for Lease {self.lease_id} - Amount: {self.expected_amount} Status: {self.status.value}>"

# Placeholder for LandlordBankAccount to satisfy relationship, actual model should be in its own file.
# class LandlordBankAccount(db.Model):
#     __tablename__ = 'landlord_bank_accounts'
#     account_id = db.Column(db.Integer, primary_key=True)
#     # ... other fields ...

# Note: The GatewayTransaction model and its relationship will be fully defined in models/gateway_transaction.py.
# The FinancialTransaction relationship will be updated in models/financial_transaction.py.
# Ensure Lease and User models are correctly defined and imported by SQLAlchemy when the app runs.
