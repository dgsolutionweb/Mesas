from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128))
    cargo = db.Column(db.String(20), nullable=False)  # Gerente, Garçom, etc.

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Mesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.String(20), default='Livre')  # Livre, Ocupada, Reservada
    comandas = db.relationship('Comanda', backref='mesa', lazy=True)

class Comanda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesa.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    caixa_id = db.Column(db.Integer, db.ForeignKey('caixa_diario.id'), nullable=True)
    data_abertura = db.Column(db.DateTime, default=datetime.utcnow)
    data_fechamento = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Aberta')  # Aberta, Fechada
    itens = db.relationship('ItemComanda', backref='comanda', lazy=True)
    valor_total = db.Column(db.Float, default=0.0)
    usuario = db.relationship('Usuario', backref='comandas', lazy=True)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    disponivel = db.Column(db.Boolean, default=True)

class ItemComanda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comanda_id = db.Column(db.Integer, db.ForeignKey('comanda.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    observacao = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    produto = db.relationship('Produto', backref='itens_comanda')

class CaixaDiario(db.Model):
    __tablename__ = 'caixa_diario'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    valor_total = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='Aberto')  # Aberto, Fechado
    comandas = db.relationship('Comanda', backref='caixa', lazy=True)

class ConfiguracaoSistema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_restaurante = db.Column(db.String(120), nullable=False, default='DGSoluções')
    logo_path = db.Column(db.String(255))
    endereco = db.Column(db.String(255))
    telefone = db.Column(db.String(20))
    mensagem_rodape = db.Column(db.String(255), default='Sistema desenvolvido por DGSoluções')
    impressora_cozinha = db.Column(db.String(120), default='Microsoft Print to PDF')
    impressora_bar = db.Column(db.String(120), default='Microsoft Print to PDF')
    imprimir_pedidos_cozinha = db.Column(db.Boolean, default=True)
    imprimir_pedidos_bar = db.Column(db.Boolean, default=True)
    categorias_cozinha = db.Column(db.String(500), default='Pratos Principais,Entradas,Porções')
    categorias_bar = db.Column(db.String(500), default='Bebidas,Drinks')

class StatusPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_comanda_id = db.Column(db.Integer, db.ForeignKey('item_comanda.id'), nullable=False)
    status = db.Column(db.String(20), default='Pendente')  # Pendente, Em Preparo, Pronto, Entregue
    tempo_estimado = db.Column(db.Integer)  # em minutos
    inicio_preparo = db.Column(db.DateTime)
    fim_preparo = db.Column(db.DateTime)
    observacoes_cozinha = db.Column(db.String(200))
    
    item_comanda = db.relationship('ItemComanda', backref=db.backref('status_pedido', uselist=False))

class TempoPreparoPadrao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    tempo_padrao = db.Column(db.Integer, nullable=False)  # em minutos
    
    produto = db.relationship('Produto', backref='tempo_preparo', lazy=True) 