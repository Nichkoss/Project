import json

from werkzeug.security import generate_password_hash
# from lab4.blueprint import *
from lab4.models import *
from flask_testing import TestCase
from flask import url_for
# from lab4.blueprint import *
from lab4.app import app
import base64


class TestApi(TestCase):

    def create_tables(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def setUp(self):
        super().setUp()


    def get_basic_client_headers(self):
        return {
            "Authorization": "Basic " + base64.b64encode(b"check11u@gmail.com:12345").decode("utf8")
        }
    def get_basic_manager_headers(self):
        return {
            "Authorization": "Basic " + base64.b64encode(b"m1@gmail.com:12345").decode("utf8")
        }

    def close_session(self):
        Session.close()
    def tearDown(self):
        self.close_session()
    def create_app(self):
        return app


class TestAuthentication(TestApi):
    def setUp(self):
        self.create_tables()
        self.email = 'check2u@gmail.com'
        self.password = "12345"
        self.password_hash = generate_password_hash('12345')
        self.booking_data_ok = {

                "total_price" : 200,
                 "personid" : 1
            }
        self.client_data_ok = {
            "email": "check11u@gmail.com",
            "password": "12345",
            "creation_time": "2022-11-11T23:23",
            "role": "client",
            "firstname": "u1fname",
            "lastname": "u1lname",
            "birthdate": "2022-01-01",
            "pass_ser": "KA",
            "pass_num": "121212",
            "expirydate": "2022-02-02"
        }
        self.client2_data_ok = {
            "email": "check22u@gmail.com",
            "password": "12345",
            "creation_time": "2022-11-11T23:23",
            "role": "client",
            "firstname": "u2fname",
            "lastname": "u1lname",
            "birthdate": "2022-01-01",
            "pass_ser": "KA",
            "pass_num": "121212",
            "expirydate": "2022-02-02"
        }
        self.passenger1_data_ok = {
                "email": "p1@gmail.com",
                "firstname": "fname",
                "lastname": "lname",
                "birthdate": "2022-01-01",
                "pass_ser": "KA",
                "pass_num": "121212",
                "expirydate": "2022-02-02"
            }
        self.passenger2_data_ok = {
                "email": "p2@gmail.com",
                "firstname": "fname",
                "lastname": "lname",
                "birthdate": "2022-01-01",
                "pass_ser": "KA",
                "pass_num": "121212",
                "expirydate": "2022-02-02"
            }
        self.client_data_fail_email = {
            "email": "check2u@gmail.com",
            "password": "12345",
            "creation_time": "2022-11-11T23:23",
            "role": "client",
            "firstname": "u1fname",
            "lastname": "u1lname",
            "birthdate": "2022-01-01",
            "pass_ser": "KA",
            "pass_num": "121212",
            "expirydate": "2022-02-02"
        }
        self.client_data_fail_password = {
            "email": "check22u@gmail.com",
            "password": "1234",
            "creation_time": "2022-11-11T23:23",
            "role": "client",
            "firstname": "u1fname",
            "lastname": "u1lname",
            "birthdate": "2022-01-01",
            "pass_ser": "KA",
            "pass_num": "121212",
            "expirydate": "2022-02-02"
        }
        self.manager_data = {
            "email": "m1@gmail.com",
            "password": "12345",
            "creation_time": "2022-11-11T23:23",
            "role": "manager",
            "firstname": "m1fname",
            "lastname": "m1lname",
            "birthdate": "2022-01-01",
            "pass_ser": "KA",
            "pass_num": "121212",
            "expirydate": "2022-02-02"
        }
        self.flight_data_ok = {
            "city_from" : "Berlin",
            "city_to" : "Paris",
            "airport_from" : "Berlin International Airport",
            "airport_to": "Paris International Airport",
            "max_sits" : 300,
            "flight_date" : "2023-02-02"

        }

        self.seat_data_ok = {
            "seatnumber" : 1,
            "available" : True,
            "price" : 450.6,
            "flightid" : 1
        }

        self.ticket_data_ok = {
            "extra_lug" : 1,
            "creation_date" : "2023-01-02T23:23",
            "seatid" : 1,
            "bookingid" : 1,
            "passengerid" : 1
        }



    def test_authenticate_success(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)
        Session.add(person)
        Session.commit()
        resp = self.client.post(url_for("api.login_user"), headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.json["email"], "check11u@gmail.com")


    def  test_authenticate_fail_email(self):
        personSh = PersonSchema().load(self.client_data_fail_email)
        person = Person(**personSh)
        Session.add(person)
        Session.commit()
        resp = self.client.post(url_for("api.login_user"), headers=self.get_basic_client_headers())
        self.assertEqual(401, resp.status_code)

    def  test_authenticate_fail_password(self):
        personSh = PersonSchema().load(self.client_data_fail_password)
        person = Person(**personSh)
        Session.add(person)
        Session.commit()
        resp = self.client.post(url_for("api.login_user"), headers=self.get_basic_client_headers())
        self.assertEqual(401, resp.status_code)

    def test_create_user(self):
        payload = json.dumps(
            self.client_data_ok
        )
        resp = self.client.post(url_for("api.create_user"), headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_logout(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)
        Session.add(person)
        Session.commit()
        resp = self.client.delete(url_for("api.logout"), headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_update_user(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)
        Session.add(person)
        Session.commit()
        payload = json.dumps(
            self.client_data_ok
        )
        headers = self.get_basic_client_headers() # header can be also with manager credentials
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("api.update_user", id=person.idperson),  headers=headers, data=payload )
        self.assertEqual(200, resp.status_code)

    def test_update_user_status(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)

        personSh = PersonSchema().load(self.manager_data)
        person2 = Person(**personSh)
        Session.add(person)
        Session.add(person2)
        Session.commit()
        payload = json.dumps(
            self.client_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("api.update_user_status", id=person.idperson), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_delete_user(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person1 = Person(**personSh)

        personSh = PersonSchema().load(self.manager_data)
        person2 = Person(**personSh)
        Session.add(person1)
        Session.add(person2)
        Session.commit()
        resp = self.client.delete(url_for("api.delete_user", id=person1.idperson), headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)
    def test_get_user(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)
        Session.add(person)
        Session.commit()
        resp = self.client.get(url_for("api.get_user", id=person.idperson),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_users(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person1 = Person(**personSh)

        personSh = PersonSchema().load(self.manager_data)
        person2 = Person(**personSh)
        Session.add(person1)
        Session.add(person2)
        Session.commit()
        resp = self.client.get(url_for("api.get_users"),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)
    def test_get_users2(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person1 = Person(**personSh)

        personSh = PersonSchema().load(self.client2_data_ok)
        person3 = Person(**personSh)

        personSh = PersonSchema().load(self.manager_data)
        person2 = Person(**personSh)
        Session.add(person1)
        Session.add(person2)
        Session.add(person3)
        Session.commit()
        resp = self.client.get(url_for("api.get_users", firstname="u1fname"),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)
        self.assertEqual(  [{'birthdate': '2022-01-01', 'creation_time': '2022-11-11T23:23:00+02:00', 'email': 'check11u@gmail.com',
      'expirydate': '2022-02-02', 'firstname': 'u1fname', 'idperson': 1, 'lastname': 'u1lname', 'pass_num': '121212',
      'pass_ser': 'KA', 'role': 'client'}], resp.json)


    def test_get_passengers(self):
        passengerSh = PassengerSchema().load(self.passenger1_data_ok)
        passenger1 = Passenger(**passengerSh)

        passengerSh = PassengerSchema().load(self.passenger2_data_ok)
        passenger2 = Passenger(**passengerSh)

        managerSh = PersonSchema().load(self.manager_data)
        manager = Person(**managerSh)
        Session.add(passenger1)
        Session.add(passenger2)
        Session.add(manager)
        Session.commit()
        resp = self.client.get(url_for("api.get_passengers"),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200,resp.status_code)

    def test_create_passenger(self):
        payload = json.dumps(
            self.passenger1_data_ok
        )
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)
        Session.add(person)
        Session.commit()
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("api.create_passenger"), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_update_passenger(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)

        passengerSh = PassengerSchema().load(self.passenger1_data_ok)
        passenger = Passenger(**passengerSh)

        Session.add(person)
        Session.add(passenger)
        Session.commit()
        payload = json.dumps(
            self.passenger1_data_ok
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("api.update_user", id=passenger.idpassenger), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_get_passenger(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)

        passengerSh = PassengerSchema().load(self.passenger1_data_ok)
        passenger = Passenger(**passengerSh)

        Session.add(person)
        Session.add(passenger)
        Session.commit()
        resp = self.client.get(url_for("api.get_passenger", id=passenger.idpassenger),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_bookings(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)
        bookingSh = BookingSchema().load(self.booking_data_ok)
        booking = Booking(**bookingSh)

        personSh = PersonSchema().load(self.manager_data)
        person2 = Person(**personSh)
        Session.add(person)
        Session.commit()
        Session.add(booking)
        Session.add(person2)
        Session.commit()
        resp = self.client.get(url_for("api.get_bookings"),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    def test_create_booking(self):
        payload = json.dumps(
            self.booking_data_ok
        )
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)
        Session.add(person)
        Session.commit()
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("api.create_booking"), headers=headers, data=payload)

    def test_update_booking(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)
        bookingSh = BookingSchema().load(self.booking_data_ok)
        booking = Booking(**bookingSh)

        Session.add(person)
        Session.commit()
        Session.add(booking)
        Session.commit()
        payload = json.dumps(
            self.booking_data_ok
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("api.update_booking", id=booking.idbooking), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_update_booking_price(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)
        bookingSh = BookingSchema().load(self.booking_data_ok)
        booking = Booking(**bookingSh)

        Session.add(person)
        Session.commit()
        Session.add(booking)
        Session.commit()
        payload = json.dumps(
            self.booking_data_ok
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("api.update_booking_price", id=booking.idbooking), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_delete_booking(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)
        bookingSh = BookingSchema().load(self.booking_data_ok)
        booking = Booking(**bookingSh)

        Session.add(person)
        Session.commit()
        Session.add(booking)
        Session.commit()
        resp = self.client.delete(url_for("api.delete_booking", id=booking.idbooking), headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_booking(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)
        bookingSh = BookingSchema().load(self.booking_data_ok)
        booking = Booking(**bookingSh)

        Session.add(person)
        Session.commit()
        Session.add(booking)
        Session.commit()
        resp = self.client.get(url_for("api.get_booking", id=booking.idbooking),
                               headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_flights(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)
        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)

        Session.add(person)
        Session.add(flight)
        Session.commit()
        resp = self.client.get(url_for("api.get_flights"),
                               headers=self.get_basic_client_headers()) # can also be manager
        self.assertEqual(200, resp.status_code)

    def test_create_flight(self):
        personSh = PersonSchema().load(self.manager_data)
        person = Person(**personSh)
        Session.add(person)
        Session.commit()
        payload = json.dumps(
            self.flight_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("api.create_flight"), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_update_flight(self):
        personSh = PersonSchema().load(self.manager_data)
        person = Person(**personSh)
        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)
        Session.add(person)
        Session.commit()
        Session.add(flight)
        Session.commit()
        payload = json.dumps(
            self.flight_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("api.update_flight", id=flight.idflight), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_delete_flight(self):
        personSh = PersonSchema().load(self.manager_data)
        person = Person(**personSh)
        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)

        Session.add(person)
        Session.commit()
        Session.add(flight)
        Session.commit()
        resp = self.client.delete(url_for("api.delete_flight", id=flight.idflight),
                                  headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_flight(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)
        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)

        Session.add(person)
        Session.commit()
        Session.add(flight)
        Session.commit()
        resp = self.client.get(url_for("api.get_flight", id=flight.idflight),
                               headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_seats_for_flight(self):
        personSh = PersonSchema().load(self.manager_data)
        person = Person(**personSh)
        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)
        seatSh = SeatSchema().load(self.seat_data_ok)
        seat = Seat(**seatSh)
        Session.add(person)
        Session.add(flight)
        Session.commit()
        Session.add(seat)
        Session.commit()
        resp = self.client.get(url_for("api.get_seats_for_flight", id=flight.idflight),
                               headers=self.get_basic_manager_headers())  # can also be manager
        self.assertEqual(200, resp.status_code)

    def test_get_seats(self):
        personSh = PersonSchema().load(self.manager_data)
        person = Person(**personSh)
        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)
        seatSh = SeatSchema().load(self.seat_data_ok)
        seat = Seat(**seatSh)
        Session.add(person)
        Session.add(flight)
        Session.commit()
        Session.add(seat)
        Session.commit()
        resp = self.client.get(url_for("api.get_seats"),
                               headers=self.get_basic_manager_headers())  # can also be manager
        self.assertEqual(200, resp.status_code)

    def test_create_seat(self):
        personSh = PersonSchema().load(self.manager_data)
        person = Person(**personSh)
        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)

        Session.add(person)
        Session.add(flight)
        Session.commit()

        payload = json.dumps(
            self.seat_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("api.create_seat"), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_update_seat(self):
        personSh = PersonSchema().load(self.manager_data)
        person = Person(**personSh)
        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)
        seatSh = SeatSchema().load(self.seat_data_ok)
        seat = Seat(**seatSh)
        Session.add(person)
        Session.add(flight)
        Session.commit()
        Session.add(seat)
        Session.commit()
        payload = json.dumps(
            self.seat_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("api.update_seat", id=seat.idseat), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_delete_seat(self):
        personSh = PersonSchema().load(self.manager_data)
        person = Person(**personSh)
        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)
        seatSh = SeatSchema().load(self.seat_data_ok)
        seat = Seat(**seatSh)
        Session.add(person)
        Session.add(flight)
        Session.commit()
        Session.add(seat)
        Session.commit()
        resp = self.client.delete(url_for("api.delete_seat", id=seat.idseat),
                                  headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_seat(self):
        personSh = PersonSchema().load(self.manager_data)
        person = Person(**personSh)
        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)
        seatSh = SeatSchema().load(self.seat_data_ok)
        seat = Seat(**seatSh)
        Session.add(person)
        Session.add(flight)
        Session.commit()
        Session.add(seat)
        Session.commit()
        resp = self.client.get(url_for("api.get_seat", id=seat.idseat),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_tickets(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)

        bookingSh = BookingSchema().load(self.booking_data_ok)
        booking = Booking(**bookingSh)

        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)

        seatSh = SeatSchema().load(self.seat_data_ok)
        seat = Seat(**seatSh)

        personSh = PersonSchema().load(self.manager_data)
        person2 = Person(**personSh)

        ticketSh = TicketSchema().load(self.ticket_data_ok)
        ticket = Ticket(**ticketSh)
        Session.add(person)
        Session.add(flight)
        Session.commit()
        Session.add(booking)
        Session.add(person2)
        Session.add(seat)
        Session.commit()
        Session.add(ticket)
        Session.commit()


        resp = self.client.get(url_for("api.get_tickets"),
                               headers=self.get_basic_manager_headers())  # can also be manager
        self.assertEqual(200, resp.status_code)

    def test_create_ticket(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)

        bookingSh = BookingSchema().load(self.booking_data_ok)
        booking = Booking(**bookingSh)

        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)

        seatSh = SeatSchema().load(self.seat_data_ok)
        seat = Seat(**seatSh)


        Session.add(person)
        Session.add(flight)
        Session.commit()
        Session.add(booking)
        Session.add(seat)
        Session.commit()

        payload = json.dumps(
            self.ticket_data_ok
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("api.create_ticket"), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_update_ticket(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)

        bookingSh = BookingSchema().load(self.booking_data_ok)
        booking = Booking(**bookingSh)

        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)

        seatSh = SeatSchema().load(self.seat_data_ok)
        seat = Seat(**seatSh)


        ticketSh = TicketSchema().load(self.ticket_data_ok)
        ticket = Ticket(**ticketSh)
        Session.add(person)
        Session.add(flight)
        Session.commit()
        Session.add(booking)
        Session.add(seat)
        Session.commit()
        Session.add(ticket)
        Session.commit()

        payload = json.dumps(
            self.ticket_data_ok
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("api.update_ticket", id=ticket.idticket), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_delete_ticket(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)

        bookingSh = BookingSchema().load(self.booking_data_ok)
        booking = Booking(**bookingSh)

        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)

        seatSh = SeatSchema().load(self.seat_data_ok)
        seat = Seat(**seatSh)


        ticketSh = TicketSchema().load(self.ticket_data_ok)
        ticket = Ticket(**ticketSh)
        Session.add(person)
        Session.add(flight)
        Session.commit()
        Session.add(booking)
        Session.add(seat)
        Session.commit()
        Session.add(ticket)
        Session.commit()
        resp = self.client.delete(url_for("api.delete_ticket", id=ticket.idticket),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_ticket(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)

        bookingSh = BookingSchema().load(self.booking_data_ok)
        booking = Booking(**bookingSh)

        flightSh = FlightSchema().load(self.flight_data_ok)
        flight = Flight(**flightSh)

        seatSh = SeatSchema().load(self.seat_data_ok)
        seat = Seat(**seatSh)


        ticketSh = TicketSchema().load(self.ticket_data_ok)
        ticket = Ticket(**ticketSh)
        Session.add(person)
        Session.add(flight)
        Session.commit()
        Session.add(booking)
        Session.add(seat)
        Session.commit()
        Session.add(ticket)
        Session.commit()
        resp = self.client.get(url_for("api.get_ticket", id=ticket.idticket),
                               headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)
