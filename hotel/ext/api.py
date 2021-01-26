from flask_restful import Api
from hotel.resources.hotel import Hoteis, Hotel
from hotel.resources.usuario import User, UserLogin, UserRegister, UserLogout


def init_app(app):
    api = Api(app)
    api.add_resource(User, "/usuarios/<int:user_id>")
    api.add_resource(UserRegister, "/cadastro")
    api.add_resource(UserLogin, "/login")
    api.add_resource(UserLogout, "/logout")
    api.add_resource(Hoteis, "/hoteis")
    api.add_resource(Hotel, "/hoteis/<string:hotel_id>")
