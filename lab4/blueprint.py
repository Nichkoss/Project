# #from flask import Blueprint
# import operator
# from flask import Flask, jsonify, request, Response, Blueprint
# #from lab4.app import *
# from flask_swagger_ui import get_swaggerui_blueprint
# from lab4.models import *
# api_blueprint = Blueprint('api', __name__)
# #session=Session()

from flask import Blueprint, request, jsonify,Response, make_response
from functools import wraps
from flask_cors import CORS
from marshmallow import ValidationError
#from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from werkzeug.security import check_password_hash
from flask_httpauth import HTTPBasicAuth
#from flask_swagger_ui import get_swaggerui_blueprint

from lab4.models import *

api_blueprint = Blueprint('api', __name__)

CORS(app)

auth = HTTPBasicAuth()





def auth_required(f):
     @wraps(f)
     def decorated(*args, **kwargs):
         auth= request.authorization
         if auth and auth.username=='test5@gmail.com' and auth.password =='12345':
            return f(*args, **kwargs)

         return make_response('couldnt verify your login or password!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
     return decorated
     # session = Session()
def auth_required_all(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'mgr4@gmail.com' and auth.password == '12345':
            return f(*args, **kwargs)

        return make_response('couldnt verify your login or password!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated
    # session = Session()
def auth__required(email, password):
    session = Session()
    persons = session.query(Person)
    users = [i.email for i in persons]
    if email in users:
        passs = session.query(Person).filter(Person.email == email).first()
        session.close()
        return check_password_hash(passs.password, password)
    return False
# def pass_required(func):
#     # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         password = request.headers.get('password')
#         if not token:
#             return jsonify({'Alert!': 'Password is missing!'}), 401
#
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'])
#         # You can use the JWT errors in exception
#         except jwt.InvalidTokenError:
#             return 'Invalid token. Please log in again.'
#         except:
#             return jsonify({'Message': 'Invalid token'}), 403
#
#         return func(*args, **kwargs)
#
#     return decorated

# def login_required(f):
#     @wraps(f)
#     def wrapped_view(**kwargs):
#         auth = request.authorization
#         if not (auth and check_auth(auth.username, auth.password)):
#             return ('Unauthorized', 401, {
#                 'WWW-Authenticate': 'Basic realm="Login Required"'
#             })
#
#         return f(**kwargs)
#
#     return wrapped_view
STUDENT_ID = 13
@api_blueprint.route("/hello-world")
@auth.login_required
def hello_world_def():
    return f"Hello world"
@api_blueprint.route(f"/hello-world-{STUDENT_ID}")
@auth.login_required
def hello_world():
    return f"Hello world {STUDENT_ID}"


#################################################################
# def create_app(testing: bool = True):
    app = Flask(__name__)
# bcrypt=Bcrypt(app)
@auth.verify_password
def verify_password(u_email, u_password):
    # users = [i.email for i in persons]
    # if email in users:
    #     passs = session.query(Person).filter(Person.email == email).first()
    #     session.close()

    session = Session()
    persons = session.query(Person)
    user_to_verify = session.query(Person).filter(Person.email == u_email).first()
    if not user_to_verify:
        return None #make_response('couldnt verify your login or password!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
    if check_password_hash(user_to_verify.password, u_password):
        print("email: " + u_email + ", password: " + u_password)
        return user_to_verify
    else:
        return None #make_response('couldnt verify your login or password!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@auth.error_handler
def auth_error_handler(status):
    message = ""
    if status == 401:
        message = "Wrong email or password"
    if status == 403:
        message = "Access denied"
    return {"code": status, "message": message}, status

# @auth.get_user_roles
# def get_user_roles(Person):
#     return Person.role
@auth.get_user_roles
def get_user_roles(user_to_get_role):
    print(user_to_get_role.role)
    return user_to_get_role.role
def dump_or_404(data, Schema):
    if data == 404:
        return Response("Invalid id", status=404)
    else:
        if isinstance(data, list):
            return jsonify(Schema.dump(data, many=True))
        return jsonify(Schema.dump(data))

@api_blueprint.route("/users/getall", methods=['GET'])#getAll
@auth.login_required(role='manager')
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
    #user_json['password']=bcrypt.generate_password_hash(user_json['password'])
    user_object = Person(**user_json)

    response = Person.post_one(user_object)
    return Response(f"Status: {response}", status=response)
    return app

@api_blueprint.route("/users/<id>", methods=['PUT'])
@auth.login_required(role=['client','manager'])
def update_user(id):
    fields_to_update = PersonSchema().load(request.get_json(), partial=True)

    response = Person.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)

@api_blueprint.route("/users/<id>/newstatus", methods=['PUT'])
@auth.login_required(role='manager')
def update_user_status(id):
    fields_to_update = PersonSchema().load(request.get_json(), partial=True)

    response = Person.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)

@api_blueprint.route("/users/<id>", methods=['DELETE'])
@auth.login_required(role='manager')
def delete_user(id):
    response = Person.delete_by_id(id)
    return Response(f"Status: {response}", status=response)

@api_blueprint.route("/users/<id>", methods=['GET'])
@auth.login_required(role=['client','manager'])
def get_user(id):
    response = Person.get_preview(id)
    return dump_or_404(response, PersonSchema())

#Additional_passenger
@api_blueprint.route("/passengers/getall", methods=['GET'])  # getAll
@auth.login_required(role='manager')
def get_passengers():
    args = request.args
    #
    # if args != {}:
    #     response = Passenger.get_with_filter(args)
    # else:
    response = Passenger.get_all()

    return jsonify(PassengerSchema().dump(response, many=True))

@api_blueprint.route("/passengers", methods=['POST'])
@auth.login_required(role='client')
def create_passenger():
    passenger_json = PassengerSchema().load(request.get_json())
    passenger_object = Passenger(**passenger_json)

    response = Passenger.post_one(passenger_object)
    return Response(f"Status: {response}", status=response)
    return app

@api_blueprint.route("/passengers/<id>", methods=['PUT'])
@auth.login_required(role='client')
def update_passenger(id):
    fields_to_update = PassengerSchema().load(request.get_json(), partial=True)

    response = Passenger.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)

