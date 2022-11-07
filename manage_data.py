# from flask_sqlalchemy.session import Session
from lab4.models import app, db, AdditionalPassenger, Booking, Flight, Sit, Ticket, User

# session = Session()
with app.app_context():
    user = Person(email="test1@gmail.com", password="qwqwqwqwqw", creation_time="2022-07-24 14:04:06.016547", mgr=0, firstname="Mary", lastname="Topmpson", birthdate="2008-11-22", pass_ser="GB", pass_num="808056", expirydate="2023-11-12")
    user2 = Person(email="test2@gmail.com", password="12345", creation_time="2022-10-20 14:04:06.016547", mgr=1,
                firstname="Lucy", lastname="Lockwood", birthdate="2001-09-08", pass_ser="GB", pass_num="789921",
                expirydate="2024-08-14")
    additional_passenger = AdditionalPassenger(firstname="Laura", lastname="Debberson", birthdate="1998-07-02", email="test3@gmail.com", pass_ser="KB", pass_num="997645", expirydate="2022-12-28")
    additional_passenger2 = AdditionalPassenger(firstname="Dora", lastname="Dickens", birthdate="1998-01-22",
                                               email="test4@gmail.com", pass_ser="GB", pass_num="997335",
                                               expirydate="2022-12-28")
    flight = Flight(city_from="Berlin", city_to="Los Angeles", airport_from="Berlin Brandenburg Airport", airport_to="Berlin Brandenburg Airport", max_sits=300, flight_date="2023-01-03")
    flight2 = Flight(city_from="Paris", city_to="Frankfurt", airport_from="'Charles de Gaulle Airport'",
                    airport_to="'Frankfurt Airport'", max_sits=400, flight_date="2022-12-05")

    db.session.add(user)
    db.session.add(user2)
    db.session.add(additional_passenger)
    db.session.add(additional_passenger2)
    db.session.add(flight)
    db.session.add(flight2)
    db.session.commit()

    booking = Booking(total_price=161, personid=user.idperson)
    booking2 = Booking(total_price=161, personid=user2.idperson)
    seat1 = Seat(seatnumber=23, available=1, price=80.50, flightid=flight.idflight)
    seat2 = Seat(seatnumber=24, available=1, price=80.50, flightid=flight.idflight)
    seat3 = Seat(seatnumber=12, available=1, price=80.50, flightid=flight2.idflight)
    seat4 = Seat(seatnumber=13, available=1, price=80.50, flightid=flight2.idflight)
    db.session.add(booking)
    db.session.add(booking2)
    db.session.add(seat1)
    db.session.add(seat2)
    db.session.add(seat3)
    db.session.add(seat4)
    db.session.commit()

    ticket1 = Ticket(creation_date="2022-10-24 08:04:06.016547", seatid=seat1.idseat, bookingid=booking.idbooking, passengerid=additional_passenger.idpassenger)
    ticket2 = Ticket(creation_date="2022-10-24 08:09:09.016547", seatid=seat2.idseat, bookingid=booking.idbooking)
    ticket3 = Ticket(creation_date="2022-11-01 12:03:06.016547", seatid=seat3.idseat, extra_lug=1, bookingid=booking2.idbooking,
                     passengerid=additional_passenger2.idpassenger)
    ticket4 = Ticket(creation_date="2022-10-01 12:15:09.016547", seatid=seat4.idseat, bookingid=booking2.idbooking)
    db.session.add(ticket1)
    db.session.add(ticket2)
    db.session.add(ticket3)
    db.session.add(ticket4)
    db.session.commit()


