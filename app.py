import json
import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, timezone
import bleach
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# La libreta ahora tiene un nuevo campo para la fecha
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    likes = db.Column(db.Integer, default=0)
    liked_by = db.Column(db.String(200), default='[]')
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    posts = []
    for post in pagination.items:
        posts.append({
            'id': post.id,
            'content': post.content,
            'likes': post.likes,
            'liked_by': json.loads(post.liked_by),
            # Enviamos la fecha formateada
            'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M')
        })
    
    return jsonify({
        'posts': posts,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
        'page': pagination.page,
    })

@app.route('/create_post', methods=['POST'])
@csrf.exempt
@limiter.limit("5 per minute") # <-- Limite más estricto para crear posts
def create_post():
    data = request.json
    content = data.get('content')

    if not content or len(content.strip()) == 0:
        return jsonify({"error": "El mensaje no puede estar vacío"}), 400
    if len(content) > 200: # <-- Nueva validación
        return jsonify({"error": "El mensaje no puede superar los 200 caracteres"}), 400    

     # Limpiamos el contenido del mensaje antes de guardarlo
    clean_content = bleach.clean(content, tags=[], attributes={}, strip=True)    

    new_post = Post(content=clean_content)
    db.session.add(new_post)
    db.session.commit()
    # Devolvemos el post con la fecha
    return jsonify(id=new_post.id, content=new_post.content, likes=new_post.likes, liked_by=[], timestamp=new_post.timestamp.strftime('%Y-%m-%d %H:%M'))

@csrf.exempt
@app.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    post = db.session.get(Post, post_id) or Post.query.filter_by(id=post_id).first_or_404()
    current_user_id = 'user-001'
    liked_by = json.loads(post.liked_by)

    if current_user_id in liked_by:
        liked_by.remove(current_user_id)
        post.likes -= 1
    else:
        liked_by.append(current_user_id)
        post.likes += 1
    
    post.liked_by = json.dumps(liked_by)
    db.session.commit()
    return jsonify(likes=post.likes, liked_by_user=current_user_id in liked_by)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)