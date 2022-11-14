# #from flask import Blueprint
# import operator
# from flask import Flask, jsonify, request, Response, Blueprint
# #from lab4.app import *
# from flask_swagger_ui import get_swaggerui_blueprint
# from lab4.models import *
# api_blueprint = Blueprint('api', __name__)
# #session=Session()

import operator

from flask import Blueprint, request, jsonify,Response
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
#from flask_swagger_ui import get_swaggerui_blueprint

from lab4.models import *

api_blueprint = Blueprint('api', __name__)

# session = Session()
STUDENT_ID = 13
@api_blueprint.route("/hello-world")
def hello_world_def():
    return f"Hello world"


@api_blueprint.route(f"/hello-world-{STUDENT_ID}")
def hello_world():
    return f"Hello world {STUDENT_ID}"

#################################################################
# def create_app(testing: bool = True):
    app = Flask(__name__)
bcrypt=Bcrypt(app)

def dump_or_404(data, Schema):
    if data == 404:
        return Response("Invalid id", status=404)
    else:
        if isinstance(data, list):
            return jsonify(Schema.dump(data, many=True))
        return jsonify(Schema.dump(data))

@api_blueprint.route("/users", methods=['GET'])#getAll
def get_users():
    args = request.args

    if args != {}:
        response = Person.get_with_filter(args)
    else:
        response = Person.get_all()

    return jsonify(PersonSchema().dump(response, many=True))

@api_blueprint.route("/users", methods=['POST'])
def create_user():
    user_json = PersonSchema().load(request.get_json())
    user_json['password']=bcrypt.generate_password_hash(user_json['password'])
    user_object = Person(**user_json)

    response = Person.post_one(user_object)
    return Response(f"Status: {response}", status=response)
    return app

@api_blueprint.route("/users/<id>", methods=['PUT'])
def update_user(id):
    fields_to_update = PersonSchema().load(request.get_json(), partial=True)

    response = Person.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)

@api_blueprint.route("/users/<id>/newstatus", methods=['PUT'])
def update_user_status(id):
    fields_to_update = PersonSchema().load(request.get_json(), partial=True)

    response = Person.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)

@api_blueprint.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
    response = Person.delete_by_id(id)
    return Response(f"Status: {response}", status=response)

@api_blueprint.route("/users/<id>", methods=['GET'])
def get_user(id):
    response = Person.get_preview(id)
    return dump_or_404(response, PersonSchema())

#Additional_passenger
@api_blueprint.route("/passengers", methods=['GET'])  # getAll
def get_passengers():
    args = request.args
    #
    # if args != {}:
    #     response = Passenger.get_with_filter(args)
    # else:
    response = Passenger.get_all()

    return jsonify(PassengerSchema().dump(response, many=True))

@api_blueprint.route("/passengers", methods=['POST'])
def create_passenger():
    passenger_json = PassengerSchema().load(request.get_json())
    passenger_object = Passenger(**passenger_json)

    response = Passenger.post_one(passenger_object)
    return Response(f"Status: {response}", status=response)
    return app

@api_blueprint.route("/passengers/<id>", methods=['PUT'])
def update_passenger(id):
    fields_to_update = PassengerSchema().load(request.get_json(), partial=True)

    response = Passenger.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)

@api_blueprint.route("/passengers/<id>", methods=['GET'])
def get_passenger(id):
    response = Passenger.get_preview(id)
    return dump_or_404(response, PassengerSchema())

#Booking
@api_blueprint.route("/bookings", methods=['GET'])#getAll
def get_bookings():
    args = request.args

    if args != {}:
        response = Booking.get_with_filter(args)
    else:
        response = Booking.get_all()

    return jsonify(BookingSchema().dump(response, many=True))

@api_blueprint.route("/bookings", methods=['POST'])
def create_booking():
    booking_json = BookingSchema().load(request.get_json())
    booking_object = Booking(**booking_json)

    response = Booking.post_one(booking_object)
    return Response(f"Status: {response}", status=response)
    return app

@api_blueprint.route("/bookings/<id>", methods=['PUT'])
def update_booking(id):
    fields_to_update = BookingSchema().load(request.get_json(), partial=True)

    response = Booking.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)

@api_blueprint.route("/bookings/<id>/getdiscount", methods=['PUT'])
def update_booking_price(id):
    fields_to_update = BookingSchema().load(request.get_json(), partial=True)

    response = Booking.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)
