from flask import request, session

TRANSLATIONS = {
    'es': {
        # Navegación
        'nav_home': 'Inicio',
        'nav_services': 'Servicios',
        'nav_about': 'Sobre mí',
        'nav_testimonials': 'Testimonios',
        'nav_contact': 'Contacto',
        'nav_order': 'Solicitar consulta',

        # Hero
        'hero_eyebrow': 'Consulta privada y confidencial',
        'hero_cta_primary': 'Solicitar mi consulta',
        'hero_cta_secondary': 'Escribir por WhatsApp',
        'hero_scroll': 'Descubre el camino',

        # Sobre mí
        'about_title': 'El sendero que recorro',
        'about_years_label': 'años de práctica',
        'about_clients_label': 'consultas atendidas',
        'about_countries_label': 'países alcanzados',

        # Servicios
        'services_eyebrow': 'Lo que ofrezco',
        'services_title': 'Trabajos y rituales',
        'services_subtitle': 'Cada consulta es única. Estos son los caminos que más recorro junto a quienes me buscan.',
        'service_cta': 'Pedir este trabajo',
        'category_amor': 'Amor',
        'category_dinero': 'Dinero y prosperidad',
        'category_proteccion': 'Protección',
        'category_salud': 'Salud y bienestar',
        'category_espiritual': 'Limpieza espiritual',

        # Proceso
        'process_eyebrow': 'Cómo trabajamos',
        'process_title': 'Tu consulta, paso a paso',
        'process_step1_title': 'Cuéntame tu caso',
        'process_step1_text': 'Completas el formulario o me escribes directo por WhatsApp con tu situación.',
        'process_step2_title': 'Analizo tu energía',
        'process_step2_text': 'Reviso tu caso con calma y te contacto personalmente para profundizar.',
        'process_step3_title': 'Trazamos el ritual',
        'process_step3_text': 'Te explico qué trabajo es el indicado, tiempos y lo que necesitas saber.',
        'process_step4_title': 'Acompañamiento',
        'process_step4_text': 'Te guío durante todo el proceso hasta ver resultados.',

        # Testimonios
        'testimonials_eyebrow': 'Voces del camino',
        'testimonials_title': 'Lo que cuentan quienes ya consultaron',

        # Formulario de pedido
        'order_eyebrow': 'Da el primer paso',
        'order_title': 'Solicita tu consulta',
        'order_subtitle': 'Cuéntame brevemente tu situación. Te responderé por WhatsApp lo antes posible, en total confidencialidad.',
        'form_name': 'Tu nombre',
        'form_phone': 'Número de WhatsApp',
        'form_email': 'Correo electrónico (opcional)',
        'form_service': 'Tipo de consulta',
        'form_service_placeholder': 'Selecciona un servicio',
        'form_message': 'Cuéntame tu situación',
        'form_message_placeholder': 'Describe brevemente lo que está pasando y qué te gustaría lograr...',
        'form_preferred_time': '¿Mejor horario para contactarte? (opcional)',
        'form_submit': 'Enviar y continuar en WhatsApp',
        'form_privacy': 'Tu información es confidencial y solo se usa para responder tu consulta.',
        'form_success_title': 'Solicitud recibida',
        'form_success_text': 'Te estamos redirigiendo a WhatsApp para continuar la conversación...',
        'form_error': 'Por favor completa los campos obligatorios.',

        # Footer
        'footer_rights': 'Todos los derechos reservados.',
        'footer_disclaimer': 'Servicios con fines espirituales y de acompañamiento personal. Los resultados pueden variar según cada persona.',
        'footer_whatsapp': 'Escríbeme por WhatsApp',

        # Admin
        'admin_login_title': 'Acceso al panel',
        'admin_username': 'Usuario',
        'admin_password': 'Contraseña',
        'admin_login_btn': 'Ingresar',
        'admin_dashboard': 'Panel de control',
        'admin_orders': 'Trabajos y pedidos',
        'admin_services': 'Servicios',
        'admin_testimonials': 'Testimonios',
        'admin_settings': 'Configuración',
        'admin_logout': 'Cerrar sesión',
    },
    'en': {
        'nav_home': 'Home',
        'nav_services': 'Services',
        'nav_about': 'About me',
        'nav_testimonials': 'Testimonials',
        'nav_contact': 'Contact',
        'nav_order': 'Request a consultation',

        'hero_eyebrow': 'Private and confidential consultation',
        'hero_cta_primary': 'Request my consultation',
        'hero_cta_secondary': 'Message on WhatsApp',
        'hero_scroll': 'Discover the path',

        'about_title': 'The path I walk',
        'about_years_label': 'years of practice',
        'about_clients_label': 'consultations attended',
        'about_countries_label': 'countries reached',

        'services_eyebrow': 'What I offer',
        'services_title': 'Rituals and spiritual work',
        'services_subtitle': 'Every consultation is unique. These are the paths I walk most often with those who seek me out.',
        'service_cta': 'Request this work',
        'category_amor': 'Love',
        'category_dinero': 'Money and prosperity',
        'category_proteccion': 'Protection',
        'category_salud': 'Health and wellbeing',
        'category_espiritual': 'Spiritual cleansing',

        'process_eyebrow': 'How we work',
        'process_title': 'Your consultation, step by step',
        'process_step1_title': 'Tell me your case',
        'process_step1_text': 'Fill out the form or message me directly on WhatsApp with your situation.',
        'process_step2_title': 'I read your energy',
        'process_step2_text': 'I review your case calmly and contact you personally to go deeper.',
        'process_step3_title': 'We trace the ritual',
        'process_step3_text': 'I explain which work fits your case, timing, and what you need to know.',
        'process_step4_title': 'Guidance',
        'process_step4_text': 'I guide you through the entire process until you see results.',

        'testimonials_eyebrow': 'Voices from the path',
        'testimonials_title': 'What those who already consulted say',

        'order_eyebrow': 'Take the first step',
        'order_title': 'Request your consultation',
        'order_subtitle': "Tell me briefly about your situation. I'll reply on WhatsApp as soon as possible, in complete confidentiality.",
        'form_name': 'Your name',
        'form_phone': 'WhatsApp number',
        'form_email': 'Email (optional)',
        'form_service': 'Type of consultation',
        'form_service_placeholder': 'Select a service',
        'form_message': 'Tell me your situation',
        'form_message_placeholder': "Briefly describe what's happening and what you'd like to achieve...",
        'form_preferred_time': 'Best time to contact you? (optional)',
        'form_submit': 'Send and continue on WhatsApp',
        'form_privacy': 'Your information is confidential and only used to respond to your inquiry.',
        'form_success_title': 'Request received',
        'form_success_text': "We're redirecting you to WhatsApp to continue the conversation...",
        'form_error': 'Please complete the required fields.',

        'footer_rights': 'All rights reserved.',
        'footer_disclaimer': 'Services for spiritual and personal guidance purposes. Results may vary for each person.',
        'footer_whatsapp': 'Message me on WhatsApp',

        'admin_login_title': 'Panel access',
        'admin_username': 'Username',
        'admin_password': 'Password',
        'admin_login_btn': 'Sign in',
        'admin_dashboard': 'Dashboard',
        'admin_orders': 'Orders & work',
        'admin_services': 'Services',
        'admin_testimonials': 'Testimonials',
        'admin_settings': 'Settings',
        'admin_logout': 'Log out',
    }
}


def get_lang():
    lang = request.args.get('lang')
    if lang in ('es', 'en'):
        session['lang'] = lang
        return lang
    return session.get('lang', 'es')


def get_translations(lang):
    return TRANSLATIONS.get(lang, TRANSLATIONS['es'])
