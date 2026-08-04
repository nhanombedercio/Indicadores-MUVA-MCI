"""
Entry point para Gunicorn em produção.
Executar com: gunicorn wsgi:app
"""

import os
from dotenv import load_dotenv

load_dotenv()

from app import app

if __name__ == '__main__':
    app.run()
