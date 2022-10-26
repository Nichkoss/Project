from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route('/')
def home():
    return "boom"


@app.route('/api/v1/hello-world-13')
def about():
    return "Hello World 13"


if __name__ == '__main__':
    app.run(debug=True)
    serve(app)
