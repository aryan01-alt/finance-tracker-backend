from flask import Blueprint, request, jsonify
from database import db
from models import Category

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    cats = Category.query.all()
    return jsonify([c.to_dict() for c in cats])

@categories_bp.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    cat = Category(name=data['name'], type=data['type'])
    db.session.add(cat)
    db.session.commit()
    return jsonify(cat.to_dict()), 201