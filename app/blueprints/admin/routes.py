import os
from flask import render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from flask_login import login_required
from app.extensions import db
from app.models import Employee
from . import admin_bp

# Função auxiliar para verificar extensão
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Função auxiliar para salvar a imagem
def save_picture(form_picture):
    # Gera um nome seguro (remove caracteres perigosos)
    filename = secure_filename(form_picture.filename)
    
    # Define o caminho completo
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    # Salva o arquivo na pasta
    form_picture.save(picture_path)
    
    return filename

@admin_bp.route('/')
@login_required
def index():
    employees = Employee.query.all()
    units_query = db.session.query(Employee.unidade).distinct().order_by(Employee.unidade).all()
    all_units = [u[0] for u in units_query if u[0]]
    return render_template('admin/dashboard.html', employees=employees, all_units=all_units)

@admin_bp.route('/add', methods=['POST'])
@login_required
def add_employee():
    # Lógica de Upload
    foto_nome = None
    if 'foto' in request.files:
        file = request.files['foto']
        if file and file.filename != '' and allowed_file(file.filename):
            foto_nome = save_picture(file)

    new_employee = Employee(
        nome=request.form.get('nome'),
        cargo=request.form.get('cargo'),
        unidade=request.form.get('unidade'),
        nome_unidade=request.form.get('nome_unidade'),
        ramal=request.form.get('ramal'),
        email=request.form.get('email'),
        foto_url=foto_nome # Salva o nome do arquivo no banco
    )
    db.session.add(new_employee)
    db.session.commit()
    flash('Colaborador adicionado com sucesso!')
    return redirect(url_for('admin.index'))

@admin_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    
    employee.nome = request.form.get('nome')
    employee.cargo = request.form.get('cargo')
    employee.unidade = request.form.get('unidade')
    employee.nome_unidade = request.form.get('nome_unidade')
    employee.ramal = request.form.get('ramal')
    employee.email = request.form.get('email')
    
    # Verifica se enviou uma NOVA foto
    if 'foto' in request.files:
        file = request.files['foto']
        if file and file.filename != '' and allowed_file(file.filename):
            # Salva a nova e atualiza o banco
            foto_nome = save_picture(file)
            employee.foto_url = foto_nome
            # Opcional: Aqui você poderia deletar a foto antiga do disco para economizar espaço
    
    # Se não enviou foto nova, mantém a antiga (não faz nada com foto_url)

    db.session.commit()
    flash('Atualizado com sucesso!')
    return redirect(url_for('admin.index'))

@admin_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Removido com sucesso.')
    return redirect(url_for('admin.index'))