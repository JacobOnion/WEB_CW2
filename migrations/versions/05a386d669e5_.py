"""empty message

Revision ID: 05a386d669e5
Revises: 2d73f3c3f648
Create Date: 2024-11-29 19:54:58.080350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05a386d669e5'
down_revision = '2d73f3c3f648'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('puzzle_table',
    sa.Column('puzzleId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('puzzleLetters', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('puzzleId'),
    sa.UniqueConstraint('puzzleId')
    )
    op.create_table('user_table',
    sa.Column('userId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('userId'),
    sa.UniqueConstraint('userId')
    )
    op.create_table('attempts',
    sa.Column('puzzleId', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['puzzleId'], ['puzzle_table.puzzleId'], ),
    sa.ForeignKeyConstraint(['userId'], ['user_table.userId'], ),
    sa.PrimaryKeyConstraint('puzzleId', 'userId')
    )
    op.drop_table('puzzle')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('puzzle',
    sa.Column('puzzleId', sa.INTEGER(), nullable=False),
    sa.Column('puzzleLetters', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('puzzleId'),
    sa.UniqueConstraint('puzzleId')
    )
    op.drop_table('attempts')
    op.drop_table('user_table')
    op.drop_table('puzzle_table')
    # ### end Alembic commands ###
