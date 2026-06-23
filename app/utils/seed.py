from app import db
from app.models.admin import Admin
from app.models.service import Service
from app.models.settings import SiteSettings, Testimonial


def seed_initial_data():
    # Crear admin por defecto si no existe ninguno
    if Admin.query.count() == 0:
        admin = Admin(username='admin')
        admin.set_password('cambiar123')
        db.session.add(admin)

    # Configuración del sitio
    SiteSettings.get_settings()

    # Servicios de ejemplo
    if Service.query.count() == 0:
        services = [
            Service(
                name_es='Amarre de amor', name_en='Love binding ritual',
                description_es='Un ritual ancestral para atraer, fortalecer o recuperar el amor de esa persona especial, trabajando desde la raíz del sentimiento.',
                description_en='An ancestral ritual to attract, strengthen, or recover the love of that special person, working from the root of the feeling.',
                category='amor', icon='heart', price_note_es='Previa consulta', price_note_en='By consultation',
                is_featured=True, order_index=1
            ),
            Service(
                name_es='Tarot del destino', name_en='Tarot of destiny',
                description_es='Lectura profunda de las cartas para iluminar tu presente y mostrarte los caminos que se abren ante ti.',
                description_en='A deep card reading to illuminate your present and reveal the paths opening before you.',
                category='espiritual', icon='star', price_note_es='Consulta individual', price_note_en='Individual session',
                is_featured=True, order_index=2
            ),
            Service(
                name_es='Limpieza espiritual', name_en='Spiritual cleansing',
                description_es='Ritual de purificación para liberar cargas energéticas, malas vibras y bloqueos que no te dejan avanzar.',
                description_en='A purification ritual to release energetic burdens, bad vibes, and blocks holding you back.',
                category='espiritual', icon='leaf', price_note_es='Previa consulta', price_note_en='By consultation',
                is_featured=False, order_index=3
            ),
            Service(
                name_es='Ritual de prosperidad', name_en='Prosperity ritual',
                description_es='Trabajo enfocado en abrir los caminos del dinero, el trabajo y la abundancia en tu vida.',
                description_en='A working focused on opening the paths of money, work, and abundance in your life.',
                category='dinero', icon='coin', price_note_es='Previa consulta', price_note_en='By consultation',
                is_featured=True, order_index=4
            ),
            Service(
                name_es='Protección y blindaje', name_en='Protection & shielding',
                description_es='Ritual de protección para alejar envidias, malas energías y personas que desean hacerte daño.',
                description_en='A protection ritual to ward off envy, bad energy, and people who wish you harm.',
                category='proteccion', icon='shield', price_note_es='Previa consulta', price_note_en='By consultation',
                is_featured=False, order_index=5
            ),
            Service(
                name_es='Sanación energética', name_en='Energy healing',
                description_es='Trabajo de armonización para restaurar tu equilibrio físico, emocional y espiritual.',
                description_en='A harmonization session to restore your physical, emotional, and spiritual balance.',
                category='salud', icon='sun', price_note_es='Previa consulta', price_note_en='By consultation',
                is_featured=False, order_index=6
            ),
        ]
        db.session.bulk_save_objects(services)

    # Testimonios de ejemplo
    if Testimonial.query.count() == 0:
        testimonials = [
            Testimonial(
                customer_name='M. Fernanda',
                text_es='Sentí un acompañamiento real durante todo el proceso. Hoy mi situación cambió por completo.',
                text_en='I felt real support throughout the whole process. My situation has completely changed today.',
                rating=5, order_index=1
            ),
            Testimonial(
                customer_name='Carlos R.',
                text_es='La consulta fue clara, honesta y respetuosa. Recomiendo totalmente la experiencia.',
                text_en='The consultation was clear, honest, and respectful. I fully recommend the experience.',
                rating=5, order_index=2
            ),
            Testimonial(
                customer_name='Daniela P.',
                text_es='Encontré paz y claridad en un momento muy difícil de mi vida. Eternamente agradecida.',
                text_en='I found peace and clarity during a very difficult time in my life. Eternally grateful.',
                rating=5, order_index=3
            ),
            Testimonial(
                customer_name='Valentina Londoño',
                text_es='El ritual de amarre que me hicieron fue exactamente lo que necesitaba. En menos de dos semanas las cosas empezaron a fluir como nunca. No lo puedo creer.',
                text_en='The love binding ritual was exactly what I needed. In less than two weeks things started flowing like never before. I can barely believe it.',
                rating=5, order_index=4
            ),
            Testimonial(
                customer_name='Santiago Mejía',
                text_es='Llegué escéptico, pero la limpieza espiritual cambió mi perspectiva. Sentí una paz que no tenía hace años. Ahora duermo bien y todo fluye mejor.',
                text_en='I arrived skeptical, but the spiritual cleansing changed my perspective. I felt a peace I hadnt felt in years. Now I sleep well and everything flows better.',
                rating=5, order_index=5
            ),
            Testimonial(
                customer_name='Laura Castaño',
                text_es='Me hicieron una lectura de tarot y fue tan precisa que se me erizó la piel. Describió situaciones que nadie más podía saber. Volveré sin dudar.',
                text_en='I had a tarot reading and it was so accurate it gave me goosebumps. It described situations no one else could know. I will return without hesitation.',
                rating=5, order_index=6
            ),
            Testimonial(
                customer_name='Andrés Rivera',
                text_es='El ritual de prosperidad me ayudó a conseguir el trabajo que tanto buscaba. Después de meses de intentarlo, en tres semanas todo cambió.',
                text_en='The prosperity ritual helped me get the job I had been looking for. After months of trying, everything changed in three weeks.',
                rating=5, order_index=7
            ),
            Testimonial(
                customer_name='Carolina Vargas',
                text_es='Tenía muchas dudas antes de consultar, pero desde la primera llamada sentí una conexión sincera. Me orientaron con mucha sabiduría y paciencia.',
                text_en='I had many doubts before consulting, but from the first call I felt a sincere connection. They guided me with great wisdom and patience.',
                rating=5, order_index=8
            ),
            Testimonial(
                customer_name='Felipe Orozco',
                text_es='El blindaje de protección me quitó un peso de encima. Dejaron de pasarme cosas raras en la casa y mi energía cambió totalmente.',
                text_en='The protection shielding lifted a weight off my shoulders. Strange things stopped happening at home and my energy changed completely.',
                rating=5, order_index=9
            ),
            Testimonial(
                customer_name='Manuela Restrepo',
                text_es='Pasé por una ruptura muy dolorosa y el ritual de sanación energética me devolvió la esperanza. Ahora entiendo que todo pasa por algo.',
                text_en='I went through a very painful breakup and the energy healing ritual gave me back my hope. Now I understand everything happens for a reason.',
                rating=5, order_index=10
            ),
            Testimonial(
                customer_name='Ricardo Gómez',
                text_es='Mi esposa notó el cambio antes que yo. Estoy más tranquilo, más enfocado y las cosas en el negocio mejoraron notablemente.',
                text_en='My wife noticed the change before I did. I am calmer, more focused, and things at the business improved noticeably.',
                rating=4, order_index=11
            ),
            Testimonial(
                customer_name='Juliana Ángel',
                text_es='Recomiendo este espacio con los ojos cerrados. Todo fue serio, respetuoso y con resultados reales. La lectura de cartas fue impresionantemente certera.',
                text_en='I recommend this space with my eyes closed. Everything was serious, respectful, and with real results. The card reading was impressively accurate.',
                rating=5, order_index=12
            ),
            Testimonial(
                customer_name='Pedro Hernández',
                text_es='No sabía qué esperar, pero la consulta me aclaró muchas dudas que traía guardadas. Me fui sintiendo mucho más liviano y en paz.',
                text_en='I did not know what to expect, but the consultation cleared up many doubts I had been carrying. I left feeling much lighter and at peace.',
                rating=4, order_index=13
            ),
            Testimonial(
                customer_name='Ana Sofía Torres',
                text_es='Hice el ritual para el amor propio y no para atraer a alguien más. El cambio interno fue enorme. Hoy me quiero como nunca me había querido.',
                text_en='I did the ritual for self-love, not to attract someone else. The internal change was enormous. Today I love myself like never before.',
                rating=5, order_index=14
            ),
            Testimonial(
                customer_name='Diego Alzate',
                text_es='Desde que me hicieron la limpieza espiritual siento que me quitaron una venda de los ojos. Mi relación con mi familia mejoró drásticamente.',
                text_en='Since I had the spiritual cleansing, I feel like a blindfold was removed from my eyes. My relationship with my family improved dramatically.',
                rating=5, order_index=15
            ),
        ]
        db.session.bulk_save_objects(testimonials)

    db.session.commit()
