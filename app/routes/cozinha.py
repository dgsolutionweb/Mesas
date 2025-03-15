from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app.models.models import db, ItemComanda, StatusPedido, Produto, ConfiguracaoSistema

bp = Blueprint('cozinha', __name__)

@bp.route('/cozinha')
@login_required
def cozinha():
    config = ConfiguracaoSistema.query.first()
    categorias_cozinha = config.categorias_cozinha.split(',') if config else []
    
    # Buscar pedidos pendentes e em preparo
    pedidos = db.session.query(ItemComanda, StatusPedido)\
        .join(StatusPedido)\
        .join(Produto)\
        .filter(
            Produto.categoria.in_(categorias_cozinha),
            StatusPedido.status.in_(['Pendente', 'Em Preparo'])
        )\
        .order_by(StatusPedido.status.desc(), ItemComanda.id.asc())\
        .all()
    
    return render_template('cozinha/cozinha.html', pedidos=pedidos)

@bp.route('/cozinha/atualizar_status/<int:pedido_id>', methods=['POST'])
@login_required
def atualizar_status(pedido_id):
    status = request.form.get('status')
    pedido = StatusPedido.query.get_or_404(pedido_id)
    
    if status == 'Em Preparo' and pedido.status == 'Pendente':
        pedido.status = 'Em Preparo'
        pedido.inicio_preparo = datetime.now()
    elif status == 'Pronto' and pedido.status == 'Em Preparo':
        pedido.status = 'Pronto'
        pedido.fim_preparo = datetime.now()
    elif status == 'Entregue' and pedido.status == 'Pronto':
        pedido.status = 'Entregue'
    
    db.session.commit()
    return redirect(url_for('cozinha.cozinha'))

@bp.route('/cozinha/atualizar_tempo/<int:pedido_id>', methods=['POST'])
@login_required
def atualizar_tempo(pedido_id):
    tempo = request.form.get('tempo', type=int)
    pedido = StatusPedido.query.get_or_404(pedido_id)
    pedido.tempo_estimado = tempo
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/cozinha/adicionar_observacao/<int:pedido_id>', methods=['POST'])
@login_required
def adicionar_observacao(pedido_id):
    observacao = request.form.get('observacao')
    pedido = StatusPedido.query.get_or_404(pedido_id)
    pedido.observacoes_cozinha = observacao
    db.session.commit()
    return jsonify({'success': True}) 