@api_blueprint.route("/passengers/<id>", methods=['GET'])
@auth.login_required(role=['client','manager'])
def get_passenger(id):
    response = Passenger.get_preview(id)
    return dump_or_404(response, PassengerSchema())

#Booking
@api_blueprint.route("/bookings/getall", methods=['GET'])#getAll
@auth.login_required(role='manager')
def get_bookings():
    args = request.args

    if args != {}:
        response = Booking.get_with_filter(args)
    else:
        response = Booking.get_all()

    return jsonify(BookingSchema().dump(response, many=True))

@api_blueprint.route("/bookings", methods=['POST'])
@auth.login_required(role='client')
def create_booking():
    booking_json = BookingSchema().load(request.get_json())
    booking_object = Booking(**booking_json)

    response = Booking.post_one(booking_object)
    return Response(f"Status: {response}", status=response)
    return app

@api_blueprint.route("/bookings/<id>", methods=['PUT'])
@auth.login_required(role='client')
def update_booking(id):
    fields_to_update = BookingSchema().load(request.get_json(), partial=True)

    response = Booking.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)

@api_blueprint.route("/bookings/<id>/getdiscount", methods=['PUT'])
@auth.login_required(role='client')
def update_booking_price(id):
    fields_to_update = BookingSchema().load(request.get_json(), partial=True)

    response = Booking.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)
@api_blueprint.route("/bookings/<id>", methods=['DELETE'])
@auth.login_required(role='client')
def delete_booking(id):
    response = Booking.delete_by_id(id)
    return Response(f"Status: {response}", status=response)

@api_blueprint.route("/bookings/<id>", methods=['GET'])
@auth.login_required(role=['client','manager'])
def get_booking(id):
    response = Booking.get_preview(id)
    return dump_or_404(response, BookingSchema())

#Ticket
@api_blueprint.route("/tickets/getall", methods=['GET'])#getAll
@auth.login_required(role='manager')
def get_tickets():
    args = request.args

    if args != {}:
        response = Ticket.get_with_filter(args)
    else:
        response = Ticket.get_all()

    return jsonify(TicketSchema().dump(response, many=True))
@api_blueprint.route("/tickets", methods=['POST'])
@auth.login_required(role='client')
def create_ticket():
    ticket_json = TicketSchema().load(request.get_json())
    ticket_object = Ticket(**ticket_json)

    response = Ticket.post_one(ticket_object)
    return Response(f"Status: {response}", status=response)
    return app

@api_blueprint.route("/tickets/<id>", methods=['PUT'])
@auth.login_required(role='client')
def update_ticket(id):
    fields_to_update = TicketSchema().load(request.get_json(), partial=True)

    response = Ticket.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)

