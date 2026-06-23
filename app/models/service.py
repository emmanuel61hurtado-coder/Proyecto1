from datetime import datetime
from app import db


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)

    # Campos bilingües
    name_es = db.Column(db.String(150), nullable=False)
    name_en = db.Column(db.String(150), nullable=False)
    description_es = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, nullable=False)

    category = db.Column(db.String(50), nullable=False, default='amor')
    # categorias: amor, dinero, proteccion, salud, espiritual

    icon = db.Column(db.String(50), default='moon')  # nombre de icono SVG
    price_note_es = db.Column(db.String(150))  # ej: "Desde consulta"
    price_note_en = db.Column(db.String(150))

    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    order_index = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='service', lazy=True)

    def name(self, lang='es'):
        return self.name_en if lang == 'en' else self.name_es

    def description(self, lang='es'):
        return self.description_en if lang == 'en' else self.description_es

    def price_note(self, lang='es'):
        note = self.price_note_en if lang == 'en' else self.price_note_es
        return note or ''

    def to_dict(self, lang='es'):
        return {
            'id': self.id,
            'name': self.name(lang),
            'description': self.description(lang),
            'category': self.category,
            'icon': self.icon,
            'price_note': self.price_note(lang),
            'is_featured': self.is_featured
        }

    def __repr__(self):
        return f'<Service {self.name_es}>'