@api_blueprint.route("/bookings/<id>", methods=['DELETE'])
def delete_booking(id):
    response = Booking.delete_by_id(id)
    return Response(f"Status: {response}", status=response)

@api_blueprint.route("/bookings/<id>", methods=['GET'])
def get_booking(id):
    response = Booking.get_preview(id)
    return dump_or_404(response, BookingSchema())

#Ticket
@api_blueprint.route("/tickets", methods=['GET'])#getAll
def get_tickets():
    args = request.args

    if args != {}:
        response = Ticket.get_with_filter(args)
    else:
        response = Ticket.get_all()

    return jsonify(TicketSchema().dump(response, many=True))
@api_blueprint.route("/tickets", methods=['POST'])
def create_ticket():
    ticket_json = TicketSchema().load(request.get_json())
    ticket_object = Ticket(**ticket_json)

    response = Ticket.post_one(ticket_object)
    return Response(f"Status: {response}", status=response)
    return app

@api_blueprint.route("/tickets/<id>", methods=['PUT'])
def update_ticket(id):
    fields_to_update = TicketSchema().load(request.get_json(), partial=True)

    response = Ticket.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)

@api_blueprint.route("/tickets/<id>", methods=['DELETE'])
def delete_ticket(id):
    response = Ticket.delete_by_id(id)
    return Response(f"Status: {response}", status=response)

@api_blueprint.route("/tickets/<id>", methods=['GET'])
def get_ticket(id):
    response = Ticket.get_preview(id)
    return dump_or_404(response, TicketSchema())

#Seat
@api_blueprint.route("/seats", methods=['GET'])#getAll
def get_seats():
    args = request.args

    if args != {}:
        response = Seat.get_with_filter(args)
    else:
        response = Seat.get_all()

    return jsonify(SeatSchema().dump(response, many=True))
@api_blueprint.route("/seats", methods=['POST'])
def create_seat():
    seat_json = SeatSchema().load(request.get_json())
    seat_object = Seat(**seat_json)

    response = Seat.post_one(seat_object)
    return Response(f"Status: {response}", status=response)

    return app

@api_blueprint.route("/seats/<id>", methods=['PUT'])
def update_seat(id):
    fields_to_update = SeatSchema().load(request.get_json(), partial=True)

    response = Seat.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)

@api_blueprint.route("/seats/<id>", methods=['DELETE'])
def delete_seat(id):
    response = Seat.delete_by_id(id)
    return Response(f"Status: {response}", status=response)

@api_blueprint.route("/seats/<id>", methods=['GET'])
def get_seat(id):
    response = Seat.get_preview(id)
    return dump_or_404(response, SeatSchema())

#FLIGHT

@api_blueprint.route("/flights", methods=['GET'])#getAll
def get_flights():
    args = request.args

    if args != {}:
        response = Flight.get_with_filter(args)
    else:
        response = Flight.get_all()

    return jsonify(FlightSchema().dump(response, many=True))
@api_blueprint.route("/flights", methods=['POST'])
def create_flight():
    flight_json = FlightSchema().load(request.get_json())
    flight_object = Flight(**flight_json)

    response = Flight.post_one(flight_object)
    return Response(f"Status: {response}", status=response)

    return app

@api_blueprint.route("/flights/<id>", methods=['PUT'])
def update_flight(id):
    fields_to_update = FlightSchema().load(request.get_json(), partial=True)

    response = Flight.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)

@api_blueprint.route("/flights/<id>", methods=['DELETE'])
def delete_flight(id):
    response = Flight.delete_by_id(id)
    return Response(f"Status: {response}", status=response)

@api_blueprint.route("/flights/<id>", methods=['GET'])
def get_flight(id):
    response = Flight.get_preview(id)
    return dump_or_404(response, FlightSchema())

@api_blueprint.route("/flights/<id>/freeseats", methods=['GET'])
def get_flight_freeseats(id):
    response = Flight.get_preview(id)
    return dump_or_404(response, FlightSchema())

@api_blueprint.route("/flights/<id>/usedseats", methods=['GET'])
def get_flight_usedseats(id):
    response = Flight.get_preview(id)
    return dump_or_404(response, FlightSchema())

if __name__ == "__main__":
    app.run(debug=True)
