from hotel.ext.serializer import ma
from hotel.models.usuario import UserModel
from hotel.models.hotel import HotelModel
from marshmallow_sqlalchemy import field_for


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    user_id = ma.auto_field()
    login = ma.auto_field()


class HotelSchema(ma.SQLAlchemyAutoSchema):
    hotel_id = field_for(HotelModel, 'hotel_id', dump_only=True)
    nome = field_for(HotelModel, 'nome', dump_only=True)
    estrelas = field_for(HotelModel, 'estrelas', dump_only=True)
    diaria = field_for(HotelModel, 'diaria', dump_only=True)
    cidade = field_for(HotelModel, 'cidade', dump_only=True)

    class Meta:
        meta = HotelModel
        load_instance = True
        ordered = True
