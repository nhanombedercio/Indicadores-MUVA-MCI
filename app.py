from flask import Flask
from models import db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuração de base de dados
database_url = os.getenv('DATABASE_URL', 'sqlite:////var/www/mci_indicadores/instance/mci_indicadores.db')
if database_url.startswith('sqlite:'):
    # Para SQLite em produção, usar caminho absoluto
    if not database_url.startswith('sqlite:////'):
        database_url = 'sqlite:////var/www/mci_indicadores/instance/mci_indicadores.db'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

# Segurança
secret_key = os.getenv('SECRET_KEY')
if not secret_key or secret_key == 'dev-secret-key':
    raise ValueError('SECRET_KEY não configurada ou usando default. Configure uma chave segura em .env')
app.config['SECRET_KEY'] = secret_key
app.config['GESTAO_PASSWORD'] = os.getenv('GESTAO_PASSWORD', 'muva2026')

# Desabilitar cache em desenvolvimento
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db.init_app(app)

from routes.revisao import revisao_bp
from routes.gestao import gestao_bp

app.register_blueprint(revisao_bp)
app.register_blueprint(gestao_bp, url_prefix='/gestao')

# Criar tabelas na primeira execução (apenas em desenvolvimento)
@app.before_request
def init_db():
    if not hasattr(app, '_db_initialized'):
        try:
            with app.app_context():
                db.create_all()
            app._db_initialized = True
        except Exception:
            pass

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)
