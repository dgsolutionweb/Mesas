from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.models import db, ConfiguracaoSistema, Usuario
from werkzeug.utils import secure_filename
import os

bp = Blueprint('configuracoes', __name__)

def is_gerente():
    return current_user.cargo == 'Gerente'

@bp.route('/configuracoes')
@login_required
def ver_configuracoes():
    if not is_gerente():
        flash('Acesso negado. Apenas gerentes podem acessar as configurações.', 'error')
        return redirect(url_for('index'))
    
    config = ConfiguracaoSistema.query.first()
    if not config:
        config = ConfiguracaoSistema()
        db.session.add(config)
        db.session.commit()
    
    return render_template('configuracoes/configuracoes.html', config=config)

@bp.route('/configuracoes/salvar', methods=['POST'])
@login_required
def salvar_configuracoes():
    if not is_gerente():
        flash('Acesso negado. Apenas gerentes podem modificar as configurações.', 'error')
        return redirect(url_for('index'))
    
    config = ConfiguracaoSistema.query.first()
    if not config:
        config = ConfiguracaoSistema()
        db.session.add(config)
    
    config.nome_restaurante = request.form.get('nome_restaurante')
    config.endereco = request.form.get('endereco')
    config.telefone = request.form.get('telefone')
    config.mensagem_rodape = request.form.get('mensagem_rodape')
    config.impressora_cozinha = request.form.get('impressora_cozinha')
    config.impressora_bar = request.form.get('impressora_bar')
    config.imprimir_pedidos_cozinha = 'imprimir_pedidos_cozinha' in request.form
    config.imprimir_pedidos_bar = 'imprimir_pedidos_bar' in request.form
    config.categorias_cozinha = request.form.get('categorias_cozinha')
    config.categorias_bar = request.form.get('categorias_bar')
    
    # Tratamento do upload da logo
    if 'logo' in request.files:
        logo = request.files['logo']
        if logo.filename != '':
            filename = secure_filename(logo.filename)
            upload_path = os.path.join('app', 'static', 'uploads')
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            logo_path = os.path.join(upload_path, filename)
            logo.save(logo_path)
            config.logo_path = f'/static/uploads/{filename}'
    
    db.session.commit()
    flash('Configurações salvas com sucesso!', 'success')
    return redirect(url_for('configuracoes.ver_configuracoes')) 