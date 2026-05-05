from flask import Flask
from flask_cors import CORS
from database import db, init_db
from routes.transactions import transactions_bp
from routes.categories import categories_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    init_db(app)
    app.register_blueprint(transactions_bp, url_prefix='/api')
    app.register_blueprint(categories_bp, url_prefix='/api')
    return app

# This is needed for gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)