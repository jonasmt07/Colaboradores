from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.extensions import db, login_manager
from app.models import User
from . import auth_bp

# Configuração necessária para o Flask-Login saber como achar o usuário pelo ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # TODO: No futuro, usar hash de senha (ex: werkzeug.security.check_password_hash)
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            login_user(user)
            # Atenção: 'admin.index' refere-se ao blueprint 'admin', função 'index'
            return redirect(url_for('admin.index'))
        else:
            flash('Login inválido!')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    # 'main.home' refere-se ao blueprint 'main', função 'home'
    return render_template('auth/login.html')