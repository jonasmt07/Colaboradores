import csv
import os
from app import create_app
from app.extensions import db
from app.models import User, Employee

app = create_app()

def seed_database():
    arquivo_csv = 'colaboradores.csv'

    if not os.path.exists(arquivo_csv):
        print(f"❌ Erro: Arquivo '{arquivo_csv}' não encontrado.")
        print("   Rode o script de conversão primeiro ou crie o CSV.")
        return

    with app.app_context():
        print(f"--- Importando dados de {arquivo_csv} ---")

        # 1. Garante Admin
        if not User.query.filter_by(username='admin').first():
            db.session.add(User(username='admin', password='123'))
            print("✅ Usuário Admin criado.")

        novos = 0
        existentes = 0

        try:
            with open(arquivo_csv, newline='', encoding='utf-8') as csvfile:
                # O delimitador deve ser o mesmo usado na criação (ponto e vírgula)
                reader = csv.DictReader(csvfile, delimiter=';')
                
                for row in reader:
                    # Limpeza básica (remove espaços extras)
                    email = row['email'].strip()
                    nome = row['nome'].strip()
                    
                    if not email and not nome:
                        continue

                    # Verifica duplicidade
                    colaborador = Employee.query.filter_by(email=email).first()
                    if not colaborador:
                        colaborador = Employee.query.filter_by(nome=nome).first()

                    # Prepara dados (CSV -> Modelo)
                    dados = {
                        'nome': nome,
                        'email': email,
                        'ramal': row['ramal'].strip() if row['ramal'] else None,
                        'cargo': row['cargo'].strip(),
                        'unidade': row['Unidade'].strip(), # Atenção se no Excel a coluna é 'Unidade' ou 'unidade'
                        'nome_unidade': row['nome_unidade'].strip(),
                        'foto_url': row['fotoUrl'].strip() if row.get('fotoUrl') else None
                    }

                    if not colaborador:
                        db.session.add(Employee(**dados))
                        novos += 1
                    else:
                        # Atualiza dados
                        colaborador.cargo = dados['cargo']
                        colaborador.unidade = dados['unidade']
                        colaborador.nome_unidade = dados['nome_unidade']
                        colaborador.ramal = dados['ramal']
                        existentes += 1

            db.session.commit()
            print(f"✅ Importação Concluída!")
            print(f"🆕 Novos: {novos}")
            print(f"🔄 Atualizados: {existentes}")

        except KeyError as e:
            print(f"❌ Erro nas colunas do CSV: Coluna {e} não encontrada.")
            print("   Verifique se o cabeçalho do CSV está correto (nome;email;ramal;Unidade;nome_unidade;cargo;fotoUrl)")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")

if __name__ == '__main__':
    seed_database()