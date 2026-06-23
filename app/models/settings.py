from datetime import datetime
from app import db


class Testimonial(db.Model):
    __tablename__ = 'testimonials'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    text_es = db.Column(db.Text, nullable=False)
    text_en = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    is_active = db.Column(db.Boolean, default=True)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def text(self, lang='es'):
        return self.text_en if lang == 'en' else self.text_es


class SiteSettings(db.Model):
    __tablename__ = 'site_settings'

    id = db.Column(db.Integer, primary_key=True)
    whatsapp_number = db.Column(db.String(30), default='573000000000')
    site_name = db.Column(db.String(100), default='Arcanum')
    tagline_es = db.Column(db.String(200), default='Sabiduría ancestral para tu camino')
    tagline_en = db.Column(db.String(200), default='Ancestral wisdom for your path')
    contact_email = db.Column(db.String(150), default='contacto@arcanum.com')
    instagram_url = db.Column(db.String(200), default='')
    facebook_url = db.Column(db.String(200), default='')
    whatsapp_default_message_es = db.Column(
        db.Text,
        default='Hola, vengo de la página web y quiero más información sobre sus servicios.'
    )
    whatsapp_default_message_en = db.Column(
        db.Text,
        default='Hello, I came from the website and would like more information about your services.'
    )

    @staticmethod
    def get_settings():
        settings = SiteSettings.query.first()
        if not settings:
            settings = SiteSettings()
            db.session.add(settings)
            db.session.commit()
        return settings

    def whatsapp_message(self, lang='es'):
        return self.whatsapp_default_message_en if lang == 'en' else self.whatsapp_default_message_es
