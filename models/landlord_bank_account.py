from datetime import datetime
from typing import Optional
from hermitta_app import db # Import db instance
from .enums import BankAccountType # Import from shared enums

class LandlordBankAccount(db.Model):
    __tablename__ = 'landlord_bank_accounts'

    account_id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)

    bank_name = db.Column(db.String(100), nullable=False)
    account_holder_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50), nullable=False) # Consider encrypting this field
    branch_name = db.Column(db.String(100), nullable=True)
    swift_code = db.Column(db.String(20), nullable=True)
    account_type = db.Column(db.Enum(BankAccountType), default=BankAccountType.OTHER, nullable=True)

    is_primary = db.Column(db.Boolean, default=False, nullable=False, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship
    landlord = db.relationship('User', backref=db.backref('bank_accounts', lazy='dynamic'))
    # Payments received to this account are backref'd from Payment.landlord_bank_account

    def __init__(self, **kwargs):
        # Explicitly set defaults if not provided
        if 'account_type' not in kwargs:
            kwargs['account_type'] = BankAccountType.OTHER
        if 'is_primary' not in kwargs:
            kwargs['is_primary'] = False
        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.utcnow()
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = datetime.utcnow()
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<LandlordBankAccount {self.account_id} - {self.bank_name} {self.account_number} (Landlord: {self.landlord_id})>"

# Example Usage (SQLAlchemy style):
# primary_account = LandlordBankAccount(
#     landlord_id=10,
#     bank_name="Equity Bank Kenya",
#     account_holder_name="John Doe Properties Ltd",
#     account_number="1234567890123",
#     branch_name="Westlands Branch",
#     swift_code="EQBLKENA",
#     account_type=BankAccountType.BUSINESS,
#     is_primary=True
# )
# db.session.add(primary_account)
# db.session.commit()

# secondary_account = LandlordBankAccount(
#     account_id=1,
#     landlord_id=10, # Assuming landlord user_id 10
#     bank_name="Equity Bank Kenya",
#     account_holder_name="John Doe Properties Ltd",
#     account_number="1234567890123",
#     branch_name="Westlands Branch",
#     swift_code="EQBLKENA",
#     account_type=BankAccountType.BUSINESS,
#     is_primary=True
# )
#
# secondary_account = LandlordBankAccount(
#     account_id=2,
#     landlord_id=10,
#     bank_name="KCB Bank Kenya",
#     account_holder_name="John Doe",
#     account_number="0987654321098",
#     branch_name="Sarit Centre Branch",
#     swift_code="KCBLKENX",
#     account_type=BankAccountType.CHECKING,
#     is_primary=False
# )
#
# print(f"Primary Account: {primary_account.bank_name} - {primary_account.account_number}")
# print(f"Secondary Account Holder: {secondary_account.account_holder_name}, Type: {secondary_account.account_type.value if secondary_account.account_type else 'N/A'}")
