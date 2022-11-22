from flask import Flask, jsonify, request, Response, Blueprint
from lab4.blueprint import api_blueprint
from flask_swagger_ui import get_swaggerui_blueprint
from lab4.models import * #Session, app, AdditionalPassenger, PassengerSchema, Booking, BookingSchema, Flight, FlightSchema, Seat, SeatSchema, Ticket, TicketSchema, Person, PersonSchema
# api_blueprint = Blueprint('api', __name__)


def create_app(testing: bool = True):
    app = Flask(__name__)
    # api_blueprint = Blueprint('api', __name__)

    def dump_or_404(data, Schema):
        if data == 404:
            return Response("Invalid id", status=404)
        else:
            if isinstance(data, list):
                return jsonify(Schema.dump(data, many=True))
            return jsonify(Schema.dump(data))

    @app.route("/users", methods=['GET'])#getAll
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
        user_object = Person(**user_json)

        response = Person.post_one(user_object)
        return Response(f"Status: {response}", status=response)
    return app

    @api_blueprint.route("/users/<id>", methods=['PUT'])
    def update_user(id):
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
    @api_blueprint.route("/api/v1/passengers", methods=['GET'])  # getAll
    def get_passengers():
        args = request.args
        #
        # if args != {}:
        #     response = AdditionalPassenger.get_with_filter(args)
        # else:
        response = Passenger.get_all()

        return jsonify(PassengerSchema().dump(response, many=True))

    @api_blueprint.route("/api/v1/passengers", methods=['POST'])
    def create_passenger():
        passenger_json = PassengerSchema().load(request.get_json())
        passenger_object = Passenger(**passenger_json)

        response = Passenger.post_one(passenger_object)
        return Response(f"Status: {response}", status=response)
    return app

    @api_blueprint.route("/api/v1/passengers/<id>", methods=['PUT'])
    def update_passenger(id):
        fields_to_update = PassengerSchema().load(request.get_json(), partial=True)

        response = Passenger.update_one(id, fields_to_update)
        return Response(f"status: {response}", status=response)

    @api_blueprint.route("/api/v1/passengers/<id>", methods=['GET'])
    def get_passenger(id):
        response = Passenger.get_preview(id)
        return dump_or_404(response, PassengerSchema())

#Booking

    @api_blueprint.route("/api/v1/bookings", methods=['POST'])
    def create_booking():
        booking_json = BookingSchema().load(request.get_json())
        booking_object = Booking(**booking_json)

        response = Booking.post_one(booking_object)
        return Response(f"Status: {response}", status=response)
    return app

    @api_blueprint.route("/api/v1/bookings/<id>", methods=['PUT'])
    def update_booking(id):
        fields_to_update = BookingSchema().load(request.get_json(), partial=True)

        response = Booking.update_one(id, fields_to_update)
        return Response(f"status: {response}", status=response)

    @api_blueprint.route("/api/v1/bookings/<id>", methods=['DELETE'])
    def delete_booking(id):
        response = Booking.delete_by_id(id)
        return Response(f"Status: {response}", status=response)

    @api_blueprint.route("/api/v1/bookings/<id>", methods=['GET'])
    def get_booking(id):
        response = Booking.get_preview(id)
        return dump_or_404(response, BookingSchema())

#Ticket
    @api_blueprint.route("/api/v1/tickets", methods=['POST'])
    def create_ticket():
        ticket_json = TicketSchema().load(request.get_json())
        ticket_object = Ticket(**ticket_json)

        response = Ticket.post_one(ticket_object)
        return Response(f"Status: {response}", status=response)
    return app

    @api_blueprint.route("/api/v1/tickets/<id>", methods=['PUT'])
    def update_ticket(id):
        fields_to_update = TicketSchema().load(request.get_json(), partial=True)

        response = Ticket.update_one(id, fields_to_update)
        return Response(f"status: {response}", status=response)

    @api_blueprint.route("/api/v1/tickets/<id>", methods=['DELETE'])
    def delete_ticket(id):
        response = Ticket.delete_by_id(id)
        return Response(f"Status: {response}", status=response)

    @api_blueprint.route("/api/v1/tickets/<id>", methods=['GET'])
    def get_ticket(id):
        response = Ticket.get_preview(id)
        return dump_or_404(response, TicketSchema())

#Seat

    @api_blueprint.route("/api/v1/tickets", methods=['POST'])
    def create_ticket():
        ticket_json = TicketSchema().load(request.get_json())
        ticket_object = Ticket(**ticket_json)

        response = Ticket.post_one(ticket_object)
        return Response(f"Status: {response}", status=response)

    return app

    @api_blueprint.route("/api/v1/tickets/<id>", methods=['PUT'])
    def update_ticket(id):
        fields_to_update = TicketSchema().load(request.get_json(), partial=True)

        response = Ticket.update_one(id, fields_to_update)
        return Response(f"status: {response}", status=response)

    @api_blueprint.route("/api/v1/tickets/<id>", methods=['DELETE'])
    def delete_ticket(id):
        response = Ticket.delete_by_id(id)
        return Response(f"Status: {response}", status=response)

    @api_blueprint.route("/api/v1/tickets/<id>", methods=['GET'])
    def get_ticket(id):
        response = Ticket.get_preview(id)
        return dump_or_404(response, TicketSchema())

if __name__ == "__main__":
    app.run()
