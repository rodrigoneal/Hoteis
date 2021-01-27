from typing import Optional
import json
from hotel.ext.database import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    __tablename__ = "usuarios"
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40))
    senha = db.Column(db.String(255))

    def __init__(self, login):
        self.login = login

    def json(self) -> json:
        return {"user_id": self.user_id, "login": self.login}

    @classmethod
    def find_user(cls, user_id: int) -> Optional:
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    @property
    def password(self):
        raise NotImplementedError

    @password.setter
    def password(self, value):
        self.senha = generate_password_hash(value)

    @classmethod
    def correct_user_and_password(cls, login, senha):
        user = cls.query.filter_by(login=login).first()
        if user and check_password_hash(user.senha, senha):
            return user
        return None

    def save_user(self):

        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
