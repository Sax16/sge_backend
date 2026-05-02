"""Update school management and ugel to enums

Revision ID: 0436dd1be87a
Revises: 92af4a3cd45a
Create Date: 2026-05-01 14:52:00.435707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0436dd1be87a'
down_revision: Union[str, Sequence[str], None] = '92af4a3cd45a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # --- management: stale enum type has PRIVADO/PUBLICO, needs PRIVADA/PUBLICA ---
    # 1. Convert column back to VARCHAR (so we can drop the old enum)
    op.execute("ALTER TABLE school ALTER COLUMN management TYPE VARCHAR(50) USING management::text")
    # 2. Update existing data to match new enum labels
    op.execute("UPDATE school SET management = 'PRIVADA' WHERE management = 'PRIVADO'")
    op.execute("UPDATE school SET management = 'PUBLICA' WHERE management = 'PUBLICO'")
    # 3. Drop old enum type and create correct one
    sa.Enum(name='managementtype').drop(op.get_bind(), checkfirst=True)
    managementtype = sa.Enum('PRIVADA', 'PUBLICA', name='managementtype')
    managementtype.create(op.get_bind(), checkfirst=True)
    # 4. Convert column to new enum type
    op.execute("ALTER TABLE school ALTER COLUMN management TYPE managementtype USING management::managementtype")

    # --- ugel: labels already correct (SATIPO, RIO_NEGRO, etc.) ---
    op.execute("ALTER TABLE school ALTER COLUMN ugel TYPE ugel USING ugel::ugel")


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('school', 'ugel',
               existing_type=sa.Enum('SATIPO', 'RIO_NEGRO', 'MAZAMARI', 'PANGOA', 'PICHANAKI', 'RIO_TAMBO', 'LA_MERCED', 'CONCEPCION', 'JAUJA', 'HUANCAYO', 'OTRO', name='ugel'),
               type_=sa.VARCHAR(length=50),
               existing_comment='Local Education Management Unit (UGEL)',
               existing_nullable=True)
    op.alter_column('school', 'management',
               existing_type=sa.Enum('PRIVADA', 'PUBLICA', name='managementtype'),
               type_=sa.VARCHAR(length=50),
               existing_comment='Name of the management or administrative unit',
               existing_nullable=False)
    # Drop enum types after reverting columns
    sa.Enum(name='ugel').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='managementtype').drop(op.get_bind(), checkfirst=True)
