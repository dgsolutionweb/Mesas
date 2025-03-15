from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models.models import Usuario, db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        user = Usuario.query.filter_by(email=email).first()
        if user and user.check_senha(senha):
            login_user(user)
            return redirect(url_for('mesas.listar_mesas'))
        flash('Email ou senha inválidos')
    
    return render_template('auth/login.html')

@bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        cargo = request.form.get('cargo')
        
        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado')
            return redirect(url_for('auth.registrar'))
        
        user = Usuario(nome=nome, email=email, cargo=cargo)
        user.set_senha(senha)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Usuário registrado com sucesso!')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/registrar.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 