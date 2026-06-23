import re
from urllib.parse import quote
from flask import Blueprint, request, jsonify
from app import db
from app.models.order import Order
from app.models.service import Service
from app.models.settings import SiteSettings

api_bp = Blueprint('api', __name__)


def clean_phone(phone):
    return re.sub(r'[^\d+]', '', phone or '')


@api_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json(silent=True) or request.form

    name = (data.get('name') or '').strip()
    phone = (data.get('phone') or '').strip()
    email = (data.get('email') or '').strip()
    service_id = data.get('service_id')
    message = (data.get('message') or '').strip()
    preferred_time = (data.get('preferred_time') or '').strip()
    lang = data.get('lang', 'es')

    if not name or not phone:
        return jsonify({
            'ok': False,
            'error': 'missing_fields'
        }), 400

    service = None
    service_name = None
    if service_id:
        try:
            service = Service.query.get(int(service_id))
            if service:
                service_name = service.name_es
        except (ValueError, TypeError):
            pass

    order = Order(
        customer_name=name,
        customer_phone=phone,
        customer_email=email or None,
        service_id=service.id if service else None,
        service_name_snapshot=service_name,
        message=message or None,
        preferred_contact_time=preferred_time or None,
        lang=lang
    )
    db.session.add(order)
    db.session.commit()

    # Construir el link de WhatsApp con mensaje prellenado
    settings = SiteSettings.get_settings()
    wa_number = clean_phone(settings.whatsapp_number)

    if lang == 'en':
        wa_text = (
            f"Hello! My name is {name}.\n"
            f"I'd like to request: {service_name or 'a consultation'}.\n"
        )
        if message:
            wa_text += f"My situation: {message}\n"
        wa_text += f"\n(Reference code: {order.code})"
    else:
        wa_text = (
            f"Hola! Mi nombre es {name}.\n"
            f"Quiero solicitar: {service_name or 'una consulta'}.\n"
        )
        if message:
            wa_text += f"Mi situación: {message}\n"
        wa_text += f"\n(Código de referencia: {order.code})"

    wa_link = f"https://wa.me/{wa_number}?text={quote(wa_text)}"

    order.sent_to_whatsapp = True
    db.session.commit()

    return jsonify({
        'ok': True,
        'order_code': order.code,
        'whatsapp_link': wa_link
    })
