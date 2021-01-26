from datetime import timedelta
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from flask_restful import Resource, reqparse
from hotel.blacklist import BLACKLIST

from hotel.models.usuario import UserModel
from hotel.schema.serializer import UserSchema

atributos = reqparse.RequestParser()
atributos.add_argument(
    "login", type=str, required=True, help="The Field 'login' cannot be left blank "
)
atributos.add_argument(
    "senha", type=str, required=True, help="The Field 'senha' cannot be left blank "
)


class User(Resource):
    # /usuario/{user_id}

    def get(self, user_id):
        user_schema = UserSchema()
        user = UserModel.find_user(user_id)

        if user:
            return user_schema.dump(user)

        return {"message": "User not found."}, 404

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()

            return {"message": "User deleted."}
        return {"message": "User not found."}, 404


class UserRegister(Resource):
    def post(self):

        dados = atributos.parse_args()

        if UserModel.find_by_login(dados["login"]):
            return {"message": f"The login '{dados['login']}' already exists"}, 400
        user = UserModel(dados["login"])
        user.password = dados["senha"]
        try:
            user.save_user()
            return {"message": "User created successfully"}, 201
        except:
            return {"message": "An internal error ocurred trying to save hotel"}, 500


class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.correct_user_and_password(**dados)
        if user:
            token_de_acesso = create_access_token(
                identity=user.user_id, expires_delta=timedelta(minutes=2)
            )
            return {"access_token": token_de_acesso}, 200

        return {"message": "The Username or password is incorrect"}


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()["jti"]
        BLACKLIST.add(jwt_id)
        return {"message": "Logged out successfully! "}, 200
