from flask_restful import Resource, reqparse
from hotel.models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3
from sqlalchemy import and_


def normalize_path_params(
    cidade=None,
    estrelas_min=0,
    estrelas_max=5,
    diaria_min=0,
    diaria_max=10000,
    limit=50,
    offset=0,
    **kwargs,
):
    if cidade:
        return {
            "estrelas_min": estrelas_min,
            "estrelas_max": estrelas_max,
            "diaria_min": diaria_min,
            "diaria_max": diaria_max,
            "cidade": cidade,
            "limit": limit,
            "offset": offset,
        }

    return {
        "estrelas_min": estrelas_min,
        "estrelas_max": estrelas_max,
        "diaria_min": diaria_min,
        "diaria_max": diaria_max,
        "limit": limit,
        "offset": offset,
    }


path_params = reqparse.RequestParser()
path_params.add_argument("cidade", type=str)
path_params.add_argument("estrelas_min", type=int)
path_params.add_argument("estrelas_max", type=int)
path_params.add_argument("diaria_min", type=float)
path_params.add_argument("diaria_max", type=float)
path_params.add_argument("limit", type=int)
path_params.add_argument("offset", type=int)


class Hoteis(Resource):
    def get(self):

        connection = sqlite3.connect("banco.db")
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {
            chave: dados[chave] for chave in dados if dados[chave] is not None
        }
        parametros = normalize_path_params(**dados_validos)

        if parametros.get("cidade"):
            consulta = (
                HotelModel.query.filter(
                    HotelModel.cidade == parametros.get("cidade"),
                    and_(
                        HotelModel.estrelas > parametros.get("estrelas_min"),
                        HotelModel.estrelas < parametros.get("estrelas_max"),
                    ),
                    and_(
                        HotelModel.diaria > parametros.get("diaria_min"),
                        HotelModel.diaria < parametros.get("diaria_max"),
                    ),
                )
                .limit(parametros.get("limit"))
                .offset(parametros.get("offset"))
            )
        else:
            consulta = (
                HotelModel.query.filter(
                    and_(
                        HotelModel.estrelas > parametros.get("estrelas_min"),
                        HotelModel.estrelas < parametros.get("estrelas_max"),
                    ),
                    and_(
                        HotelModel.diaria > parametros.get("diaria_min"),
                        HotelModel.diaria < parametros.get("diaria_max"),
                    ),
                )
                .limit(parametros.get("limit"))
                .offset(parametros.get("offset"))
            )

        resposta = [resp.json() for resp in consulta]
        return {"hotel": resposta}


class Hotel(Resource):
    argumento = reqparse.RequestParser()
    argumento.add_argument(
        "nome", required=True, type=str, help="The field 'nome' cannot be left blank."
    )
    argumento.add_argument(
        "estrelas",
        required=True,
        type=str,
        help="The field 'estrela' cannot be left blank.",
    )
    argumento.add_argument("diaria")
    argumento.add_argument("cidade")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {"message": "Hotel not found."}, 404

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": f"Hotel id '{hotel_id}' already exists"}, 400

        dados = self.argumento.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save hotel"}, 500
        return hotel.json()

    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.argumento.parse_args()

        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            for key, value in dados.items():
                setattr(hotel_encontrado, key, value)
            try:
                hotel_encontrado.save_hotel()
            except:
                return {
                    "message": "An internal error ocurred trying to save hotel"
                }, 500
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {
                    "message": "An internal error ocurred trying to delete hotel"
                }, 500
            return {"message": "hotel deleted."}
        return {"message": "hotel not found"}, 404
