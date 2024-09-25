"""Database creation

Revision ID: d3c42ef182eb
Revises: 
Create Date: 2024-09-25 13:29:14.698563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3c42ef182eb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_user_notes', 'notes', type_='unique')
    op.create_unique_constraint('unique_user_note', 'notes', ['user_id', 'note_title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_user_note', 'notes', type_='unique')
    op.create_unique_constraint('unique_user_notes', 'notes', ['user_id', 'note_title'])
    # ### end Alembic commands ###
