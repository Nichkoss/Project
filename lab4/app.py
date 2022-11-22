from flask import Flask
#from gevent.pywsgi import WSGIServer
from wsgiref.simple_server import make_server
from flask_cors import CORS
from lab4.blueprint import api_blueprint
#from lab4.models import *

app = Flask(__name__)
CORS(app)

app.register_blueprint(api_blueprint, url_prefix="/api/v1")
if __name__ == "__main__":
    with make_server('', 5000, app) as server:
        server.serve_forever()

