from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route("/")
def index():
    return "<span style = 'color: red'>Wrong page</span>"


@app.route("/api/v1/hello-world-2")
def HelloWorld():
    return "<h1>Hello World 2</h1>"


if __name__ == '__main__':
    serve(app)
