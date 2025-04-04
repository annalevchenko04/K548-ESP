"""Initial migration

Revision ID: ebe8d57febd6
Revises: 
Create Date: 2025-03-26 16:43:46.896732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ebe8d57febd6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_phone', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_favorites_post_id', table_name='favorites')
    op.drop_index('ix_favorites_user_id', table_name='favorites')
    op.drop_table('favorites')
    op.drop_table('admins')
    op.drop_index('ix_avatars_id', table_name='avatars')
    op.drop_table('avatars')
    op.drop_index('ix_posts_id', table_name='posts')
    op.drop_table('posts')
    op.drop_index('ix_carbon_footprint_id', table_name='carbon_footprint')
    op.drop_table('carbon_footprint')
    op.drop_index('ix_companies_id', table_name='companies')
    op.drop_table('companies')
    op.drop_index('ix_images_id', table_name='images')
    op.drop_table('images')
    op.drop_table('members')
    op.drop_index('ix_interactive_questions_id', table_name='interactive_questions')
    op.drop_table('interactive_questions')
    op.drop_index('ix_comments_id', table_name='comments')
    op.drop_table('comments')
    op.drop_index('ix_user_answers_id', table_name='user_answers')
    op.drop_table('user_answers')
    op.drop_index('ix_user_badges_id', table_name='user_badges')
    op.drop_table('user_badges')
    op.drop_index('ix_badges_id', table_name='badges')
    op.drop_table('badges')
    op.drop_index('ix_carbon_footprint_details_id', table_name='carbon_footprint_details')
    op.drop_table('carbon_footprint_details')
    op.drop_index('ix_events_id', table_name='events')
    op.drop_table('events')
    op.drop_index('ix_bookings_id', table_name='bookings')
    op.drop_table('bookings')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bookings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], name='bookings_event_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='bookings_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='bookings_pkey')
    )
    op.create_index('ix_bookings_id', 'bookings', ['id'], unique=False)
    op.create_table('events',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('time', postgresql.TIME(), autoincrement=False, nullable=True),
    sa.Column('duration', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('event_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_personal_training', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('max_participants', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('room_number', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('creator_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], name='events_creator_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='events_pkey')
    )
    op.create_index('ix_events_id', 'events', ['id'], unique=False)
    op.create_table('carbon_footprint_details',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('footprint_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('value', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['footprint_id'], ['carbon_footprint.id'], name='carbon_footprint_details_footprint_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='carbon_footprint_details_pkey')
    )
    op.create_index('ix_carbon_footprint_details_id', 'carbon_footprint_details', ['id'], unique=False)
    op.create_table('badges',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('badges_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='badges_pkey'),
    sa.UniqueConstraint('name', name='badges_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_badges_id', 'badges', ['id'], unique=False)
    op.create_table('user_badges',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('badge_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['badge_id'], ['badges.id'], name='user_badges_badge_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_badges_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_badges_pkey')
    )
    op.create_index('ix_user_badges_id', 'user_badges', ['id'], unique=False)
    op.create_table('user_answers',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('question_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('answer', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['interactive_questions.id'], name='user_answers_question_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_answers_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_answers_pkey')
    )
    op.create_index('ix_user_answers_id', 'user_answers', ['id'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='comments_post_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='comments_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='comments_pkey')
    )
    op.create_index('ix_comments_id', 'comments', ['id'], unique=False)
    op.create_table('interactive_questions',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('input_type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('options', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('next_question_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['next_question_id'], ['interactive_questions.id'], name='interactive_questions_next_question_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='interactive_questions_pkey')
    )
    op.create_index('ix_interactive_questions_id', 'interactive_questions', ['id'], unique=False)
    op.create_table('members',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('membership_status', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id'], ['users.id'], name='members_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='members_pkey')
    )
    op.create_table('images',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('upload_date', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='images_post_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='images_pkey')
    )
    op.create_index('ix_images_id', 'images', ['id'], unique=False)
    op.create_table('companies',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('companies_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('industry', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('domain', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='companies_pkey'),
    sa.UniqueConstraint('domain', name='companies_domain_key'),
    sa.UniqueConstraint('name', name='companies_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_companies_id', 'companies', ['id'], unique=False)
    op.create_table('carbon_footprint',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('total_footprint', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='carbon_footprint_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='carbon_footprint_pkey')
    )
    op.create_index('ix_carbon_footprint_id', 'carbon_footprint', ['id'], unique=False)
    op.create_table('posts',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('posts_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('category', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('tags', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='posts_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='posts_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_posts_id', 'posts', ['id'], unique=False)
    op.create_table('avatars',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('upload_date', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='avatars_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='avatars_pkey')
    )
    op.create_index('ix_avatars_id', 'avatars', ['id'], unique=False)
    op.create_table('admins',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id'], ['users.id'], name='admins_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='admins_pkey')
    )
    op.create_table('favorites',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='favorites_post_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='favorites_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='favorites_pkey'),
    sa.UniqueConstraint('user_id', 'post_id', name='unique_favorite')
    )
    op.create_index('ix_favorites_user_id', 'favorites', ['user_id'], unique=False)
    op.create_index('ix_favorites_post_id', 'favorites', ['post_id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('surname', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('gender', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('role', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.CheckConstraint("gender::text = ANY (ARRAY['male'::character varying, 'female'::character varying]::text[])", name='check_valid_genders'),
    sa.CheckConstraint("role::text = ANY (ARRAY['admin'::character varying, 'member'::character varying]::text[])", name='check_valid_roles'),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name='users_company_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_phone', 'users', ['phone'], unique=True)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    # ### end Alembic commands ###