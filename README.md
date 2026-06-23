# Arcanum — Sitio web de brujería y rituales

Sitio web completo, listo para funcionar, con:

- Landing page bilingüe (Español / Inglés) con animaciones
- Formulario de solicitud de consulta que se guarda en una base de datos
- Botón de WhatsApp que abre la conversación con el mensaje ya redactado
- Panel de administración (solo para ti, sin que los visitantes necesiten iniciar sesión) donde puedes:
  - Ver todos los pedidos/trabajos solicitados
  - Cambiar el estado de cada trabajo (nuevo, contactado, en proceso, completado, cancelado)
  - Llevar una bitácora/registro de las conversaciones de WhatsApp y llamadas de cada cliente
  - Administrar los servicios/rituales que se muestran en la web
  - Administrar los testimonios
  - Cambiar el número de WhatsApp, redes sociales, textos, etc.

---

## 1. Requisitos

- Python 3.10 o superior
- pip

---

## 2. Instalación

Abre una terminal dentro de la carpeta del proyecto y ejecuta:

```bash
# 1. Crear un entorno virtual (recomendado)
python3 -m venv venv

# 2. Activar el entorno virtual
# En Mac/Linux:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# 3. Instalar las dependencias
pip install -r requirements.txt

# 4. Ejecutar el sitio
python run.py
```

El sitio quedará disponible en: **http://localhost:5000**

La primera vez que lo ejecutes, se creará automáticamente la base de datos con:
- 6 servicios de ejemplo (amor, dinero, protección, salud, limpieza espiritual, tarot)
- 3 testimonios de ejemplo
- Un usuario administrador por defecto

---

## 3. Acceder al panel de administración

Ve a: **http://localhost:5000/admin/login**

Usuario y contraseña por defecto:

```
Usuario:    admin
Contraseña: cambiar123
```

**Importante: cambia esta contraseña apenas entres**, desde *Configuración → Cambiar contraseña* dentro del panel.

---

## 4. Configurar tu número de WhatsApp (paso obligatorio)

Por defecto el sitio usa un número de ejemplo. Para que el botón de WhatsApp y el formulario funcionen con tu número real:

1. Entra al panel admin → **Configuración**
2. En el campo **"Número de WhatsApp"** escribe tu número completo con código de país, **sin signos "+", espacios ni guiones**.
   - Ejemplo Colombia: `573001234567`
   - Ejemplo México: `5215512345678`
   - Ejemplo España: `34612345678`
3. Guarda los cambios.

---

## 5. Cómo funciona el flujo de pedidos

Como pediste, **los visitantes nunca necesitan crear una cuenta ni iniciar sesión**. El flujo es:

1. Un visitante completa el formulario "Solicita tu consulta" en la página principal.
2. Ese pedido se guarda automáticamente en la base de datos (lo puedes ver en el panel admin, en *Trabajos y pedidos*).
3. Al enviar el formulario, se abre WhatsApp en una pestaña nueva con un mensaje ya redactado dirigido a tu número, para que continúes la conversación ahí directamente.
4. Cuando hables con el cliente por WhatsApp, **vuelve al panel admin, entra al detalle de ese pedido y agrega un registro en la "Bitácora de seguimiento"** con el resumen de lo conversado. Así queda guardado el historial de cada trabajo dentro del sitio.

> Nota técnica importante: WhatsApp no permite que ninguna página web lea o guarde automáticamente los mensajes que se envían dentro de la app de WhatsApp — esa conversación ocurre fuera del sitio, en el teléfono del cliente y el tuyo. Por eso el panel incluye la bitácora manual: te toma unos segundos anotar el resumen de cada conversación y queda guardado para siempre en el admin, organizado por cliente y por pedido.

---

## 6. Estructura del proyecto

```
brujeria-web/
├── run.py                     ← Arranca el servidor
├── requirements.txt           ← Dependencias de Python
├── app/
│   ├── __init__.py            ← Configuración central de Flask
│   ├── models/                ← Tablas de la base de datos
│   │   ├── admin.py           ← Usuario administrador
│   │   ├── order.py           ← Pedidos y bitácora de notas
│   │   ├── service.py         ← Servicios/rituales
│   │   └── settings.py        ← Configuración del sitio y testimonios
│   ├── routes/                ← Lógica de cada sección
│   │   ├── public.py          ← Página principal pública
│   │   ├── admin.py           ← Panel de administración
│   │   └── api.py             ← Recepción de pedidos del formulario
│   ├── utils/
│   │   ├── i18n.py            ← Sistema de traducciones ES/EN
│   │   └── seed.py            ← Datos de ejemplo iniciales
│   ├── static/
│   │   ├── css/                ← Estilos del sitio público y del admin
│   │   └── js/                 ← Animaciones, formulario, panel admin
│   └── templates/
│       ├── base.html
│       ├── index.html         ← Página principal
│       ├── partials/          ← Header, footer, íconos
│       └── admin/             ← Todas las vistas del panel
└── instance/
    └── brujeria.db            ← Base de datos (se crea sola al arrancar)
```

---

## 7. Editar contenido del sitio

Todo el contenido editable está disponible desde el panel admin, sin tocar código:

- **Servicios**: admin → Servicios → Nuevo/Editar. Cada servicio tiene nombre, descripción, categoría, ícono y nota de precio en español e inglés.
- **Testimonios**: admin → Testimonios.
- **Datos generales** (nombre del sitio, WhatsApp, correo, redes sociales, mensaje predeterminado de WhatsApp): admin → Configuración.

---

## 8. Antes de publicar el sitio (producción)

Este proyecto está listo para desarrollo/pruebas locales. Antes de ponerlo en un servidor público:

1. Cambia la `SECRET_KEY` en `app/__init__.py` por una clave larga y aleatoria propia.
2. Cambia la contraseña del admin por defecto.
3. Usa un servidor de producción real en lugar del servidor de desarrollo de Flask, por ejemplo `gunicorn`:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 run:app
   ```
4. Considera usar HTTPS (la mayoría de proveedores de hosting lo configuran automáticamente).

---

## 9. Soporte de idiomas

El sitio detecta y recuerda el idioma elegido por el visitante (se guarda en su sesión). El selector ES/EN está en la esquina superior derecha del menú. Todo el contenido del sitio público (textos fijos, servicios, testimonios, formulario) está traducido.
