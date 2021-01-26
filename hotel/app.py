from flask import Flask
from hotel.ext import configuration


def create_app():
    app = Flask(__name__)
    configuration.init_app(app)
    configuration.load_extensions(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
