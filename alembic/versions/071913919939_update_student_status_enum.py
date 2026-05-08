"""update_student_status_enum

Revision ID: 071913919939
Revises: fedc469062e1
Create Date: 2026-05-07 03:56:23.914684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '071913919939'
down_revision: Union[str, Sequence[str], None] = 'fedc469062e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE studentstatus RENAME VALUE 'ACTIVO' TO 'MATRICULADO'")
    op.execute("ALTER TYPE studentstatus ADD VALUE 'PENDIENTE'")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TYPE studentstatus RENAME VALUE 'MATRICULADO' TO 'ACTIVO'")
    # Note: PostgreSQL does not support dropping ENUM values easily.
    # PENDIENTE will remain in the database upon downgrade.
