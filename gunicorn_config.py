import multiprocessing

# Configurações do servidor
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Configurações de logging
accesslog = "/var/log/dgsolutions/access.log"
errorlog = "/var/log/dgsolutions/error.log"
loglevel = "info"

# Configurações do processo
daemon = False
pidfile = "/var/run/gunicorn/dgsolutions.pid"
user = "www-data"
group = "www-data"

# Configurações do ambiente
raw_env = [
    "FLASK_APP=app",
    "FLASK_ENV=production"
]

# Configurações de segurança
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190 