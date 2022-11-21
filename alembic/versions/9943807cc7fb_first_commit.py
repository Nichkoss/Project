"""First commit

Revision ID: 9943807cc7fb
Revises: 
Create Date: 2022-10-24 21:28:08.828962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9943807cc7fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('passenger',
    sa.Column('idpassenger', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=50), nullable=False),
    sa.Column('lastname', sa.String(length=50), nullable=False),
    sa.Column('birthdate', sa.Date(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('pass_ser', sa.String(length=50), nullable=False),
    sa.Column('pass_num', sa.String(length=50), nullable=False),
    sa.Column('expirydate', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('idpassenger'),
    sa.UniqueConstraint('email')
    )
    op.create_table('flight',
    sa.Column('idflight', sa.Integer(), nullable=False),
    sa.Column('city_from', sa.String(length=50), nullable=False),
    sa.Column('city_to', sa.String(length=50), nullable=False),
    sa.Column('airport_from', sa.String(length=50), nullable=False),
    sa.Column('airport_to', sa.String(length=50), nullable=False),
    sa.Column('max_sits', sa.Integer(), nullable=False),
    sa.Column('flight_date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('idflight')
    )
    op.create_table('person',
    sa.Column('idperson', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('creation_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('role', sa.String(length=50), nullable=True),
    sa.Column('firstname', sa.String(length=50), nullable=False),
    sa.Column('lastname', sa.String(length=50), nullable=False),
    sa.Column('birthdate', sa.Date(), nullable=False),
    sa.Column('pass_ser', sa.String(length=50), nullable=False),
    sa.Column('pass_num', sa.String(length=50), nullable=False),
    sa.Column('expirydate', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('idperson'),
    sa.UniqueConstraint('email')
    )
    op.create_table('booking',
    sa.Column('idbooking', sa.Integer(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('personid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['personid'], ['person.idperson'], ),
    sa.PrimaryKeyConstraint('idbooking')
    )
    op.create_table('seat',
    sa.Column('idseat', sa.Integer(), nullable=False),
    sa.Column('seatnumber', sa.Integer(), nullable=False),
    sa.Column('available', sa.Boolean(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('flightid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['flightid'], ['flight.idflight'], ),
    sa.PrimaryKeyConstraint('idseat')
    )
    op.create_table('ticket',
    sa.Column('idticket', sa.Integer(), nullable=False),
    sa.Column('extra_lug', sa.Integer(), nullable=True),
    sa.Column('creation_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('seatid', sa.Integer(), nullable=True),
    sa.Column('bookingid', sa.Integer(), nullable=True),
    sa.Column('passengerid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bookingid'], ['booking.idbooking'], ),
    sa.ForeignKeyConstraint(['passengerid'], ['passenger.idpassenger'], ),
    sa.ForeignKeyConstraint(['seatid'], ['seat.idseat'], ),
    sa.PrimaryKeyConstraint('idticket')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ticket')
    op.drop_table('seat')
    op.drop_table('booking')
    op.drop_table('person')
    op.drop_table('flight')
    op.drop_table('passenger')
    # ### end Alembic commands ###
