from hotel.models.hotel import HotelModel
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
        parametros = {
            "estrelas_min": estrelas_min,
            "estrelas_max": estrelas_max,
            "diaria_min": diaria_min,
            "diaria_max": diaria_max,
            "cidade": cidade,
            "limit": limit,
            "offset": offset,
        }
    else:
        parametros = {
            "estrelas_min": estrelas_min,
            "estrelas_max": estrelas_max,
            "diaria_min": diaria_min,
            "diaria_max": diaria_max,
            "limit": limit,
            "offset": offset,
        }
    if parametros.get("cidade"):

        consulta = (
            HotelModel.query.filter(
                HotelModel.cidade.like("%" + parametros.get("cidade") + "%"),
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
        return consulta
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
        return consulta
