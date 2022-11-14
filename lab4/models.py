
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, sessionmaker, scoped_session, declarative_base, backref
from marshmallow import Schema, fields, validate, post_load, pre_load
import datetime


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:databasesql2022@localhost:5432/airline"

#db = SQLAlchemy(app)

DB_URI="postgresql://postgres:databasesql2022@localhost:5432/airline"
engine = create_engine(DB_URI)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

Base = declarative_base()

class CustomBase():
    @classmethod
    def get_all(cls):
        with Session() as session:
            return session.query(cls).all()

    @classmethod
    def post_one(cls, item):
        with Session() as session:
            session.add(item)
            session.commit()

            return 200

    @classmethod
    def get_by_id(cls, id):
        with Session() as session:
            class_id_attr = f"id{cls.__name__}".lower()
            class_object = session.query(cls).filter(getattr(cls, class_id_attr) == id).first()
            if class_object is None:
                return 404
            return class_object

    @classmethod
    def delete_by_id(cls, id):
        with Session() as session:
            class_object = cls.get_by_id(id)

            if class_object == 404:
                return 404
            class_id_attr = f"id{cls.__name__}".lower()
            session.query(cls).filter(getattr(cls, class_id_attr) == id).delete()
            session.commit()
            return 200

    @classmethod
    def update_one(cls, id, updates):
        with Session() as session:
            if cls.get_by_id(id) == 404:
                return 404
            class_id_attr = f"id{cls.__name__}".lower()
            session.query(cls).filter(getattr(cls, class_id_attr) == id).update(updates)
            session.commit()
            return 200

    @classmethod
    def get_with_filter(cls, parameters):
        with Session() as session:
            q = session.query(cls)
            for attr, value in parameters.items():
                q = q.filter(getattr(cls, attr).ilike(f"%%{value}%%"))

            return q.all()

class Person(CustomBase, Base):
    __tablename__ = 'person'

    idperson = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String())
    creation_time = Column(DateTime(timezone=True), default=func.now())#timestamp??
    mgr = Column(Boolean, nullable=True, default='NULL')
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    birthdate = Column(Date, nullable=False)
    pass_ser = Column(String(50), nullable=False)
    pass_num = Column(String(50), nullable=False)
    expirydate = Column(Date, nullable=False)

    def __repr__(self):
        return "<User: '{}' '{}', email: '{}'>" \
            .format(self.first_name, self.last_name, self.email)
    def __init_(self, email, password, creation_time, mgr, firstname, lastname, birthdate, pass_ser, pass_num, expirydate):
        self.email = email
        self.password = password
        self.creation_time = creation_time
        self.mgr = mgr
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.pass_ser = pass_ser
        self.pass_num = pass_num
        self.expirydate = expirydate

    # GET
    @classmethod
    def get_preview(cls, id):
        with Session() as session:
            user_object = session.query(cls).filter(getattr(cls, "idperson") == id).\
                with_entities(Person.firstname, Person.lastname, Person.email, Person.idperson).first()
            if user_object is None:
                return 404

            return user_object
class PersonSchema(Schema):
    idperson=fields.Integer()

    email = fields.Email(required=True)
    password = fields.String(required=True)
    creation_time = fields.DateTime(required=True)
    mgr = fields.Boolean(required=True)
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    birthdate = fields.Date(required=True)
    pass_ser = fields.String(required=True)
    pass_num = fields.String(required=True)
    expirydate = fields.Date(required=True)

