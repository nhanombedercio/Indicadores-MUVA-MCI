#!/usr/bin/env python
"""
Script para inicializar a base de dados.
Executar uma vez antes de arrancar a aplicação em produção.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Garantir que DATABASE_URL é local para desenvolvimento
if os.getenv('DATABASE_URL', '').startswith('/var/www'):
    print("⚠️ AVISO: DATABASE_URL apontando para caminho de produção.")
    print("Para desenvolvimento local, remova ou mude DATABASE_URL no .env")
    sys.exit(1)

from app import app, db

def init_database():
    """Inicializar a base de dados com as tabelas."""
    with app.app_context():
        print(f"Criando base de dados em: {os.getenv('DATABASE_URL', 'sqlite:///mci_indicadores.db')}")
        db.create_all()
        print("✓ Base de dados inicializada com sucesso!")
        print("✓ Tabelas criadas: CicloRevisao, IndicadorDado")

if __name__ == '__main__':
    init_database()
