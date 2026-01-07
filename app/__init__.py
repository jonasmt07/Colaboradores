# app/__init__.py
from flask import Flask
from .config import Config
from .extensions import db, login_manager

def create_app(config_class=Config):
    """
    Padrão Factory: Cria e configura uma instância da aplicação Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa as extensões com a app configurada
    db.init_app(app)
    login_manager.init_app(app)

    # Configuração do Login
    login_manager.login_view = 'auth.login' 
    login_manager.login_message_category = 'info'

    # Registro de Blueprints (As rotas do sistema)
    from app.blueprints.auth import auth_bp
    from app.blueprints.main import main_bp
    
    # --- ADICIONE ESTAS DUAS LINHAS AQUI EMBAIXO ---
    from app.blueprints.admin import admin_bp
    # -----------------------------------------------

    # Registra os prefixos de URL
    app.register_blueprint(auth_bp, url_prefix='/auth')  
    app.register_blueprint(main_bp)                      
    
    # --- E ESTA LINHA PARA ATIVAR O ADMIN ---
    app.register_blueprint(admin_bp, url_prefix='/admin')
    # ----------------------------------------

    # Cria o banco de dados se não existir
    with app.app_context():
        db.create_all()

    return app