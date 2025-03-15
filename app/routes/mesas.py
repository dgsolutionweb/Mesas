from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.models import db, Mesa, Comanda

bp = Blueprint('mesas', __name__)

@bp.route('/mesas')
@login_required
def listar_mesas():
    mesas = Mesa.query.all()
    return render_template('mesas/listar.html', mesas=mesas)

@bp.route('/mesas/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_mesa():
    if request.method == 'POST':
        numero = request.form.get('numero')
        
        if Mesa.query.filter_by(numero=numero).first():
            flash('Número de mesa já existe')
            return redirect(url_for('mesas.adicionar_mesa'))
        
        nova_mesa = Mesa(numero=numero)
        db.session.add(nova_mesa)
        db.session.commit()
        
        return redirect(url_for('mesas.listar_mesas'))
    return render_template('mesas/adicionar.html')

@bp.route('/mesas/<int:mesa_id>/status', methods=['POST'])
@login_required
def alterar_status_mesa(mesa_id):
    mesa = Mesa.query.get_or_404(mesa_id)
    novo_status = request.form.get('status')
    
    if novo_status in ['Livre', 'Ocupada', 'Reservada']:
        mesa.status = novo_status
        db.session.commit()
    
    return redirect(url_for('mesas.listar_mesas'))

@bp.route('/mesas/<int:mesa_id>/abrir_comanda')
@login_required
def abrir_comanda(mesa_id):
    mesa = Mesa.query.get_or_404(mesa_id)
    
    if mesa.status != 'Livre':
        flash('Mesa não está livre')
        return redirect(url_for('mesas.listar_mesas'))
    
    nova_comanda = Comanda(
        mesa_id=mesa_id,
        usuario_id=current_user.id
    )
    mesa.status = 'Ocupada'
    
    db.session.add(nova_comanda)
    db.session.commit()
    
    return redirect(url_for('comandas.ver_comanda', comanda_id=nova_comanda.id)) 