from app import create_app, db
from app.models.models import Usuario

def recreate_database():
    # Cria a aplicação
    app = create_app()
    
    # Entra no contexto da aplicação
    with app.app_context():
        # Recria todas as tabelas
        db.drop_all()
        db.create_all()
        
        # Cria um usuário gerente padrão
        gerente = Usuario(
            nome='Gerente',
            email='gerente@email.com',
            cargo='Gerente'
        )
        gerente.set_senha('123456')
        
        # Adiciona e salva no banco
        db.session.add(gerente)
        db.session.commit()
        
        print('Banco de dados recriado com sucesso!')
        print('Usuário gerente criado:')
        print('Email: gerente@email.com')
        print('Senha: 123456')

if __name__ == '__main__':
    recreate_database() 