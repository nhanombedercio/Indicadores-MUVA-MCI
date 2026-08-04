from flask import Flask
from models import db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///mci_indicadores.db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['GESTAO_PASSWORD'] = os.getenv('GESTAO_PASSWORD', 'muva2026')

db.init_app(app)

from routes.revisao import revisao_bp
from routes.gestao import gestao_bp

app.register_blueprint(revisao_bp)
app.register_blueprint(gestao_bp, url_prefix='/gestao')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
