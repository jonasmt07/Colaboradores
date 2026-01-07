# app/models.py
from typing import Dict, Any, Optional
from flask_login import UserMixin
from .extensions import db  # Importamos o db de extensions, evitando ciclo

class User(UserMixin, db.Model):
    """
    Modelo de Usuário para autenticação.
    Herda de UserMixin para fornecer implementações padrão 
    para o Flask-Login (is_authenticated, etc).
    """
    __tablename__ = 'users' # Boa prática: definir nome da tabela explicitamente

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(150), unique=True, nullable=False)
    password: str = db.Column(db.String(150), nullable=False)

    def __repr__(self) -> str:
        # Essencial para logs e debug: mostra o nome em vez do endereço de memória
        return f'<User {self.username}>'


class Employee(db.Model):
    """
    Modelo de Funcionário contendo dados corporativos.
    """
    __tablename__ = 'employees'

    id: int = db.Column(db.Integer, primary_key=True)
    nome: str = db.Column(db.String(100), nullable=False)
    cargo: Optional[str] = db.Column(db.String(100))
    unidade: Optional[str] = db.Column(db.String(50))       # Sigla (ex: CDT)
    nome_unidade: Optional[str] = db.Column(db.String(100)) # Extenso
    ramal: Optional[str] = db.Column(db.String(20))
    email: Optional[str] = db.Column(db.String(100))
    foto_url: Optional[str] = db.Column(db.String(500))

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializa o objeto para um dicionário Python (compatível com JSON).
        Útil para retornar dados em APIs REST para o front-end.
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'cargo': self.cargo,
            # Mantive 'Unidade' com maiúscula conforme seu código original,
            # mas o padrão JSON costuma ser tudo minúsculo (camelCase ou snake_case).
            'Unidade': self.unidade, 
            'nome_unidade': self.nome_unidade,
            'ramal': self.ramal,
            'email': self.email,
            # Convertendo snake_case (Python) para camelCase (Javascript)
            # para facilitar o uso no front-end.
            'fotoUrl': self.foto_url 
        }

    def __repr__(self) -> str:
        return f'<Employee {self.nome} - {self.unidade}>'