from flask_jwt_extended import JWTManager
from flask import jsonify
from hotel.blacklist import BLACKLIST as blacklist


def init_app(app):
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def verifica_blacklist(token):
        return token["jti"] in blacklist

    @jwt.revoked_token_loader
    def token_de_acesso_invalidade():
        return jsonify({"message": "You Have been logged out."}), 401
