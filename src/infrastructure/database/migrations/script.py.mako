"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
    sa.Enum(name="language").drop(op.get_bind())
    sa.Enum(name="member").drop(op.get_bind())
    sa.Enum(name="productmode").drop(op.get_bind())
    sa.Enum(name="menuproductstatus").drop(op.get_bind())
    sa.Enum(name="productstatus").drop(op.get_bind())
    sa.Enum(name="paymenttype").drop(op.get_bind())
    sa.Enum(name="orderstatus").drop(op.get_bind())
    sa.Enum(name="ordertype").drop(op.get_bind())
    sa.Enum(name="basketstatus").drop(op.get_bind())
    sa.Enum(name="telegramstatus").drop(op.get_bind())