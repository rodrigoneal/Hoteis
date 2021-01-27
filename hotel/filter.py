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
    cidade = parametros.get("cidade")
    estrelas_min = parametros.get("estrelas_min")
    estrelas_max = parametros.get("estrelas_max")
    diaria_min = parametros.get("diaria_min")
    diaria_max = parametros.get("diaria_max")
    limit = parametros.get("limit")
    offset = parametros.get("offset")
    if cidade:
        consulta = (
            HotelModel.query.filter(
                HotelModel.cidade.like("%" + cidade + "%"),
                and_(
                    HotelModel.estrelas >= estrelas_min,
                    HotelModel.estrelas <= estrelas_max,
                ),
                and_(HotelModel.diaria >= diaria_min, HotelModel.diaria <= diaria_max),
            )
            .limit(limit)
            .offset(offset)
            .all()
        )
        return consulta
    else:
        consulta = (
            HotelModel.query.filter(
                and_(
                    HotelModel.estrelas >= estrelas_min,
                    HotelModel.estrelas <= estrelas_max,
                ),
                and_(HotelModel.diaria >= diaria_min, HotelModel.diaria <= diaria_max),
            )
            .limit(limit)
            .offset(offset)
            .all()
        )
        return consulta
