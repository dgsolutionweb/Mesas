from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_caching import Cache
from flask_session import Session
from .config import Config

# Inicialização das extensões
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cache = Cache()
sess = Session()

@login_manager.user_loader
def load_user(user_id):
    from .models.models import Usuario
    return Usuario.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cache.init_app(app)
    sess.init_app(app)
    
    # Configuração do Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    # Importar blueprints
    from .routes import auth, mesas, produtos, comandas, caixa, dashboard, cozinha, configuracoes, main
    
    # Registrar blueprints
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(mesas.bp)
    app.register_blueprint(produtos.bp)
    app.register_blueprint(comandas.bp)
    app.register_blueprint(caixa.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(cozinha.bp)
    app.register_blueprint(configuracoes.bp)
    
    # Inicializar configurações personalizadas
    Config.init_app(app)
    
    return app

# Importar modelos para que o Flask-Migrate os detecte
from .models import models 