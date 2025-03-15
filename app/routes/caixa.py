from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from datetime import datetime, date
from app.models.models import db, CaixaDiario, Comanda

bp = Blueprint('caixa', __name__)

@bp.route('/caixa')
@login_required
def ver_caixa():
    hoje = date.today()
    caixa = CaixaDiario.query.filter_by(data=hoje).first()
    
    if not caixa:
        caixa = CaixaDiario(data=hoje)
        db.session.add(caixa)
        db.session.commit()
    
    comandas_fechadas = Comanda.query.filter_by(
        status='Fechada',
        caixa_id=caixa.id
    ).all()
    
    return render_template('caixa/ver.html', caixa=caixa, comandas=comandas_fechadas)

@bp.route('/caixa/historico')
@login_required
def historico_caixa():
    caixas = CaixaDiario.query.order_by(CaixaDiario.data.desc()).all()
    return render_template('caixa/historico.html', caixas=caixas)

@bp.route('/caixa/fechar', methods=['POST'])
@login_required
def fechar_caixa():
    hoje = date.today()
    caixa = CaixaDiario.query.filter_by(data=hoje).first()
    
    if not caixa:
        flash('Não há caixa aberto para hoje')
        return redirect(url_for('caixa.ver_caixa'))
    
    if caixa.status == 'Fechado':
        flash('Caixa já está fechado')
        return redirect(url_for('caixa.ver_caixa'))
    
    # Calcula o total do dia
    comandas_fechadas = Comanda.query.filter_by(
        status='Fechada',
        caixa_id=caixa.id
    ).all()
    
    total = sum(comanda.valor_total for comanda in comandas_fechadas)
    
    caixa.valor_total = total
    caixa.status = 'Fechado'
    db.session.commit()
    
    return redirect(url_for('caixa.ver_caixa')) 