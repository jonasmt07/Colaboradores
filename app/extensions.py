# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inicializamos o SQLAlchemy sem passar o 'app' ainda.
# Isso permite que ele seja configurado depois, dentro da Factory (create_app).
db = SQLAlchemy()

# Inicializamos o LoginManager da mesma forma.
# Isso gerencia a sessão do usuário (login/logout).
login_manager = LoginManager()