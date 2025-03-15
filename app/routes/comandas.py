from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from datetime import datetime, date
from app.models.models import db, Comanda, ItemComanda, Produto, Mesa, CaixaDiario, StatusPedido, TempoPreparoPadrao
from app.services.impressao import ServicoImpressao

bp = Blueprint('comandas', __name__)

@bp.route('/comandas')
@login_required
def listar_comandas():
    comandas = Comanda.query.filter_by(status='Aberta').all()
    return render_template('comandas/listar.html', comandas=comandas)

@bp.route('/comandas/<int:comanda_id>')
@login_required
def ver_comanda(comanda_id):
    comanda = Comanda.query.get_or_404(comanda_id)
    produtos = Produto.query.filter_by(disponivel=True).all()
    return render_template('comandas/ver.html', comanda=comanda, produtos=produtos)

@bp.route('/comandas/<int:comanda_id>/adicionar_item', methods=['POST'])
@login_required
def adicionar_item(comanda_id):
    comanda = Comanda.query.get_or_404(comanda_id)
    produto_id = request.form.get('produto_id')
    quantidade = int(request.form.get('quantidade', 1))
    observacao = request.form.get('observacao', '')
    
    produto = Produto.query.get_or_404(produto_id)
    
    item = ItemComanda(
        comanda_id=comanda_id,
        produto_id=produto_id,
        quantidade=quantidade,
        preco_unitario=produto.preco,
        observacao=observacao
    )
    
    comanda.valor_total += produto.preco * quantidade
    
    db.session.add(item)
    db.session.commit()
    
    # Criar status do pedido
    status = StatusPedido(
        item_comanda_id=item.id,
        status='Pendente'
    )
    
    # Se houver tempo padrão de preparo, usar
    tempo_padrao = TempoPreparoPadrao.query.filter_by(produto_id=produto_id).first()
    if tempo_padrao:
        status.tempo_estimado = tempo_padrao.tempo_padrao
    
    db.session.add(status)
    db.session.commit()
    
    # Tenta imprimir o pedido
    ServicoImpressao.imprimir_pedido(item)
    
    return redirect(url_for('comandas.ver_comanda', comanda_id=comanda_id))

@bp.route('/comandas/<int:comanda_id>/remover_item/<int:item_id>', methods=['POST'])
@login_required
def remover_item(comanda_id, item_id):
    item = ItemComanda.query.get_or_404(item_id)
    comanda = item.comanda
    
    comanda.valor_total -= item.preco_unitario * item.quantidade
    
    db.session.delete(item)
    db.session.commit()
    
    return redirect(url_for('comandas.ver_comanda', comanda_id=comanda_id))

@bp.route('/comandas/<int:comanda_id>/fechar', methods=['POST'])
@login_required
def fechar_comanda(comanda_id):
    comanda = Comanda.query.get_or_404(comanda_id)
    
    # Busca o caixa do dia ou cria um novo
    hoje = date.today()
    caixa = CaixaDiario.query.filter_by(data=hoje).first()
    if not caixa:
        caixa = CaixaDiario(data=hoje)
        db.session.add(caixa)
        db.session.commit()
    
    comanda.status = 'Fechada'
    comanda.data_fechamento = datetime.utcnow()
    comanda.mesa.status = 'Livre'
    comanda.caixa_id = caixa.id
    
    db.session.commit()
    
    return redirect(url_for('comandas.listar_comandas')) 