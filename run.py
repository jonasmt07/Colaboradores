# run.py
from app import create_app

# Cria a aplicação usando a fábrica
app = create_app()

if __name__ == '__main__':
    # Roda em modo debug apenas se executado diretamente
    app.run(debug=True)