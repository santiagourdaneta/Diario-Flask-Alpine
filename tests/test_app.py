import json
from app import db, Post
from datetime import datetime

# Prueba unitaria para el modelo Post
# La prueba ahora acepta "client" como parámetro
def test_new_post(client):
    post = Post(content="Hola mundo")
    db.session.add(post)
    db.session.commit()
    
    # Se debe recargar el objeto de la base de datos para ver los valores por defecto
    retrieved_post = Post.query.filter_by(content="Hola mundo").first()

    assert retrieved_post.content == "Hola mundo"
    assert retrieved_post.likes == 0
    assert json.loads(retrieved_post.liked_by) == []
    assert isinstance(retrieved_post.timestamp, datetime)

# Prueba unitaria para la lógica de "Me gusta" en el modelo (indirecta)
def test_like_post_logic(client):
    # Crear un post de prueba
    post = Post(content="Probando likes")
    db.session.add(post)
    db.session.commit()

    # Simular dar "me gusta"
    response = client.post(f'/like_post/{post.id}', json={})
    assert response.status_code == 200
    assert json.loads(response.data)['likes'] == 1

    # Simular quitar "me gusta"
    response = client.post(f'/like_post/{post.id}', json={})
    assert response.status_code == 200
    assert json.loads(response.data)['likes'] == 0

# Prueba de integración: Obtener posts y paginación
def test_get_posts_pagination(client):
    # Crear 20 posts para simular paginación
    for i in range(20):
        db.session.add(Post(content=f"Post de prueba {i+1}"))
    db.session.commit()

    # Obtener la primera página (10 posts)
    response = client.get('/posts?page=1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['posts']) == 10
    assert data['has_next'] == True
    assert data['has_prev'] == False

    # Obtener la segunda página (10 posts restantes)
    response = client.get('/posts?page=2')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['posts']) == 10
    assert data['has_next'] == False
    assert data['has_prev'] == True

# Prueba E2E: Crear un post y verificar que los valores por defecto sean correctos
def test_create_and_view_post_e2e(client):
    # Simular la creación de un post desde la interfaz
    post_data = {'content': 'Este es un post de prueba E2E'}
    response = client.post('/create_post', json=post_data)
    assert response.status_code == 200

    # Verificar que el post ha sido creado correctamente en la base de datos
    new_post = Post.query.filter_by(content='Este es un post de prueba E2E').first()
    assert new_post is not None
    assert new_post.content == 'Este es un post de prueba E2E'
    assert new_post.likes == 0 # <-- La validación que fallaba
    assert json.loads(new_post.liked_by) == [] # <-- Validar la lista vacía

# Prueba de validación de caracteres
def test_create_post_too_long(client):
    long_content = "a" * 201
    response = client.post('/create_post', json={'content': long_content})
    assert response.status_code == 400
    assert "no puede superar los 200 caracteres" in json.loads(response.data)['error']

# Prueba de validación de post vacío
def test_create_post_empty(client):
    response = client.post('/create_post', json={'content': ''})
    assert response.status_code == 400
    assert "no puede estar vacío" in json.loads(response.data)['error']