class Passenger(CustomBase, Base):
    __tablename__ = 'passenger'

    idpassenger = Column(Integer, primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    birthdate = Column(Date, nullable=False)
    email = Column(String(50), unique=True, nullable=True)
    pass_ser = Column(String(50), nullable=False)
    pass_num = Column(String(50), nullable=False)
    expirydate = Column(Date, nullable=False)

    def __repr__(self):
        return "<Additional passenger : '{}' '{}', email: '{}'>" \
            .format(self.first_name, self.last_name, self.email)
    def __init__(self, firstname, lastname, birthdate, email, pass_ser, pass_num, expirydate):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.email = email
        self.pass_ser = pass_ser
        self.pass_num = pass_num
        self.expirydate = expirydate

    # GET
    @classmethod
    def get_preview(cls, id):
        with Session() as session:
            passenger_object = session.query(cls).filter(getattr(cls, "idpassenger") == id).\
                with_entities(Passenger.firstname, Passenger.lastname, Passenger.email, Passenger.idpassenger).first()
            if passenger_object is None:
                return 404

            return passenger_object
class PassengerSchema(Schema):
    idpassenger = fields.Integer()

    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    birthdate = fields.Date(required=True)
    email = fields.Email(required=True)
    pass_ser = fields.String(required=True)
    pass_num = fields.String(required=True)
    expirydate = fields.Date(required=True)

class Booking(CustomBase, Base):
    __tablename__ = 'booking'
    idbooking = Column(Integer, primary_key=True)
    total_price = Column(Float, nullable=False)
    personid = Column(Integer, ForeignKey('person.idperson'))
    def __repr__(self):
        return "<Booking by user id: '{}', price: '{} >" \
            .format( self.userid, self.total_price)
    def __init__(self, total_price, personid):
        self.total_price=total_price
        self.personid=personid
    @classmethod
    def get_preview(cls, id):
        with Session() as session:
            booking_object = session.query(cls).filter(getattr(cls, "idbooking") == id).\
                with_entities(Booking.total_price, Booking.idbooking).first()
            if booking_object is None:
                return 404

            return booking_object
class BookingSchema(Schema):
    idbooking= fields.Integer()
    total_price=fields.Float(required=True)

    person=fields.Nested(PersonSchema, dump_only=True)
    personid=fields.Integer(load_only=True)

class Flight(CustomBase, Base):
    __tablename__ = 'flight'
    idflight = Column(Integer, primary_key=True)
    city_from = Column(String(50), nullable=False)
    city_to = Column(String(50), nullable=False)
    airport_from = Column(String(50), nullable=False)
    airport_to = Column(String(50), nullable=False)
    max_sits = Column(Integer, nullable=False)
    flight_date = Column(Date, nullable=False)
    def __repr__(self):
        return "<Flight  '{}' - '{}' on '{}'>" \
            .format(self.flight_from, self.flight_to, self.flight_date)

    def __init__(self, city_from, city_to, airport_from, airport_to, max_sits, flight_date):
        self.city_from=city_from
        self.city_to=city_to
        self.airport_from=airport_from
        self.airport_to=airport_to
        self.max_sits=max_sits
        self.flight_date=flight_date

    # GET
    @classmethod
    def get_preview(cls, id):
        with Session() as session:
            flight_object = session.query(cls).filter(getattr(cls, "idflight") == id).\
                with_entities(Flight.city_from, Flight.city_to, Flight.max_sits, Flight.flight_date, Flight.idflight).first()
            if flight_object is None:
                return 404

            return flight_object
class FlightSchema(Schema):
    idflight = fields.Integer()

    city_from = fields.String(required=True)
    city_to = fields.String(required=True)
    airport_from = fields.String(required=True)
    airport_to = fields.String(required=True)
    max_sits = fields.Integer(required=True)
    flight_date = fields.Date(required=True)

class Seat(CustomBase, Base):
    __tablename__ = 'seat'
    idseat = Column(Integer, primary_key=True)
    seatnumber = Column(Integer, nullable=False)
    available = Column(Boolean, nullable=False )
    price = Column(Float, nullable=False )
    flightid = Column(Integer, ForeignKey('flight.idflight'))
    def __repr__(self):
        return "<Sit number : '{}', availability : '{}', price: '{}'>" \
            .format(self.seatnumber, self.available, self.price)

    def __init__(self, seatnumber, available, price, flightid):
        self.seatnumber = seatnumber
        self.available = available
        self.price = price
        self.flightid = flightid

    # GET
    @classmethod
    def get_preview(cls, id):
        with Session() as session:
            seat_object = session.query(cls).filter(getattr(cls, "idseat") == id).\
                with_entities(Seat.seatnumber, Seat.available, Seat.price, Seat.idseat).first()
            if seat_object is None:
                return 404

            return seat_object
class SeatSchema(Schema):
    idseat = fields.Integer()

    seatnumber = fields.Integer(required=True)
    available = fields.Boolean(required=True)
    price = fields.Float(required=True)

    flight = fields.Nested(FlightSchema, dump_only=True)
    flightid = fields.Integer(load_only=True)

class Ticket(CustomBase, Base):
    __tablename__ = 'ticket'

    idticket = Column(Integer, primary_key=True)
    extra_lug = Column(Integer, nullable=True)
    creation_date = Column(DateTime(timezone=True),default=datetime.datetime.utcnow)
    seatid = Column(Integer, ForeignKey('seat.idseat'))
    bookingid = Column(Integer, ForeignKey('booking.idbooking'))
    passengerid = Column(Integer, ForeignKey('passenger.idpassenger'))

    def __repr__(self):
        return "<Extra luggage: '{}', Time of creation: '{}'>" \
            .format(self.extra_lug, self.creation_date)
    def __init__(self, extra_lug, creation_date, seatid, bookingid, passengerid):
        self.extra_lug = extra_lug
        self.creation_date = creation_date
        self.seatid = seatid
        self.bookingid = bookingid
        self.passengerid = passengerid
    # GET
    @classmethod
    def get_preview(cls, id):
        with Session() as session:
            ticket_object = session.query(cls).filter(getattr(cls, "idticket") == id).\
                with_entities(Ticket.extra_lug, Ticket.creation_date, Ticket.idticket).first()
            if ticket_object is None:
                return 404

            return ticket_object
class TicketSchema(Schema):
    idticket=fields.Integer()

    extra_lug=fields.Integer(required=True)
    creation_date=fields.DateTime(required=True)

    seatid=fields.Integer(load_only=True)
    seat=fields.Nested(SeatSchema, dump_only=True)

    bookingid=fields.Integer(load_only=True)
    booking=fields.Nested(BookingSchema, dump_only=True)

    passengerid=fields.Integer(load_only=True)
    passenger=fields.Nested(PassengerSchema, dump_only=True)

if __name__ == "__main__":
    pass
#@app.route('/')
#def home():
#    return "boom"


#@app.route('/api/v1/hello-world-13')
#def about():
#    return "Hello World 13"


#if __name__ == '__main__':
#    app.run(debug=True)


#mysql --user=root --password=mysql2022 airline < create-table.sql