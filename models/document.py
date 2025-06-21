from datetime import datetime, date
from typing import Optional, List
from hermitta_app import db # Import db instance
from .enums import DocumentType # Import from shared enums

class Document(db.Model):
    __tablename__ = 'documents'

    document_id = db.Column(db.Integer, primary_key=True)
    uploader_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)

    document_name = db.Column(db.String(255), nullable=False)
    document_type = db.Column(db.Enum(DocumentType), nullable=False, index=True)

    file_url = db.Column(db.String(1024), nullable=False) # URL to the stored file
    file_mime_type = db.Column(db.String(100), nullable=True)
    file_size_bytes = db.Column(db.Integer, nullable=True)

    description = db.Column(db.Text, nullable=True)

    # Contextual Links (Optional Foreign Keys)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'), nullable=True, index=True)
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.lease_id'), nullable=True, index=True)
    rental_application_id = db.Column(db.Integer, db.ForeignKey('rental_applications.application_id'), nullable=True, index=True)
    maintenance_request_id = db.Column(db.Integer, db.ForeignKey('maintenance_requests.request_id'), nullable=True, index=True)
    financial_transaction_id = db.Column(db.Integer, db.ForeignKey('financial_transactions.transaction_id'), nullable=True, index=True)

    folder_id = db.Column(db.Integer, db.ForeignKey('document_folders.folder_id'), nullable=True, index=True) # FK to DocumentFolder

    tags = db.Column(db.JSON, nullable=True, default=lambda: []) # List of strings, e.g., ["unit-5a", "tax-2023", "invoice"]

    expiry_date = db.Column(db.Date, nullable=True, index=True) # For documents like insurance policies
    reminder_date_for_expiry = db.Column(db.Date, nullable=True) # System can notify user before expiry

    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    uploader = db.relationship('User', backref=db.backref('uploaded_documents', lazy='dynamic'))
    property = db.relationship('Property', backref=db.backref('documents', lazy='dynamic'))
    lease = db.relationship('Lease', backref=db.backref('documents', lazy='dynamic'))
    # rental_application = db.relationship('RentalApplication', backref=db.backref('documents', lazy='dynamic')) # Ensure RentalApplication model exists
    # maintenance_request = db.relationship('MaintenanceRequest', backref=db.backref('documents', lazy='dynamic')) # Ensure MaintenanceRequest model exists
    # financial_transaction = db.relationship('FinancialTransaction', backref=db.backref('documents', lazy='dynamic')) # Ensure FinancialTransaction model exists
    # document_folder = db.relationship('DocumentFolder', backref=db.backref('documents', lazy='dynamic')) # Ensure DocumentFolder model exists

    # Notifications related to this document are backref'd from Notification.document

    def __init__(self, **kwargs):
        if kwargs.get('tags') is None: # Handles both 'tags' not present or tags=None
            kwargs['tags'] = []
        if 'uploaded_at' not in kwargs:
            kwargs['uploaded_at'] = datetime.utcnow()
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = datetime.utcnow()
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Document {self.document_id} '{self.document_name}' Type: {self.document_type.value}>"

# Example Usage (SQLAlchemy style):
# insurance_doc = Document(
#     uploader_user_id=10,
#     document_name="Property_XYZ_Insurance_Policy_2024.pdf",
#     document_type=DocumentType.INSURANCE_POLICY_PROPERTY,
#     file_url="https://storage.example.com/docs/prop_xyz_insurance_2024.pdf",
#     property_id=101,
#     folder_id=20,
#     tags=["insurance", "property-xyz", "annual"],
#     expiry_date=date(2024, 12, 31),
#     reminder_date_for_expiry=date(2024, 11, 30)
# )
# db.session.add(insurance_doc)
# db.session.commit()

# tenant_lease_scan = Document(
#     document_id=1, uploader_user_id=10, # Landlord
#     document_name="Property_XYZ_Insurance_Policy_2024.pdf",
#     document_type=DocumentType.INSURANCE_POLICY_PROPERTY,
#     file_url="https://storage.example.com/docs/prop_xyz_insurance_2024.pdf",
#     property_id=101,
#     folder_id=20, # e.g., "Property XYZ/Legal Documents" folder
#     tags=["insurance", "property-xyz", "annual"],
#     expiry_date=date(2024, 12, 31),
#     reminder_date_for_expiry=date(2024, 11, 30)
# )
#
# tenant_lease_scan = Document(
#     document_id=2, uploader_user_id=10, # Landlord uploaded scanned copy
#     document_name="Signed_Lease_Unit1A_TenantJane.pdf",
#     document_type=DocumentType.LEASE_AGREEMENT,
#     file_url="...",
#     lease_id=501, property_id=102,
#     folder_id=22, tags=["lease", "unit-1a", "tenant-jane"]
# )
# print(insurance_doc.document_name, insurance_doc.tags, insurance_doc.expiry_date)
