#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Iniciando implantação do DGSoluções...${NC}"

# Criar diretórios necessários
echo "Criando diretórios..."
sudo mkdir -p /var/www/dgsolutions
sudo mkdir -p /var/log/dgsolutions
sudo mkdir -p /var/run/gunicorn

# Instalar dependências do sistema
echo "Instalando dependências do sistema..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev nginx postgresql postgresql-contrib

# Copiar arquivos do projeto
echo "Copiando arquivos do projeto..."
sudo cp -r . /var/www/dgsolutions/
cd /var/www/dgsolutions

# Configurar ambiente virtual
echo "Configurando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar banco de dados
echo "Configurando banco de dados..."
sudo -u postgres psql -c "CREATE DATABASE dg_solucoes;"
sudo -u postgres psql -c "CREATE USER dgsolutions WITH PASSWORD '@DG450159753';"
sudo -u postgres psql -c "ALTER ROLE dgsolutions SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE dgsolutions SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE dgsolutions SET timezone TO 'America/Sao_Paulo';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE dg_solucoes TO dgsolutions;"

# Configurar variáveis de ambiente
echo "Configurando variáveis de ambiente..."
echo "FLASK_APP=app
FLASK_ENV=production
DATABASE_URL=postgresql://dgsolutions:@DG450159753@localhost:5432/dg_solucoes
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(16))')" > .env

# Configurar Nginx
echo "Configurando Nginx..."
sudo cp nginx_dgsolutions.conf /etc/nginx/sites-available/dgsolutions
sudo ln -s /etc/nginx/sites-available/dgsolutions /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# Configurar Gunicorn como serviço
echo "Configurando Gunicorn como serviço..."
echo "[Unit]
Description=DGSoluções Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/dgsolutions
Environment="PATH=/var/www/dgsolutions/venv/bin"
ExecStart=/var/www/dgsolutions/venv/bin/gunicorn --config gunicorn_config.py 'app:create_app()'

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/dgsolutions.service

# Iniciar serviços
echo "Iniciando serviços..."
sudo systemctl daemon-reload
sudo systemctl start dgsolutions
sudo systemctl enable dgsolutions

# Configurar permissões
echo "Configurando permissões..."
sudo chown -R www-data:www-data /var/www/dgsolutions
sudo chown -R www-data:www-data /var/log/dgsolutions
sudo chown -R www-data:www-data /var/run/gunicorn

echo -e "${GREEN}Implantação concluída!${NC}"
echo -e "Você pode acessar o sistema em: http://seu_dominio.com"
echo -e "Verifique os logs em: /var/log/dgsolutions/error.log" 