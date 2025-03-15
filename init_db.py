from app import create_app, db
from app.models.models import Usuario
from werkzeug.security import generate_password_hash

def init_db():
    app = create_app()
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Verificar se já existe um usuário gerente
        if not Usuario.query.filter_by(cargo='Gerente').first():
            # Criar usuário gerente padrão
            gerente = Usuario(
                nome='Gerente',
                email='gerente@email.com',
                senha_hash=generate_password_hash('123456'),
                cargo='Gerente'
            )
            db.session.add(gerente)
            db.session.commit()
            print('Usuário gerente criado com sucesso!')
            print('Email: gerente@email.com')
            print('Senha: 123456')
        else:
            print('Usuário gerente já existe!')

if __name__ == '__main__':
    init_db() 