"""Re-sync database schema

Revision ID: 922df20d66ff
Revises: ed76f5dc38dc
Create Date: 2024-09-11 14:58:25.740043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '922df20d66ff'
down_revision: Union[str, None] = 'ed76f5dc38dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_apscheduler_jobs_next_run_time', table_name='apscheduler_jobs')
    op.drop_table('apscheduler_jobs')
    op.drop_constraint('alert_coin_bot_id_fkey', 'alert', type_='foreignkey')
    op.create_foreign_key(None, 'alert', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.add_column('analysis', sa.Column('image_url', sa.String(), nullable=True))
    op.drop_constraint('analysis_coin_bot_id_fkey', 'analysis', type_='foreignkey')
    op.create_foreign_key(None, 'analysis', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.alter_column('analysis_image', 'image',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_constraint('article_coin_bot_id_fkey', 'article', type_='foreignkey')
    op.create_foreign_key(None, 'article', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.drop_constraint('blacklist_coin_bot_id_fkey', 'blacklist', type_='foreignkey')
    op.create_foreign_key(None, 'blacklist', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.drop_column('category', 'name')
    op.drop_column('category', 'alias')
    op.drop_constraint('chart_coin_bot_id_fkey', 'chart', type_='foreignkey')
    op.create_foreign_key(None, 'chart', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.add_column('coin_bot', sa.Column('bot_name', sa.String(), nullable=True))
    op.add_column('coin_bot', sa.Column('image', sa.String(), nullable=True))
    op.alter_column('coin_bot', 'category_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('coin_bot_category_id_fkey', 'coin_bot', type_='foreignkey')
    op.create_foreign_key(None, 'coin_bot', 'category', ['category_id'], ['category_id'])
    op.drop_column('coin_bot', 'name')
    op.drop_column('coin_bot', 'alias')
    op.drop_column('coin_bot', 'icon')
    op.drop_column('coin_bot', 'background_color')
    op.drop_column('coin_bot', 'is_active')
    op.drop_constraint('competitor_coin_bot_id_fkey', 'competitor', type_='foreignkey')
    op.create_foreign_key(None, 'competitor', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.drop_constraint('dapps_coin_bot_id_fkey', 'dapps', type_='foreignkey')
    op.create_foreign_key(None, 'dapps', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.drop_constraint('hacks_coin_bot_id_fkey', 'hacks', type_='foreignkey')
    op.create_foreign_key(None, 'hacks', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.drop_constraint('introduction_coin_bot_id_fkey', 'introduction', type_='foreignkey')
    op.create_foreign_key(None, 'introduction', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.drop_constraint('keyword_coin_bot_id_fkey', 'keyword', type_='foreignkey')
    op.create_foreign_key(None, 'keyword', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.add_column('narrative_trading', sa.Column('image_url', sa.String(), nullable=True))
    op.drop_constraint('narrative_trading_coin_bot_id_fkey', 'narrative_trading', type_='foreignkey')
    op.create_foreign_key(None, 'narrative_trading', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.drop_constraint('revenue_model_coin_bot_id_fkey', 'revenue_model', type_='foreignkey')
    op.create_foreign_key(None, 'revenue_model', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.drop_constraint('site_coin_bot_id_fkey', 'site', type_='foreignkey')
    op.create_foreign_key(None, 'site', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.drop_constraint('token_distribution_coin_bot_id_fkey', 'token_distribution', type_='foreignkey')
    op.create_foreign_key(None, 'token_distribution', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.drop_constraint('token_utility_coin_bot_id_fkey', 'token_utility', type_='foreignkey')
    op.create_foreign_key(None, 'token_utility', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.drop_constraint('tokenomics_coin_bot_id_fkey', 'tokenomics', type_='foreignkey')
    op.create_foreign_key(None, 'tokenomics', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.drop_constraint('top_story_coin_bot_id_fkey', 'top_story', type_='foreignkey')
    op.create_foreign_key(None, 'top_story', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.drop_constraint('upgrades_coin_bot_id_fkey', 'upgrades', type_='foreignkey')
    op.create_foreign_key(None, 'upgrades', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    op.alter_column('user_table', 'nickname',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user_table', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user_table', 'email_verified',
               existing_type=sa.VARCHAR(),
               type_=sa.Boolean(),
               existing_nullable=True,
               postgresql_using='email_verified::boolean')
    op.alter_column('user_table', 'auth_token',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_unique_constraint(None, 'user_table', ['email'])
    op.create_unique_constraint(None, 'user_table', ['nickname'])
    op.create_unique_constraint(None, 'user_table', ['auth_token'])
    op.drop_constraint('value_accrual_mechanisms_coin_bot_id_fkey', 'value_accrual_mechanisms', type_='foreignkey')
    op.create_foreign_key(None, 'value_accrual_mechanisms', 'coin_bot', ['coin_bot_id'], ['bot_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'value_accrual_mechanisms', type_='foreignkey')
    op.create_foreign_key('value_accrual_mechanisms_coin_bot_id_fkey', 'value_accrual_mechanisms', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_constraint(None, 'user_table', type_='unique')
    op.drop_constraint(None, 'user_table', type_='unique')
    op.drop_constraint(None, 'user_table', type_='unique')
    op.alter_column('user_table', 'auth_token',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user_table', 'email_verified',
               existing_type=sa.Boolean(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.alter_column('user_table', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user_table', 'nickname',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'upgrades', type_='foreignkey')
    op.create_foreign_key('upgrades_coin_bot_id_fkey', 'upgrades', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_constraint(None, 'top_story', type_='foreignkey')
    op.create_foreign_key('top_story_coin_bot_id_fkey', 'top_story', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_constraint(None, 'tokenomics', type_='foreignkey')
    op.create_foreign_key('tokenomics_coin_bot_id_fkey', 'tokenomics', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_constraint(None, 'token_utility', type_='foreignkey')
    op.create_foreign_key('token_utility_coin_bot_id_fkey', 'token_utility', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_constraint(None, 'token_distribution', type_='foreignkey')
    op.create_foreign_key('token_distribution_coin_bot_id_fkey', 'token_distribution', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_constraint(None, 'site', type_='foreignkey')
    op.create_foreign_key('site_coin_bot_id_fkey', 'site', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_constraint(None, 'revenue_model', type_='foreignkey')
    op.create_foreign_key('revenue_model_coin_bot_id_fkey', 'revenue_model', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_constraint(None, 'narrative_trading', type_='foreignkey')
    op.create_foreign_key('narrative_trading_coin_bot_id_fkey', 'narrative_trading', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_column('narrative_trading', 'image_url')
    op.drop_constraint(None, 'keyword', type_='foreignkey')
    op.create_foreign_key('keyword_coin_bot_id_fkey', 'keyword', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_constraint(None, 'introduction', type_='foreignkey')
    op.create_foreign_key('introduction_coin_bot_id_fkey', 'introduction', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_constraint(None, 'hacks', type_='foreignkey')
    op.create_foreign_key('hacks_coin_bot_id_fkey', 'hacks', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_constraint(None, 'dapps', type_='foreignkey')
    op.create_foreign_key('dapps_coin_bot_id_fkey', 'dapps', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_constraint(None, 'competitor', type_='foreignkey')
    op.create_foreign_key('competitor_coin_bot_id_fkey', 'competitor', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.add_column('coin_bot', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('coin_bot', sa.Column('background_color', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('coin_bot', sa.Column('icon', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('coin_bot', sa.Column('alias', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('coin_bot', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'coin_bot', type_='foreignkey')
    op.create_foreign_key('coin_bot_category_id_fkey', 'coin_bot', 'category', ['category_id'], ['category_id'], ondelete='CASCADE')
    op.alter_column('coin_bot', 'category_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('coin_bot', 'image')
    op.drop_column('coin_bot', 'bot_name')
    op.drop_constraint(None, 'chart', type_='foreignkey')
    op.create_foreign_key('chart_coin_bot_id_fkey', 'chart', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.add_column('category', sa.Column('alias', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('category', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'blacklist', type_='foreignkey')
    op.create_foreign_key('blacklist_coin_bot_id_fkey', 'blacklist', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_constraint(None, 'article', type_='foreignkey')
    op.create_foreign_key('article_coin_bot_id_fkey', 'article', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.alter_column('analysis_image', 'image',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'analysis', type_='foreignkey')
    op.create_foreign_key('analysis_coin_bot_id_fkey', 'analysis', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.drop_column('analysis', 'image_url')
    op.drop_constraint(None, 'alert', type_='foreignkey')
    op.create_foreign_key('alert_coin_bot_id_fkey', 'alert', 'coin_bot', ['coin_bot_id'], ['bot_id'], ondelete='CASCADE')
    op.create_table('apscheduler_jobs',
    sa.Column('id', sa.VARCHAR(length=191), autoincrement=False, nullable=False),
    sa.Column('next_run_time', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('job_state', postgresql.BYTEA(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='apscheduler_jobs_pkey')
    )
    op.create_index('ix_apscheduler_jobs_next_run_time', 'apscheduler_jobs', ['next_run_time'], unique=False)
    # ### end Alembic commands ###
