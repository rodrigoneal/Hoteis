from flask_restful import Resource, reqparse
from hotel.models.hotel import HotelModel
from flask_jwt_extended import jwt_required
from hotel.schema.serializer import HotelSchema
from hotel.filter import normalize_path_params

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
        dados = path_params.parse_args()
        dados_validos = {
            chave: dados[chave] for chave in dados if dados[chave] is not None
        }
        parametros = normalize_path_params(**dados_validos)

        hotel_schema = HotelSchema(many=True)

        return {"hotel": hotel_schema.dump(parametros)}


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
