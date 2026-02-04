"""empty message

Revision ID: c7c2cdd4168a
Revises: 
Create Date: 2026-02-09 17:09:17.498162

"""
from alembic import op
import sqlalchemy as sa
from app.models.cars.schema_car import Car
from app.models.users.schema_user import User

# revision identifiers, used by Alembic.
revision = 'c7c2cdd4168a'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    columns_car = []
    columns_user = []

    for column in Car.__table__.columns:
        
        columns_car.append(
            sa.Column(
            column.name,
            column.type,
            primary_key = column.primary_key,
            nullable = column.nullable,
            )
        )

    for column in User.__table__.columns:
        columns_user.append(
                sa.Column(
                column.name,
                column.type,
                primary_key = column.primary_key,
                nullable = column.nullable,
            )
        )
    
    op.create_table(Car.__tablename__, *columns_car)
    op.create_table(User.__tablename__, *columns_user)

def downgrade():
    op.drop_table(Car.__tablename__)
    op.drop_table(User.__tablename__)
