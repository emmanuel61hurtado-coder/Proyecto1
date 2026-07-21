from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.admin import Admin
from app.models.order import Order, OrderNote
from app.models.service import Service
from app.models.settings import SiteSettings, Testimonial

admin_bp = Blueprint('admin', __name__)


@admin_bp.context_processor
def inject_unread_count():
    try:
        count = Order.query.filter_by(is_read=False).count()
    except Exception:
        count = 0
    return {'unread_count': count}


# ---------- AUTH ----------

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin.dashboard'))
        flash('Usuario o contraseña incorrectos.', 'error')

    return render_template('admin/login.html')


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


# ---------- DASHBOARD ----------

@admin_bp.route('/')
@login_required
def dashboard():
    total_orders = Order.query.count()
    new_orders = Order.query.filter_by(status='nuevo').count()
    in_progress = Order.query.filter_by(status='en_proceso').count()
    completed = Order.query.filter_by(status='completado').count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(8).all()

    return render_template(
        'admin/dashboard.html',
        total_orders=total_orders,
        new_orders=new_orders,
        in_progress=in_progress,
        completed=completed,
        recent_orders=recent_orders
    )


# ---------- ORDERS (Trabajos / Pedidos) ----------

@admin_bp.route('/orders')
@login_required
def orders_list():
    status_filter = request.args.get('status', 'all')
    query = Order.query

    if status_filter != 'all':
        query = query.filter_by(status=status_filter)

    orders = query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders, status_filter=status_filter)


@admin_bp.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    if not order.is_read:
        order.is_read = True
        db.session.commit()
    services = Service.query.filter_by(is_active=True).all()
    return render_template('admin/order_detail.html', order=order, services=services)


@admin_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@login_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')

    if new_status in Order.STATUS_LABELS:
        old_status = order.status
        order.status = new_status
        order.updated_at = datetime.utcnow()

        note = OrderNote(
            order_id=order.id,
            author=current_user.username,
            note_type='sistema',
            content=f'Estado cambiado de "{old_status}" a "{new_status}".'
        )
        db.session.add(note)
        db.session.commit()
        flash('Estado actualizado correctamente.', 'success')

    return redirect(url_for('admin.order_detail', order_id=order.id))


@admin_bp.route('/orders/<int:order_id>/notes', methods=['POST'])
@login_required
def add_order_note(order_id):
    order = Order.query.get_or_404(order_id)
    content = request.form.get('content', '').strip()
    note_type = request.form.get('note_type', 'nota')

    if content:
        note = OrderNote(
            order_id=order.id,
            author=current_user.username,
            note_type=note_type,
            content=content
        )
        db.session.add(note)
        order.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Registro guardado en la bitácora.', 'success')
    else:
        flash('La nota no puede estar vacía.', 'error')

    return redirect(url_for('admin.order_detail', order_id=order.id))


@admin_bp.route('/orders/<int:order_id>/delete', methods=['POST'])
@login_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Pedido eliminado.', 'success')
    return redirect(url_for('admin.orders_list'))


# ---------- SERVICES ----------

@admin_bp.route('/services')
@login_required
def services_list():
    services = Service.query.order_by(Service.order_index).all()
    return render_template('admin/services.html', services=services)


@admin_bp.route('/services/new', methods=['GET', 'POST'])
@login_required
def service_new():
    if request.method == 'POST':
        service = Service(
            name_es=request.form.get('name_es', '').strip(),
            name_en=request.form.get('name_en', '').strip(),
            description_es=request.form.get('description_es', '').strip(),
            description_en=request.form.get('description_en', '').strip(),
            category=request.form.get('category', 'amor'),
            icon=request.form.get('icon', 'moon'),
            price_note_es=request.form.get('price_note_es', '').strip(),
            price_note_en=request.form.get('price_note_en', '').strip(),
            is_active='is_active' in request.form,
            is_featured='is_featured' in request.form,
            order_index=int(request.form.get('order_index', 0) or 0)
        )
        db.session.add(service)
        db.session.commit()
        flash('Servicio creado correctamente.', 'success')
        return redirect(url_for('admin.services_list'))

    return render_template('admin/service_form.html', service=None)


