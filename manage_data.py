# from flask_sqlalchemy.session import Session
from lab4.models import Session, app, Passenger, Booking, Flight, Seat, Ticket, Person

session = Session()
with app.app_context():
    user = Person(email="test3@gmail.com", password="qwqwqwqwqw", creation_time="2022-07-24 14:04:06.016547", role='client', firstname="Mary", lastname="Topmpson", birthdate="2008-11-22", pass_ser="GB", pass_num="808056", expirydate="2023-11-12")
    user2 = Person(email="test4@gmail.com", password="12345", creation_time="2022-10-20 14:04:06.016547", role='manager',
                firstname="Lucy", lastname="Lockwood", birthdate="2001-09-08", pass_ser="GB", pass_num="789921",
                expirydate="2024-08-14")
    additional_passenger = Passenger(firstname="Laura", lastname="Debberson", birthdate="1998-07-02", email="test13@gmail.com", pass_ser="KB", pass_num="997645", expirydate="2022-12-28")
    additional_passenger2 = Passenger(firstname="Dora", lastname="Dickens", birthdate="1998-01-22",
                                               email="test14@gmail.com", pass_ser="GB", pass_num="997335",
                                               expirydate="2022-12-28")
    flight = Flight(city_from="Berlin", city_to="Los Angeles", airport_from="Berlin Brandenburg Airport", airport_to="Berlin Brandenburg Airport", max_sits=300, flight_date="2023-01-03")
    flight2 = Flight(city_from="Paris", city_to="Frankfurt", airport_from="'Charles de Gaulle Airport'",
                    airport_to="'Frankfurt Airport'", max_sits=400, flight_date="2022-12-05")

    session.add(user)
    session.add(user2)
    session.add(additional_passenger)
    session.add(additional_passenger2)
    session.add(flight)
    session.add(flight2)
    session.commit()

    booking = Booking(total_price=161, personid=user.idperson)
    booking2 = Booking(total_price=161, personid=user2.idperson)
    seat1 = Seat(seatnumber=23, available=1, price=80.50, flightid=flight.idflight)
    seat2 = Seat(seatnumber=24, available=1, price=80.50, flightid=flight.idflight)
    seat3 = Seat(seatnumber=12, available=1, price=80.50, flightid=flight2.idflight)
    seat4 = Seat(seatnumber=13, available=1, price=80.50, flightid=flight2.idflight)
    session.add(booking)
    session.add(booking2)
    session.add(seat1)
    session.add(seat2)
    session.add(seat3)
    session.add(seat4)
    session.commit()

    ticket1 = Ticket(creation_date="2022-10-24 08:04:06.016547", seatid=seat1.idseat, extra_lug=0, bookingid=booking.idbooking, passengerid=additional_passenger.idpassenger)
    ticket2 = Ticket(creation_date="2022-10-24 08:09:09.016547", seatid=seat2.idseat,extra_lug=0, bookingid=booking.idbooking, passengerid=additional_passenger.idpassenger)
    ticket3 = Ticket(creation_date="2022-11-01 12:03:06.016547", seatid=seat3.idseat, extra_lug=1, bookingid=booking2.idbooking,passengerid=additional_passenger2.idpassenger)
    ticket4 = Ticket(creation_date="2022-10-01 12:15:09.016547", seatid=seat4.idseat,extra_lug=2, bookingid=booking2.idbooking,passengerid=additional_passenger2.idpassenger)
    session.add(ticket1)
    session.add(ticket2)
    session.add(ticket3)
    session.add(ticket4)
    session.commit()


