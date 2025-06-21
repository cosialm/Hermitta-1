from datetime import datetime
from typing import Optional
from hermitta_app import db # Import db instance

class DocumentFolder(db.Model):
    __tablename__ = 'document_folders'

    folder_id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)

    # Self-referential foreign key for nested folders
    parent_folder_id = db.Column(db.Integer, db.ForeignKey('document_folders.folder_id'), nullable=True, index=True)

    # Optional: Link folder to a specific property if all its contents are property-specific
    # property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'), nullable=True, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    landlord = db.relationship('User', backref=db.backref('document_folders', lazy='dynamic'))
    parent_folder = db.relationship('DocumentFolder', remote_side=[folder_id], backref=db.backref('subfolders', lazy='dynamic'))
    documents = db.relationship('Document', backref='folder', lazy='dynamic')
    # If property_id is added:
    # property = db.relationship('Property', backref=db.backref('document_folders', lazy='dynamic'))

    def __init__(self, **kwargs):
        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.utcnow()
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = datetime.utcnow()
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<DocumentFolder {self.folder_id} '{self.name}' by Landlord {self.landlord_id}>"

# Example Usage (SQLAlchemy style):
# root_folder_leases = DocumentFolder(
#     landlord_id=10, name="All Lease Agreements"
# )
# db.session.add(root_folder_leases)
# db.session.commit() # folder_id will be auto-populated
#
# property_A_folder = DocumentFolder(
#     landlord_id=10, name="Property A (123 Main St)"
# )
# db.session.add(property_A_folder)
# db.session.commit()
#
# property_A_leases_subfolder = DocumentFolder(
#     landlord_id=10, name="Lease Agreements", parent_folder_id=property_A_folder.folder_id
# )
# db.session.add(property_A_leases_subfolder)
# db.session.commit()
#
# print(root_folder_leases.name)
# print(f"Folder '{property_A_leases_subfolder.name}' is inside '{property_A_folder.name}' (ID: {property_A_leases_subfolder.parent_folder_id})")
