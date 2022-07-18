"""'InitialMigration'

Revision ID: f94e02ac1a55
Revises: 
Create Date: 2022-07-04 14:38:01.962091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f94e02ac1a55'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('detailed_network_revenue_chart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year_num', sa.Integer(), nullable=True),
    sa.Column('month_num', sa.Integer(), nullable=True),
    sa.Column('total_revenue', sa.Float(), nullable=True),
    sa.Column('total_data', sa.Float(), nullable=True),
    sa.Column('total_voice', sa.Float(), nullable=True),
    sa.Column('total_out_duration', sa.Float(), nullable=True),
    sa.Column('incoming_duration', sa.Float(), nullable=True),
    sa.Column('total_mb', sa.Float(), nullable=True),
    sa.Column('in_bound_roam_duration', sa.Float(), nullable=True),
    sa.Column('national_roam_duration', sa.Float(), nullable=True),
    sa.Column('roam_data_mb', sa.Float(), nullable=True),
    sa.Column('out_international_egp', sa.Float(), nullable=True),
    sa.Column('in_bound_roaming_rev_egp', sa.Float(), nullable=True),
    sa.Column('national_roaming_rev_egp', sa.Float(), nullable=True),
    sa.Column('roaming_data', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('detailed_sites_revenue_with_technology_chart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year_num', sa.Integer(), nullable=True),
    sa.Column('month_num', sa.Integer(), nullable=True),
    sa.Column('site_code_dwh', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('total_revenue', sa.Float(), nullable=True),
    sa.Column('total_data', sa.Float(), nullable=True),
    sa.Column('total_voice', sa.Float(), nullable=True),
    sa.Column('total_out_duration', sa.Float(), nullable=True),
    sa.Column('incoming_duration', sa.Float(), nullable=True),
    sa.Column('total_mb', sa.Float(), nullable=True),
    sa.Column('in_bound_roam_duration', sa.Float(), nullable=True),
    sa.Column('national_roam_duration', sa.Float(), nullable=True),
    sa.Column('roam_data_mb', sa.Float(), nullable=True),
    sa.Column('out_international_egp', sa.Float(), nullable=True),
    sa.Column('in_bound_roaming_rev_egp', sa.Float(), nullable=True),
    sa.Column('national_roaming_rev_egp', sa.Float(), nullable=True),
    sa.Column('roaming_data', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('merged_revenue_tech_with_technology', sa.Column('id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('merged_revenue_tech_with_technology', 'id')
    op.drop_table('detailed_sites_revenue_with_technology_chart')
    op.drop_table('detailed_network_revenue_chart')
    # ### end Alembic commands ###
