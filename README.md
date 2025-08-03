# Diario-Flask-Alpine: Un Diario Moderno con Python, Flask y Alpine.js

## Descripción del Proyecto

**Diario-Flask-Alpine** es una aplicación web minimalista y de alto rendimiento. Fue creada para demostrar cómo construir aplicaciones web modernas y reactivas utilizando un stack tecnológico ligero y eficiente: **Python**, **Flask** y **Alpine.js**.

La arquitectura del proyecto es ideal para desarrolladores que buscan:
-   Aprender a integrar un backend robusto en Python con una interfaz de usuario interactiva y sin complejidad.
-   Entender cómo implementar funciones esenciales como la **protección CSRF** y la **limitación de peticiones (rate-limiting)**.
-   Construir aplicaciones web escalables sin depender de grandes frameworks de JavaScript.

## Características Clave

-   **Backend en Python/Flask:** Un backend minimalista y potente que maneja la lógica de negocio y la interacción con la base de datos.
-   **Frontend Reactivo con Alpine.js:** Una interfaz de usuario ligera que gestiona el estado y las interacciones del usuario de manera declarativa.
-   **Funcionalidad Completa del Diario:**
    -   Creación y visualización de posts.
    -   Sistema de "me gusta" en tiempo real.
    -   Paginación para gestionar grandes volúmenes de posts.
-   **Seguridad:**
    -   **Protección CSRF:** Prevención de ataques de falsificación de peticiones en sitios cruzados.
    -   **Rate-Limiting:** Controla la cantidad de peticiones que un usuario puede realizar en un período de tiempo, protegiendo contra ataques DDoS básicos.
-   **Base de Datos SQLite:** Fácil de configurar y perfecta para el desarrollo y despliegues pequeños.

## Tecnologías Utilizadas

-   **Backend:**
    -   [Python](https://www.python.org/)
    -   [Flask](https://flask.palletsprojects.com/)
    -   [Flask-Limiter](https://flask-limiter.readthedocs.io/)
    -   [Flask-WTF](https://flask-wtf.readthedocs.io/)
    -   [SQLAlchemy](https://www.sqlalchemy.org/)
-   **Frontend:**
    -   [Alpine.js](https://alpinejs.dev/)
    -   [Pico.css](https://picocss.com/)
-   **Pruebas de Estrés:**
    -   [Locust](https://locust.io/)
-   **Pruebas Unitarias:**
    -   [Pytest](https://docs.pytest.org/)

## Configuración y Ejecución

1.  **Clona el repositorio:**
    `git clone https://github.com/santiagourdaneta/Diario-Flask-Alpine/`
    `cd Diario-Flask-Alpine`

2.  **Crea y activa un entorno virtual:**
    `python -m venv venv`
    -   En Windows: `venv\Scripts\activate`
    -   En macOS/Linux: `source venv/bin/activate`

3.  **Instala las dependencias:**
    `pip install -r requirements.txt`

4.  **Ejecuta la aplicación:**
    `python app.py`

5.  **Abre tu navegador** y visita `http://localhost:5000` para ver el diario en acción.

## Contribuciones

Las contribuciones son bienvenidas. Siéntete libre de abrir un **issue** o enviar un **pull request**.

---
