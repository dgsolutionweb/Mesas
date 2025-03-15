from flask_migrate import upgrade, migrate, init, stamp
from app import create_app, db

def init_migrations():
    """Inicializa o sistema de migrações"""
    app = create_app()
    with app.app_context():
        # Inicializar migrações
        init()
        # Criar primeira migração
        migrate()
        # Aplicar migrações
        upgrade()
        # Marcar como atual
        stamp()

if __name__ == '__main__':
    init_migrations() 