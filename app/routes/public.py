from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.service import Service
from app.models.settings import Testimonial
from app.utils.i18n import get_lang

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    lang = get_lang()
    services = Service.query.filter_by(is_active=True).order_by(Service.order_index).all()
    testimonials = Testimonial.query.filter_by(is_active=True).order_by(Testimonial.order_index).all()
    return render_template('index.html', services=services, testimonials=testimonials, lang=lang)


@public_bp.route('/set-language/<lang_code>')
def set_language(lang_code):
    if lang_code in ('es', 'en'):
        session['lang'] = lang_code
    return redirect(request.referrer or url_for('public.index'))
