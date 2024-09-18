"""Coin bot table updated - curated

Revision ID: 74a6ad6c13d3
Revises: 1ef11a055306
Create Date: 2024-09-10 09:09:56.361632

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74a6ad6c13d3'
down_revision: Union[str, None] = '1ef11a055306'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_columns = inspector.get_columns('coin_bot')
    existing_column_names = [col['name'] for col in existing_columns]

    if 'name' not in existing_column_names:
        op.add_column('coin_bot', sa.Column('name', sa.String(), nullable=True))
    
    if 'alias' not in existing_column_names:
        op.add_column('coin_bot', sa.Column('alias', sa.String(), nullable=True))
    
    if 'icon' not in existing_column_names:
        op.add_column('coin_bot', sa.Column('icon', sa.String(), nullable=True))
    
    if 'background_color' not in existing_column_names:
        op.add_column('coin_bot', sa.Column('background_color', sa.String(), nullable=True))
    
    if 'image' in existing_column_names:
        op.drop_column('coin_bot', 'image')
    
    if 'bot_name' in existing_column_names:
        op.drop_column('coin_bot', 'bot_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_columns = inspector.get_columns('coin_bot')
    existing_column_names = [col['name'] for col in existing_columns]

    if 'bot_name' not in existing_column_names:
        op.add_column('coin_bot', sa.Column('bot_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    
    if 'image' not in existing_column_names:
        op.add_column('coin_bot', sa.Column('image', sa.VARCHAR(), autoincrement=False, nullable=True))
    
    if 'background_color' in existing_column_names:
        op.drop_column('coin_bot', 'background_color')
    
    if 'icon' in existing_column_names:
        op.drop_column('coin_bot', 'icon')
    
    if 'alias' in existing_column_names:
        op.drop_column('coin_bot', 'alias')
    
    if 'name' in existing_column_names:
        op.drop_column('coin_bot', 'name')
    # ### end Alembic commands ###


# def upgrade() -> None:
#     # ### commands auto generated by Alembic - please adjust! ###
#     op.add_column('coin_bot', sa.Column('name', sa.String(), nullable=True))
#     op.add_column('coin_bot', sa.Column('alias', sa.String(), nullable=True))
#     op.add_column('coin_bot', sa.Column('icon', sa.String(), nullable=True))
#     op.add_column('coin_bot', sa.Column('background_color', sa.String(), nullable=True))
#     op.drop_column('coin_bot', 'image')
#     op.drop_column('coin_bot', 'bot_name')
#     # ### end Alembic commands ###


# def downgrade() -> None:
#     # ### commands auto generated by Alembic - please adjust! ###
#     op.add_column('coin_bot', sa.Column('bot_name', sa.VARCHAR(), autoincrement=False, nullable=True))
#     op.add_column('coin_bot', sa.Column('image', sa.VARCHAR(), autoincrement=False, nullable=True))
#     op.drop_column('coin_bot', 'background_color')
#     op.drop_column('coin_bot', 'icon')
#     op.drop_column('coin_bot', 'alias')
#     op.drop_column('coin_bot', 'name')
#     # ### end Alembic commands ###
