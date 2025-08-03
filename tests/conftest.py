import pytest
from app import app, db, Post

@pytest.fixture
def client():
    # Establece la configuración de la base de datos para las pruebas
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Usa una base de datos en memoria

    with app.test_client() as client:
        with app.app_context():
            db.create_all() # Crea las tablas para la prueba
            yield client
            db.drop_all() # Elimina las tablas después de la prueba