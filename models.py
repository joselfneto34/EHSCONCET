from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# 1. Usuários
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='Operacional') # 'Administrador', 'Supervisor', 'Operacional'
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 2. Empresas
class Empresa(db.Model):
    __tablename__ = 'empresas'
    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(150), nullable=False)
    nome_fantasia = db.Column(db.String(150))
    identificacao = db.Column(db.String(20), unique=True, nullable=False) # CNPJ ou CPF
    cnae = db.Column(db.String(10))
    grau_risco = db.Column(db.Integer)
    email = db.Column(db.String(100))
    ativo = db.Column(db.Boolean, default=True)
    colaboradores = db.relationship('Colaborador', backref='empresa_rel', lazy=True)

# 3. Colaboradores
class Colaborador(db.Model):
    __tablename__ = 'colaboradores'
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), unique=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True)
    cargo = db.Column(db.String(50))
    setor = db.Column(db.String(50))
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    status = db.Column(db.String(20), default='Ativo')
    ativo = db.Column(db.Boolean, default=True)
    entregas = db.relationship('EntregaEPI', backref='colaborador_rel', lazy=True)
    treinamentos = db.relationship('Treinamento', backref='colaborador_rel', lazy=True)

# 4. EPIs
class EPI(db.Model):
    __tablename__ = 'epis'
    id = db.Column(db.Integer, primary_key=True)
    ca = db.Column(db.String(20), unique=True)
    descricao = db.Column(db.String(200))
    fabricante = db.Column(db.String(100))
    estoque = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=5)
    valor_unitario = db.Column(db.Float, default=0.0)
    ativo = db.Column(db.Boolean, default=True)

# 5. Registro de Entregas
class EntregaEPI(db.Model):
    __tablename__ = 'entregas_epi'
    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaboradores.id'), nullable=False)
    epi_id = db.Column(db.Integer, db.ForeignKey('epis.id'), nullable=False)
    data_entrega = db.Column(db.DateTime, default=datetime.utcnow)
    data_vencimento = db.Column(db.DateTime) 

# 6. Treinamentos
class Treinamento(db.Model):
    __tablename__ = 'treinamentos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaboradores.id'), nullable=False)
    data_realizacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_vencimento = db.Column(db.DateTime, nullable=False)
