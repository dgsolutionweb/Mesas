from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Criando as extensões
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializando as extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Registrando os blueprints
    from app.routes import auth, mesas, produtos, comandas, caixa, configuracoes, dashboard, cozinha
    app.register_blueprint(auth.bp)
    app.register_blueprint(mesas.bp)
    app.register_blueprint(produtos.bp)
    app.register_blueprint(comandas.bp)
    app.register_blueprint(caixa.bp)
    app.register_blueprint(configuracoes.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(cozinha.bp)

    # Carregando o usuário
    from app.models.models import Usuario
    @login_manager.user_loader
    def load_user(id):
        return Usuario.query.get(int(id))

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    with app.app_context():
        db.create_all()

    return app 