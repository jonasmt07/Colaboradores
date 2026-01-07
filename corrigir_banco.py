from app import create_app
from app.extensions import db
from app.models import Employee

app = create_app()

def limpar_dados():
    with app.app_context():
        print("🧹 Iniciando limpeza do banco de dados...")
        
        funcionarios = Employee.query.all()
        alterados = 0
        
        for f in funcionarios:
            mudou = False
            
            # Limpa UNIDADE (Sigla)
            if f.unidade:
                nova_unidade = f.unidade.strip().upper() # Tira espaço e põe Maiúsculo
                if f.unidade != nova_unidade:
                    f.unidade = nova_unidade
                    mudou = True

            # Limpa NOME DA UNIDADE (Extenso)
            if f.nome_unidade:
                novo_nome_unidade = f.nome_unidade.strip()
                if f.nome_unidade != novo_nome_unidade:
                    f.nome_unidade = novo_nome_unidade
                    mudou = True

            if mudou:
                alterados += 1

        db.session.commit()
        print(f"✅ Pronto! {alterados} registros foram corrigidos/limpos.")
        print("🚀 Agora as siglas estão sem espaços e em maiúsculo (ex: 'CTI').")

if __name__ == '__main__':
    limpar_dados()