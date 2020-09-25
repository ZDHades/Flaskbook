from app import db, create_app, cli
from app.models import User, Post
from flask import current_app as app
from app.blueprints.shop.models import Product

app = create_app()
cli.register(app)

@app.shell_context_processor
def shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Product': Product}