@admin_bp.route('/services/<int:service_id>/edit', methods=['GET', 'POST'])
@login_required
def service_edit(service_id):
    service = Service.query.get_or_404(service_id)

    if request.method == 'POST':
        service.name_es = request.form.get('name_es', '').strip()
        service.name_en = request.form.get('name_en', '').strip()
        service.description_es = request.form.get('description_es', '').strip()
        service.description_en = request.form.get('description_en', '').strip()
        service.category = request.form.get('category', 'amor')
        service.icon = request.form.get('icon', 'moon')
        service.price_note_es = request.form.get('price_note_es', '').strip()
        service.price_note_en = request.form.get('price_note_en', '').strip()
        service.is_active = 'is_active' in request.form
        service.is_featured = 'is_featured' in request.form
        service.order_index = int(request.form.get('order_index', 0) or 0)

        db.session.commit()
        flash('Servicio actualizado correctamente.', 'success')
        return redirect(url_for('admin.services_list'))

    return render_template('admin/service_form.html', service=service)


@admin_bp.route('/services/<int:service_id>/delete', methods=['POST'])
@login_required
def service_delete(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash('Servicio eliminado.', 'success')
    return redirect(url_for('admin.services_list'))


# ---------- TESTIMONIALS ----------

@admin_bp.route('/testimonials')
@login_required
def testimonials_list():
    testimonials = Testimonial.query.order_by(Testimonial.order_index).all()
    return render_template('admin/testimonials.html', testimonials=testimonials)


@admin_bp.route('/testimonials/new', methods=['GET', 'POST'])
@login_required
def testimonial_new():
    if request.method == 'POST':
        t = Testimonial(
            customer_name=request.form.get('customer_name', '').strip(),
            text_es=request.form.get('text_es', '').strip(),
            text_en=request.form.get('text_en', '').strip(),
            rating=int(request.form.get('rating', 5) or 5),
            is_active='is_active' in request.form,
            order_index=int(request.form.get('order_index', 0) or 0)
        )
        db.session.add(t)
        db.session.commit()
        flash('Testimonio creado correctamente.', 'success')
        return redirect(url_for('admin.testimonials_list'))

    return render_template('admin/testimonial_form.html', testimonial=None)


@admin_bp.route('/testimonials/<int:t_id>/edit', methods=['GET', 'POST'])
@login_required
def testimonial_edit(t_id):
    t = Testimonial.query.get_or_404(t_id)

    if request.method == 'POST':
        t.customer_name = request.form.get('customer_name', '').strip()
        t.text_es = request.form.get('text_es', '').strip()
        t.text_en = request.form.get('text_en', '').strip()
        t.rating = int(request.form.get('rating', 5) or 5)
        t.is_active = 'is_active' in request.form
        t.order_index = int(request.form.get('order_index', 0) or 0)
        db.session.commit()
        flash('Testimonio actualizado correctamente.', 'success')
        return redirect(url_for('admin.testimonials_list'))

    return render_template('admin/testimonial_form.html', testimonial=t)


@admin_bp.route('/testimonials/<int:t_id>/delete', methods=['POST'])
@login_required
def testimonial_delete(t_id):
    t = Testimonial.query.get_or_404(t_id)
    db.session.delete(t)
    db.session.commit()
    flash('Testimonio eliminado.', 'success')
    return redirect(url_for('admin.testimonials_list'))


# ---------- SETTINGS ----------

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    site_settings = SiteSettings.get_settings()

    if request.method == 'POST':
        site_settings.site_name = request.form.get('site_name', '').strip()
        site_settings.whatsapp_number = request.form.get('whatsapp_number', '').strip()
        site_settings.tagline_es = request.form.get('tagline_es', '').strip()
        site_settings.tagline_en = request.form.get('tagline_en', '').strip()
        site_settings.contact_email = request.form.get('contact_email', '').strip()
        site_settings.instagram_url = request.form.get('instagram_url', '').strip()
        site_settings.facebook_url = request.form.get('facebook_url', '').strip()
        site_settings.tiktok_url = request.form.get('tiktok_url', '').strip()
        site_settings.whatsapp_default_message_es = request.form.get('whatsapp_default_message_es', '').strip()
        site_settings.whatsapp_default_message_en = request.form.get('whatsapp_default_message_en', '').strip()
        db.session.commit()
        flash('Configuración guardada correctamente.', 'success')
        return redirect(url_for('admin.settings'))

    return render_template('admin/settings.html', settings=site_settings)


@admin_bp.route('/account/password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not current_user.check_password(current_password):
        flash('La contraseña actual no es correcta.', 'error')
    elif len(new_password) < 6:
        flash('La nueva contraseña debe tener al menos 6 caracteres.', 'error')
    elif new_password != confirm_password:
        flash('Las contraseñas nuevas no coinciden.', 'error')
    else:
        current_user.set_password(new_password)
        db.session.commit()
        flash('Contraseña actualizada correctamente.', 'success')

    return redirect(url_for('admin.settings'))
