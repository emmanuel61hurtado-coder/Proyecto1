import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambia-esta-clave-en-produccion-12345')

    # ── Base de datos ─────────────────────────────────────────────────────────
    # En producción (Docker/Coolify) se usa DATABASE_URL con PostgreSQL.
    # En desarrollo local se usa SQLite como fallback.
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Coolify / Heroku pueden entregar 'postgres://' en lugar de 'postgresql://'
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Fallback a SQLite para desarrollo local
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            'sqlite:///' + os.path.join(basedir, 'instance', 'brujeria.db')
        )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'app', 'static', 'uploads')

    # Asegurar que existan las carpetas necesarias
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Por favor inicia sesión para continuar.'
    login_manager.login_message_category = 'error'

    from app.models.admin import Admin

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # Registrar blueprints
    from app.routes.public import public_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Context processor para traducciones e info global del sitio
    from app.utils.i18n import get_translations, get_lang
    from app.models.settings import SiteSettings

    @app.context_processor
    def inject_globals():
        from datetime import datetime
        lang = get_lang()
        return {
            't': get_translations(lang),
            'current_lang': lang,
            'site': SiteSettings.get_settings(),
            'now_year': datetime.utcnow().year
        }

    with app.app_context():
        db.create_all()
        from app.utils.seed import seed_initial_data
        seed_initial_data()

    return app

