from flask import Blueprint, request, jsonify
from database import db
from models import Transaction
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions', methods=['GET'])
def get_transactions():
    txns = Transaction.query.order_by(Transaction.date.desc()).all()
    return jsonify([t.to_dict() for t in txns])

@transactions_bp.route('/transactions/<int:id>', methods=['GET'])
def get_transaction(id):
    txn = Transaction.query.get_or_404(id)
    return jsonify(txn.to_dict())

@transactions_bp.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    txn = Transaction(
        title=data['title'],
        amount=data['amount'],
        type=data['type'],
        category_id=data.get('category_id'),
        note=data.get('note', ''),
        date=datetime.strptime(data['date'], '%Y-%m-%d') if 'date' in data else datetime.utcnow()
    )
    db.session.add(txn)
    db.session.commit()
    return jsonify(txn.to_dict()), 201

@transactions_bp.route('/transactions/<int:id>', methods=['PUT'])
def update_transaction(id):
    txn = Transaction.query.get_or_404(id)
    data = request.get_json()
    txn.title = data.get('title', txn.title)
    txn.amount = data.get('amount', txn.amount)
    txn.type = data.get('type', txn.type)
    txn.category_id = data.get('category_id', txn.category_id)
    txn.note = data.get('note', txn.note)
    db.session.commit()
    return jsonify(txn.to_dict())

@transactions_bp.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    txn = Transaction.query.get_or_404(id)
    db.session.delete(txn)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'})

@transactions_bp.route('/summary', methods=['GET'])
def get_summary():
    income = db.session.query(db.func.sum(Transaction.amount)).filter_by(type='income').scalar() or 0
    expense = db.session.query(db.func.sum(Transaction.amount)).filter_by(type='expense').scalar() or 0
    return jsonify({
        'total_income': income,
        'total_expense': expense,
        'balance': income - expense
    })