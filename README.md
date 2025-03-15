# Sistema de Gerenciamento de Restaurante

Um sistema web completo para gerenciamento de restaurante, desenvolvido com Flask e SQLAlchemy.

## Funcionalidades

- Gerenciamento de mesas
- Controle de comandas
- Cadastro de produtos
- Controle de caixa
- Sistema de autenticação de usuários

## Tecnologias Utilizadas

- Python 3.8+
- Flask
- SQLAlchemy
- Flask-Login
- Bootstrap 5
- Font Awesome

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/sistema-restaurante.git
cd sistema-restaurante
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```
SECRET_KEY=sua-chave-secreta
DATABASE_URL=sqlite:///restaurante.db
```

5. Inicialize o banco de dados:
```bash
flask db upgrade
```

6. Execute o servidor:
```bash
python run.py
```

## Uso

1. Acesse http://localhost:5000 no seu navegador
2. Crie uma conta de usuário
3. Faça login no sistema
4. Comece a usar as funcionalidades

## Estrutura do Projeto

```
sistema-restaurante/
├── app/
│   ├── models/
│   │   └── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── mesas.py
│   │   ├── comandas.py
│   │   ├── produtos.py
│   │   └── caixa.py
│   ├── templates/
│   │   ├── auth/
│   │   ├── mesas/
│   │   ├── comandas/
│   │   ├── produtos/
│   │   └── caixa/
│   ├── static/
│   └── __init__.py
├── config.py
├── run.py
└── requirements.txt
```

## Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes. 