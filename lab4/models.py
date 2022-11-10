
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:databasesql2022@localhost:5432/airline"

db = SQLAlchemy(app)
#Session = scoped_session(SessionFactory)
#session=db.session
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
            class_id_attr = f"{cls.__name__}_id".lower()
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
            class_id_attr = f"{cls.__name__}_id".lower()
            session.query(cls).filter(getattr(cls, class_id_attr) == id).delete()
            session.commit()
            return 200

    @classmethod
    def update_one(cls, id, updates):
        with Session() as session:
            if cls.get_by_id(id) == 404:
                return 404
            class_id_attr = f"{cls.__name__}_id".lower()
            session.query(cls).filter(getattr(cls, class_id_attr) == id).update(updates)
            session.commit()
            return 200

    # @classmethod
    # def get_with_filter(cls, parameters):
    #     with Session() as session:
    #         q = session.query(cls)
    #         for attr, value in parameters.items():
    #             q = q.filter(getattr(cls, attr).ilike(f"%%{value}%%"))
    #
    #         return q.all()
class Booking(CustomBase, db.Model):
    __tablename__ = 'booking'
    idbooking = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    personid = db.Column(db.Integer, db.ForeignKey('person.idperson'))
    def __repr__(self):
        return "<Booking by user id: '{}', price: '{} >" \
            .format( self.userid, self.total_price)
    def __init__(self, total_price, personid):
        self.total_price=total_price
        self.personid=personid
class BookingSchema(Schema):
    idbooking= fields.Integer()
    total_price=fields.float(required=True)

    person=fields.Nested(PersonSchema, dump_only=True)
    personid=fields.Integer(load_only=True)

class Flight(CustomBase, db.Model):
    __tablename__ = 'flight'
    idflight = db.Column(db.Integer, primary_key=True)
    city_from = db.Column(db.String(50), nullable=False)
    city_to = db.Column(db.String(50), nullable=False)
    airport_from = db.Column(db.String(50), nullable=False)
    airport_to = db.Column(db.String(50), nullable=False)
    max_sits = db.Column(db.Integer, nullable=False)
    flight_date = db.Column(db.Date, nullable=False)
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
class FlightSchema(Schema):
    idflight = fields.Integer()

    city_from = fields.String(50, required=True)
    city_to = fields.String(50, required=True)
    airport_from = fields.String(50, required=True)
    airport_to = fields.String(50, required=True)
    max_sits = fields.Integer(required=True)
    flight_date = fields.Date(required=True)

class AdditionalPassenger(CustomBase, db.Model):
    __tablename__ = 'additional_passenger'

    idpassenger = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=True)
    pass_ser = db.Column(db.String(50), nullable=False)
    pass_num = db.Column(db.String(50), nullable=False)
    expirydate = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return "<Additional passenger : '{}' '{}', email: '{}'>" \
            .format(self.first_name, self.last_name, self.email)
    def __init__(self, firstname, lastname, birthdate, email, pass_ser, pass_num, expirydate):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.email = email
        self.pass_ser = pass_ser
        self.pass_num = ass_num
        self.expirydate = expirydate
class PassengerSchema(Schema):
    idpassenger = fields.Integer()

    firstname = fields.String(50, required=True)
    lastname = fields.String(50, required=True)
    birthdate = fields.Date(required=True)
    email = fields.Email(50, required=True)
    pass_ser = fields.String(50, required=True)
    pass_num = fields.String(50, required=True)
    expirydate = fields.Date(required=True)

class Seat(CustomBase, db.Model):
    __tablename__ = 'seat'
    idseat = db.Column(db.Integer, primary_key=True)
    seatnumber = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, nullable=False )
    price = db.Column(db.Float, nullable=False )
    flightid = db.Column(db.Integer, db.ForeignKey('flight.idflight'))
    def __repr__(self):
        return "<Sit number : '{}', availability : '{}', price: '{}'>" \
            .format(self.seatnumber, self.available, self.price)

    def __init__(self, seatnumber, available, price, flightid):
        self.seatnumber = seatnumber
        self.available = available
        self.price = price
        self.flightid = flightid
class SeatSchema(Schema):
    idseat = fields.Integer()

    seatnumber = fields.Integer(required=True)
    available = fields.Boolean(required=True)
    price = fields.Float(required=True)

    flight = fields.Nested(FlightSchema, dump_only=True)
    flightid = fields.Integer(load_only=True)

class Ticket(CustomBase, db.Model):
    __tablename__ = 'ticket'

    idticket = db.Column(db.Integer, primary_key=True)
    extra_lug = db.Column(db.Integer, nullable=True)
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())#timestamp??
    seatid = db.Column(db.Integer, db.ForeignKey('seat.idseat'))
    bookingid = db.Column(db.Integer, db.ForeignKey('booking.idbooking'))
    passengerid = db.Column(db.Integer, db.ForeignKey('additional_passenger.idpassenger'))

    def __repr__(self):
        return "<Extra luggage: '{}', Time of creation: '{}'>" \
            .format(self.extra_lug, self.creation_date)
    def __init__(self, extra_lug, creation_date, seatid, bookingid, passengerid):
        self.extra_lug = extra_lug
        self.creation_date = creation_date
        self.seatid = seatid
        self.bookingid = bookingid
        self.passengerid = passengerid
class TicketSchema(Schema):
    idticket=fields.Integer()

    extra_lug=fields.Integer(required=True)
    creation_date=fields.DataTime(required=True)

    seatid=fields.Integer(load_only=True)
    seat=fields.Nested(SeatSchema, dump_only=True)

    bookingid=fields.Integer(load_only=True)
    booking=fields.Nested(BookingSchema, dump_only=True)

    passengerid=fields.Integer(load_only=True)
    passenger=fields.Nested(PassengerSchema, dump_only=True)

class Person(CustomBase, db.Model):
    __tablename__ = 'person'

    idperson = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50))
    creation_time = db.Column(db.DateTime(timezone=True), default=func.now())#timestamp??
    mgr = db.Column(db.Boolean, nullable=True, default='NULL')
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    pass_ser = db.Column(db.String(50), nullable=False)
    pass_num = db.Column(db.String(50), nullable=False)
    expirydate = db.Column(db.Date, nullable=False)

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
class PersonSchema(Schema):
    idperson=fields.Integer()

    email = fields.Email(50,required=True)
    password = fields.String(50,required=True)
    creation_time = fields.DataTime(required=True)
    mgr = fields.Boolean(required=True)
    firstname = fields.String(50,required=True)
    lastname = fields.String(50,required=True)
    birthdate = fields.Date(required=True)
    pass_ser = fields.String(50,required=True)
    pass_num = fields.String(50,required=True)
    expirydate = fields.Date(required=True)


#@app.route('/')
#def home():
 #   return "boom"


#@app.route('/api/v1/hello-world-13')
#def about():
#    return "Hello World 13"


#if __name__ == '__main__':
#    app.run(debug=True)


#mysql --user=root --password=mysql2022 airline < create-table.sql