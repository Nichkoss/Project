
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:databasesql2022@localhost:5432/airline"

db = SQLAlchemy(app)



class Booking(db.Model):
    __tablename__ = 'booking'
    idbooking = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    personid = db.Column(db.Integer, db.ForeignKey('person.idperson'))
    def __repr__(self):
        return "<Booking by user id: '{}', price: '{} >" \
            .format( self.userid, self.total_price)
class Flight(db.Model):
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
class AdditionalPassenger(db.Model):
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

class Sit(db.Model):
    __tablename__ = 'seat'
    idseat = db.Column(db.Integer, primary_key=True)
    seattnumber = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, nullable=False )
    price = db.Column(db.Float, nullable=False )
    flightid = db.Column(db.Integer, db.ForeignKey('flight.idflight'))
    def __repr__(self):
        return "<Sit number : '{}', availability : '{}', price: '{}'>" \
            .format(self.seatnumber, self.available, self.price)

class Ticket(db.Model):
    __tablename__ = 'ticket'
    idticket = db.Column(db.Integer, primary_key=True)
    extra_lug = db.Column(db.Integer, nullable=True)
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())#timestamp??
    seatid = db.Column(db.Integer, db.ForeignKey('seat.idseat'))
    bookingid = db.Column(db.Integer, db.ForeignKey('booking.idbooking'))
    passengerid = db.Column(db.Integer, db.ForeignKey('additional_passenger.idpassenger'))

class Person(db.Model):
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




#@app.route('/')
#def home():
 #   return "boom"


#@app.route('/api/v1/hello-world-13')
#def about():
#    return "Hello World 13"


#if __name__ == '__main__':
#    app.run(debug=True)


#mysql --user=root --password=mysql2022 airline < create-table.sql