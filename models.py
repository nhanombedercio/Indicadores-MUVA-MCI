from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class CicloRevisao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(64), unique=True, nullable=False)
    estado = db.Column(db.String(20), default='pendente')
    nome_director = db.Column(db.String(120))
    data_revisao = db.Column(db.DateTime)
    observacoes_director = db.Column(db.Text)
    indicadores = db.relationship('IndicadorDado', backref='ciclo', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<CicloRevisao {self.titulo}>'


class IndicadorDado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ciclo_id = db.Column(db.Integer, db.ForeignKey('ciclo_revisao.id'), nullable=False)

    # Identidade (imutável, de data.py)
    codigo = db.Column(db.String(30))
    grupo = db.Column(db.String(20))
    tipo = db.Column(db.String(1))
    nome_original = db.Column(db.Text)
    definicao = db.Column(db.Text)
    meta_original = db.Column(db.String(50))

    # Preenchido pela equipa
    resultado_actual = db.Column(db.String(100))
    projectos = db.Column(db.Text)
    notas_equipa = db.Column(db.Text)

    # Editável pelo director
    nome_editado = db.Column(db.Text)
    meta_editada = db.Column(db.String(50))
    notas_director = db.Column(db.Text)

    # Decisões do director
    confirmado = db.Column(db.Boolean, default=False)
    propor_eliminacao = db.Column(db.Boolean, default=False)
    justificacao_eliminacao = db.Column(db.Text)

    @property
    def nome_vigente(self):
        return self.nome_editado if self.nome_editado else self.nome_original

    @property
    def meta_vigente(self):
        return self.meta_editada if self.meta_editada else self.meta_original

    @property
    def foi_editado_pelo_director(self):
        return bool(self.nome_editado or self.meta_editada)

    def __repr__(self):
        return f'<IndicadorDado {self.codigo}>'
