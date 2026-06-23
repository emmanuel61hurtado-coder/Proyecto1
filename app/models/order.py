import secrets
from datetime import datetime
from app import db


def generate_order_code():
    return 'ORD-' + secrets.token_hex(4).upper()


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, default=generate_order_code, nullable=False)

    # Datos del cliente
    customer_name = db.Column(db.String(150), nullable=False)
    customer_phone = db.Column(db.String(30), nullable=False)
    customer_email = db.Column(db.String(150))
    customer_birthdate = db.Column(db.String(20))  # opcional, comun en consultas esotericas

    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    service_name_snapshot = db.Column(db.String(150))  # por si el servicio se borra despues

    message = db.Column(db.Text)  # detalle que escribe el cliente sobre su caso
    preferred_contact_time = db.Column(db.String(100))
    lang = db.Column(db.String(5), default='es')

    status = db.Column(db.String(30), default='nuevo')
    # estados: nuevo, contactado, en_proceso, completado, cancelado

    is_read = db.Column(db.Boolean, default=False)
    sent_to_whatsapp = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    notes = db.relationship('OrderNote', backref='order', lazy=True,
                             order_by='OrderNote.created_at', cascade='all, delete-orphan')

    STATUS_LABELS = {
        'nuevo': {'es': 'Nuevo', 'en': 'New', 'color': '#d4af37'},
        'contactado': {'es': 'Contactado', 'en': 'Contacted', 'color': '#7e6ad6'},
        'en_proceso': {'es': 'En proceso', 'en': 'In progress', 'color': '#3b82c4'},
        'completado': {'es': 'Completado', 'en': 'Completed', 'color': '#4a9d6e'},
        'cancelado': {'es': 'Cancelado', 'en': 'Cancelled', 'color': '#a14444'},
    }

    def status_label(self, lang='es'):
        return self.STATUS_LABELS.get(self.status, {}).get(lang, self.status)

    def status_color(self):
        return self.STATUS_LABELS.get(self.status, {}).get('color', '#888')

    def __repr__(self):
        return f'<Order {self.code}>'


class OrderNote(db.Model):
    """
    Bitacora / registro de conversacion de cada trabajo.
    El admin va guardando aqui manualmente el resumen de lo hablado por
    WhatsApp con el cliente, asi queda historial dentro del panel.
    """
    __tablename__ = 'order_notes'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)

    author = db.Column(db.String(80), default='Admin')
    note_type = db.Column(db.String(20), default='nota')  # nota, llamada, whatsapp, sistema
    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<OrderNote {self.id} for Order {self.order_id}>'
