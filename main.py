from flask import Flask, jsonify, request, Response
from lab4.models import *
from blueprint.py import *
from flask_swagger_ui import get_swaggerui_blueprint

def create_app(testing: bool = True):
    app = Flask(__name__)


    def dump_or_404(data, Schema):
        if data == 404:
            return Response("Invalid id", status=404)
        else:
            if isinstance(data, list):
                return jsonify(Schema.dump(data, many=True))
            return jsonify(Schema.dump(data))

    @app.route("/api/v1/users", methods=['GET'])#getAll
    def get_users():
        args = request.args

        if args != {}:
            response = Person.get_with_filter(args)
        else:
            response = Person.get_all()

        return jsonify(PersonSchema().dump(response, many=True))



if __name__ == "__main__":
    create_app().run(debug=True)