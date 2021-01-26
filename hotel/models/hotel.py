from hotel.ext.database import db


class HotelModel(db.Model):
    __tablename__ = "hotel"
    hotel_id = db.Column(db.String(), primary_key=True)
    nome = db.Column(db.String(50))
    estrelas = db.Column(db.Integer)
    diaria = db.Column(db.Float(2))
    cidade = db.Column(db.String(50))

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = str(cidade).lower()

    def json(self):
        return {
            "hotel_id": self.hotel_id,
            "nome": self.nome,
            "estrelas": self.estrelas,
            "diaria": self.diaria,
            "cidade": self.cidade,
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        return hotel if hotel else None

    def save_hotel(self):
        db.session.add(self)
        db.session.commit()

    def delete_hotel(self):
        db.session.delete(self)
        db.session.commit()
