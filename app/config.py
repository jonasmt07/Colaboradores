# app/config.py
import os

# Define o diretório base do projeto para localizar o banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configurações base da aplicação.
    Usa variáveis de ambiente para segurança (ex: SECRET_KEY), 
    mas fornece um padrão para desenvolvimento local.
    """
    # Segurança: Chave usada para assinar cookies de sessão
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-muito-dificil-dev-key'

    # Banco de Dados: SQLite por padrão, mas pronto para PostgreSQL/MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'instance', 'database.db')
    
    # Performance: Desativa o rastreamento de modificações do SQLAlchemy (consome muita memória)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- NOVO: Configuração de Upload ---
    # Caminho absoluto para app/static/img/fotos
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'img', 'fotos')
    # Limite de 2MB por arquivo (opcional, mas recomendado)
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024 
    # Extensões permitidas
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}