@api_blueprint.route("/tickets/<id>", methods=['DELETE'])
@auth.login_required(role='client')
def delete_ticket(id):
    response = Ticket.delete_by_id(id)
    return Response(f"Status: {response}", status=response)

@api_blueprint.route("/tickets/<id>", methods=['GET'])
@auth.login_required(role=['client','manager'])
def get_ticket(id):
    response = Ticket.get_preview(id)
    return dump_or_404(response, TicketSchema())

#Seat
@api_blueprint.route("/seats/getall", methods=['GET'])#getAll
@auth.login_required(role='manager')
def get_seats():
    args = request.args

    if args != {}:
        response = Seat.get_with_filter(args)
    else:
        response = Seat.get_all()

    return jsonify(SeatSchema().dump(response, many=True))
@api_blueprint.route("/seats", methods=['POST'])
@auth.login_required(role='manager')
def create_seat():
    seat_json = SeatSchema().load(request.get_json())
    seat_object = Seat(**seat_json)

    response = Seat.post_one(seat_object)
    return Response(f"Status: {response}", status=response)

    return app

@api_blueprint.route("/seats/<id>", methods=['PUT'])
@auth.login_required(role='manager')
def update_seat(id):
    fields_to_update = SeatSchema().load(request.get_json(), partial=True)

    response = Seat.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)

@api_blueprint.route("/seats/<id>", methods=['DELETE'])
@auth.login_required(role='manager')
def delete_seat(id):
    response = Seat.delete_by_id(id)
    return Response(f"Status: {response}", status=response)

@api_blueprint.route("/seats/<id>", methods=['GET'])
@auth.login_required(role=['client','manager'])
def get_seat(id):
    response = Seat.get_preview(id)
    return dump_or_404(response, SeatSchema())

#FLIGHT

@api_blueprint.route("/flights/getall", methods=['GET'])#getAll
@auth.login_required(role=['client','manager'])
def get_flights():
    args = request.args

    if args != {}:
        response = Flight.get_with_filter(args)
    else:
        response = Flight.get_all()

    return jsonify(FlightSchema().dump(response, many=True))
@api_blueprint.route("/flights", methods=['POST'])
@auth.login_required(role='manager')
def create_flight():
    flight_json = FlightSchema().load(request.get_json())
    flight_object = Flight(**flight_json)

    response = Flight.post_one(flight_object)
    return Response(f"Status: {response}", status=response)

    return app

@api_blueprint.route("/flights/<id>", methods=['PUT'])
@auth.login_required(role='manager')
def update_flight(id):
    fields_to_update = FlightSchema().load(request.get_json(), partial=True)

    response = Flight.update_one(id, fields_to_update)
    return Response(f"status: {response}", status=response)

@api_blueprint.route("/flights/<id>", methods=['DELETE'])
@auth.login_required(role='manager')
def delete_flight(id):
    response = Flight.delete_by_id(id)
    return Response(f"Status: {response}", status=response)

@api_blueprint.route("/flights/<id>", methods=['GET'])
@auth.login_required(role=['client','manager'])
def get_flight(id):
    response = Flight.get_preview(id)
    return dump_or_404(response, FlightSchema())

# @api_blueprint.route("/flights/<id>/freeseats", methods=['GET'])
# def get_flight_freeseats(id):
#     response = Flight.get_preview(id)
#     return dump_or_404(response, FlightSchema())
#
# @api_blueprint.route("/flights/<id>/usedseats", methods=['GET'])
# def get_flight_usedseats(id):
#     response = Flight.get_preview(id)
#     return dump_or_404(response, FlightSchema())

# @api_blueprint.route("/flights/<id>/freeseats", methods=['GET'])
# def get_freeseats_of_flight():
#     args = request.args
#
#     if args != {}:
#         response = Seat.get_with_filter(args)
#     else:
#         response = Seat.get_all()
#
#     return jsonify(SeatSchema().dump(response, many=True))

@api_blueprint.route("/flights/<id>/seats", methods=['GET'])#
@auth.login_required(role=['client','manager'])
def get_seats_for_flight(id):
    flight_object=Flight.get_by_id(id)
    if flight_object==404:
        return Response("Invalid id", status=404)
    else:
        return jsonify(SeatSchema().dump(Flight.get_seats(id), many=True))


if __name__ == "__main__":
    app.run(debug=True)


#test3@gmail.com
#mgr3@gmail.com