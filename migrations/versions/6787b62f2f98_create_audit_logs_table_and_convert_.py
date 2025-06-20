"""create audit_logs table and convert AuditLog to SQLAlchemy model

Revision ID: 6787b62f2f98
Revises: fb735da4134d
Create Date: 2025-06-21 05:18:04.630929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6787b62f2f98'
down_revision = 'fb735da4134d'
branch_labels = None
depends_on = None

# Define SA Enums based on models.enums
audit_log_event_enum = sa.Enum(
    'USER_REGISTERED', 'USER_LOGIN_SUCCESS', 'USER_LOGIN_FAILURE', 'USER_LOGOUT',
    'USER_PASSWORD_CHANGED', 'USER_PASSWORD_RESET_REQUEST', 'USER_PASSWORD_RESET_SUCCESS',
    'USER_PROFILE_UPDATED', 'USER_ROLE_CHANGED', 'USER_ACCOUNT_STATUS_CHANGED',
    'EMAIL_VERIFICATION_SENT', 'EMAIL_VERIFIED', 'PHONE_VERIFICATION_OTP_SENT', 'PHONE_VERIFIED',
    'MFA_SETUP_INITIATED', 'MFA_SETUP_COMPLETED', 'MFA_REMOVED',
    'MFA_CHALLENGE_SUCCESS', 'MFA_CHALLENGE_FAILURE',
    'ENTITY_CREATED', 'ENTITY_UPDATED', 'ENTITY_DELETED', 'ENTITY_STATUS_CHANGED',
    'SECURITY_ALERT', 'CONFIGURATION_CHANGE', 'SYSTEM_ERROR', 'ADMIN_ACTION', 'OTHER',
    name='auditlogevent'
)
audit_action_category_enum = sa.Enum(
    'AUTHENTICATION', 'USER_MANAGEMENT', 'PROPERTY_MANAGEMENT', 'LEASE_MANAGEMENT',
    'FINANCIAL_MANAGEMENT', 'MAINTENANCE_MANAGEMENT', 'DOCUMENT_MANAGEMENT',
    'COMMUNICATION', 'SYSTEM_CONFIGURATION', 'SECURITY_EVENT', 'ADMIN_ACTION',
    'JOB_EXECUTION', 'OTHER',
    name='auditactioncategory'
)
audit_action_status_enum = sa.Enum('SUCCESS', 'FAILURE', 'PENDING', name='auditactionstatus')


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audit_logs',
    sa.Column('log_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('event_type', audit_log_event_enum, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('action_category', audit_action_category_enum, nullable=True),
    sa.Column('details', sa.JSON(), nullable=True),
    sa.Column('target_entity_type', sa.String(length=100), nullable=True),
    sa.Column('target_entity_id', sa.String(length=100), nullable=True),
    sa.Column('ip_address', sa.String(length=45), nullable=True),
    sa.Column('user_agent', sa.String(length=255), nullable=True),
    sa.Column('status', audit_action_status_enum, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name=op.f('fk_audit_logs_user_id_users')),
    sa.PrimaryKeyConstraint('log_id', name=op.f('pk_audit_logs'))
    )
    op.create_index(op.f('ix_audit_logs_action_category'), 'audit_logs', ['action_category'], unique=False)
    op.create_index(op.f('ix_audit_logs_event_type'), 'audit_logs', ['event_type'], unique=False)
    op.create_index(op.f('ix_audit_logs_status'), 'audit_logs', ['status'], unique=False)
    op.create_index(op.f('ix_audit_logs_target_entity_id'), 'audit_logs', ['target_entity_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_target_entity_type'), 'audit_logs', ['target_entity_type'], unique=False)
    op.create_index(op.f('ix_audit_logs_timestamp'), 'audit_logs', ['timestamp'], unique=False)
    op.create_index(op.f('ix_audit_logs_user_id'), 'audit_logs', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_audit_logs_user_id'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_timestamp'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_target_entity_type'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_target_entity_id'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_status'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_event_type'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_action_category'), table_name='audit_logs')
    op.drop_table('audit_logs')
    # Commenting out enum drops for SQLite compatibility
    # audit_log_event_enum.drop(op.get_bind(), checkfirst=False)
    # audit_action_category_enum.drop(op.get_bind(), checkfirst=False)
    # audit_action_status_enum.drop(op.get_bind(), checkfirst=False)
    # ### end Alembic commands ###
