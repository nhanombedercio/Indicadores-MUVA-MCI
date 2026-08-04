#!/usr/bin/env python
"""
Script para inicializar a base de dados.
Executar uma vez antes de arrancar a aplicação em produção.
"""

import os
from dotenv import load_dotenv
from app import app, db

load_dotenv()

def init_database():
    """Inicializar a base de dados com as tabelas."""
    with app.app_context():
        print("Criando tabelas da base de dados...")
        db.create_all()
        print("✓ Base de dados inicializada com sucesso!")

        # Verificar número de indicadores carregados
        from models import IndicadorDado, CicloRevisao
        print(f"✓ Tabelas criadas: CicloRevisao, IndicadorDado")

if __name__ == '__main__':
    init_database()
