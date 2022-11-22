from unittest import TestCase
from unittest.mock import patch, Mock
from werkzeug.security import generate_password_hash
from lab4.blueprint import *
from lab4.models import *


class TestPersonSchema(TestCase):
    def test_valid_person(self):
        person = PersonSchema().load({
            "idperson": 1,
            "email": "a@b.com",
            "password": "myPass",
            "creation_time": "2022-11-11T23:23",
            "role": "client",
            "firstname": "fname",
            "lastname": "lname",
            "birthdate": "2022-01-01",
            "pass_ser": "KA",
            "pass_num": "121212",
            "expirydate": "2022-02-02"
        })
        self.assertEqual(1, person["idperson"])
        self.assertEqual("a@b.com", person["email"])
        self.assertNotEqual("myPass", person["password"])
        self.assertEqual(datetime.datetime(2022, 11, 11, 23, 23), person["creation_time"])
        self.assertEqual("client", person["role"])
        self.assertEqual("fname", person["firstname"])
        self.assertEqual("lname", person["lastname"])
        self.assertEqual(datetime.date(2022, 1, 1), person["birthdate"])
        self.assertEqual("KA", person["pass_ser"])
        self.assertEqual("121212", person["pass_num"])
        self.assertEqual(datetime.date(2022, 2, 2), person["expirydate"])

    def test_missing_fields(self):
        with self.assertRaises(ValidationError):
            PersonSchema().load({});

    def test_bad_email(self):
        with self.assertRaises(ValidationError):
            PersonSchema().load({
                "idperson": 1,
                "email": "ab.com",
                "password": "password",
                "creation_time": "2022-11-11T23:23",
                "role": "client",
                "firstname": "fname",
                "lastname": "lname",
                "birthdate": "2022-01-01",
                "pass_ser": "KA",
                "pass_num": "121212",
                "expirydate": "2022-02-02"
            });

    def test_bad_role(self):
        with self.assertRaises(ValidationError):
            PersonSchema().load({
                "idperson": 1,
                "email": "a@b.com",
                "password": "password",
                "creation_time": "2022-11-11T23:23",
                "role": "bad_role",
                "firstname": "fname",
                "lastname": "lname",
                "birthdate": "2022-01-01",
                "pass_ser": "KA",
                "pass_num": "121212",
                "expirydate": "2022-02-02"
            })
    def test_bad_date(self):
        with self.assertRaises(ValidationError):
            PersonSchema().load({
                "idperson": 1,
                "email": "a@b.com",
                "password": "password",
                "creation_time": "2022-11-11T23:23",
                "role": "bad_role",
                "firstname": "fname",
                "lastname": "lname",
                "birthdate": "2022-0101",
                "pass_ser": "KA",
                "pass_num": "121212",
                "expirydate": "2022-02-02"
            })
    def test_bad_datetime(self):
        with self.assertRaises(ValidationError):
            PersonSchema().load({
                "idperson": 1,
                "email": "a@b.com",
                "password": "password",
                "creation_time": "2022-11-11",
                "role": "bad_role",
                "firstname": "fname",
                "lastname": "lname",
                "birthdate": "2022-01-01",
                "pass_ser": "KA",
                "pass_num": "121212",
                "expirydate": "2022-02-02"
            })


class TestPassengerSchema(TestCase):

    def test_valid_passenger(self):
        passenger = PassengerSchema().load({
            "idpassenger": 1,
            "email": "a@b.com",
            "firstname": "fname",
            "lastname": "lname",
            "birthdate": "2022-01-01",
            "pass_ser": "KA",
            "pass_num": "121212",
            "expirydate": "2022-02-02"
        })
        self.assertEqual(1, passenger["idpassenger"])
        self.assertEqual("a@b.com", passenger["email"])
        self.assertEqual("fname", passenger["firstname"])
        self.assertEqual("lname", passenger["lastname"])
        self.assertEqual(datetime.date(2022, 1, 1), passenger["birthdate"])
        self.assertEqual("KA", passenger["pass_ser"])
        self.assertEqual("121212", passenger["pass_num"])
        self.assertEqual(datetime.date(2022, 2, 2), passenger["expirydate"])

    def test_missing_fields(self):
        with self.assertRaises(ValidationError):
            PassengerSchema().load({})

    def test_bad_email(self):
        with self.assertRaises(ValidationError):
            PassengerSchema().load({
                "idpassenger": 1,
                "email": "ab.com",
                "firstname": "fname",
                "lastname": "lname",
                "birthdate": "2022-01-01",
                "pass_ser": "KA",
                "pass_num": "121212",
                "expirydate": "2022-02-02"
            })
    def test_bad_date(self):
        with self.assertRaises(ValidationError):
            PassengerSchema().load({
                "idpassenger": 1,
                "email": "ab@.com",
                "firstname": "fname",
                "lastname": "lname",
                "birthdate": "2022-0101",
                "pass_ser": "KA",
                "pass_num": "121212",
                "expirydate": "2022-02-02"
            })

class TestBookingSchema(TestCase):
    def valid_booking(self):

        booking = BookingSchema().load(
            {
                "idbooking" : 1,
                "total_price" : 200,
                 "personid" : 1
            }

        )
        self.assertEqual(1, booking["idbooking"])
    # idbooking= fields.Integer()
    # total_price=fields.Float(required=True)
    #

    # personid=fields.Integer(load_only=True)