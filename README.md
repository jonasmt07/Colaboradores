# Sistema de Gestão de Colaboradores (RH)

Sistema web desenvolvido em Python/Flask para gerenciamento de colaboradores, unidades e ramais. O projeto segue a arquitetura **Application Factory** com **Blueprints** para modularidade e escalabilidade.

## 🚀 Tecnologias Utilizadas

* **Backend:** Python 3.12+, Flask, SQLAlchemy, Flask-Login.
* **Frontend:** HTML5, Tailwind CSS (CDN), Jinja2 Templates.
* **Banco de Dados:** SQLite (Desenvolvimento).
* **Arquitetura:** MVC com Blueprints e Factory Pattern.

## 📂 Estrutura do Projeto

O projeto foi refatorado para seguir as melhores práticas de desenvolvimento web:

```text
/meu_projeto
├── /app
│   ├── /blueprints      # Módulos de Rotas (Admin, Auth, Main)
│   ├── /static          # CSS, JS e Imagens
│   ├── /templates       # Arquivos HTML organizados por módulo
│   ├── models.py        # Modelos do Banco de Dados
│   ├── extensions.py    # Extensões (DB, LoginManager)
│   └── __init__.py      # Fábrica da Aplicação (create_app)
├── /instance            # Banco de dados local (ignorado no git)
├── run.py               # Ponto de entrada da aplicação
└── requirements.txt     # Dependências do projeto

⚙️ Como Executar o Projeto
Pré-requisitos
Python 3 instalado.



Clone o repositório ou baixe o código.

Crie e ative um ambiente virtual:

Bash

# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Instale as dependências:

Bash

pip install -r requirements.txt
(Se não tiver o arquivo requirements.txt ainda, instale: pip install flask flask-sqlalchemy flask-login)

Execute a aplicação:

Bash

python run.py