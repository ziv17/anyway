"""Add cbs_cities table to hold data from cities.csv

Revision ID: fe6dcd0178f7
Revises: fd0c85b6d1bf
Create Date: 2022-04-26 20:41:18.049443

"""

# revision identifiers, used by Alembic.
revision = 'fe6dcd0178f7'
down_revision = 'fd0c85b6d1bf'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table("cbs_cities",
                    sa.Column('heb_name', sa.String()),
                    sa.Column('symbol', sa.Integer(), primary_key=True),
                    sa.Column('eng_name', sa.String()),
                    sa.Column('district', sa.Integer()),
                    sa.Column('napa', sa.Integer()),
                    sa.Column('natural_zone', sa.Integer(), nullable=True),
                    sa.Column('municipal_stance', sa.Integer(), nullable=True),
                    sa.Column('metropolitan', sa.Integer(), nullable=True),
                    sa.Column('religion', sa.Integer(), nullable=True),
                    sa.Column('population', sa.Integer(), nullable=True),
                    sa.Column('other', sa.Float(), nullable=True),
                    sa.Column('jews', sa.Float(), nullable=True),
                    sa.Column('arab', sa.Float(), nullable=True),
                    sa.Column('founded', sa.Integer(), nullable=True),
                    sa.Column('tzura', sa.Integer(), nullable=True),
                    sa.Column('irgun', sa.Integer(), nullable=True),
                    sa.Column('center', sa.Integer(), nullable=True),
                    sa.Column('altitude', sa.Integer(), nullable=True),
                    sa.Column('planning', sa.Integer(), nullable=True),
                    sa.Column('police', sa.Integer(), nullable=True),
                    sa.Column('year', sa.Integer(), nullable=True),
                    sa.Column('taatik', sa.String(), nullable=True),
                    )
    op.create_index('cbs_cities_symbol_idx', "cbs_cities", ['symbol'], unique=True)
    op.create_index('cbs_cities_eng_name_idx', "cbs_cities", ['eng_name'], unique=True)
    op.create_index('cbs_cities_heb_name_idx', "cbs_cities", ['heb_name'], unique=True)


def downgrade():
    op.drop_index(op.f(), table_name='cbs_cities_symbol_idx')
    op.drop_index(op.f(), table_name='cbs_cities_eng_name_idx')
    op.drop_index(op.f(), table_name='cbs_cities_heb_name_idx')
    op.drop_table("cbs_cities")
