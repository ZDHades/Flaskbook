from .import bp as api
from flask import request, url_for, redirect, jsonify
from app.models import Post, User
from app import db
from datetime import datetime
from app.blueprints.shop.models import Product

# blog api routes

@api.route('/blog', methods=['GET'])
def get_posts():
    """
    [GET] api/blog
    """
    p = Post.query.all()
    return jsonify([_.to_dict() for _ in p])

@api.route('/blog/<int:id>', methods=['GET'])
def get_post(id):
    """
    [GET] api/blog/<id>
    """
    p = Post.query.get(id)
    return jsonify(p.to_dict())

@api.route('/blog', methods=['POST'])
def create_post():
    """
    [POST]/api/blog
    """
    r = request.get_json()
    p = Post()
    p.from_dict(r)
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201

@api.route('/blog/<int:id>', methods=['PUT'])
def edit_post(id):
    r = request.get_json()
    p = Post.query.get(id)
    p.body = r.get('body')
    p.updated_on = datetime.utcnow()
    db.session.commit()
    return jsonify(p.to_dict())

@api.route('/blog/<int:id>', methods=['DELETE'])
def delete_post(id):
    p = Post.query.get(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify([_.to_dict() for _ in Post.query.all()])


#  shop api routes

@api.route('/shop', methods=["GET"])
def get_products():
    """
    [GET] api/shop
    """
    s = Product.query.all()
    return jsonify([_.to_dict() for _ in s])


