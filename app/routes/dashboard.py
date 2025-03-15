from flask import Blueprint, render_template, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from app.models.models import db, ItemComanda, Produto, Usuario, Comanda, CaixaDiario
import plotly.graph_objs as go
import json

bp = Blueprint('dashboard', __name__)

def is_gerente():
    return current_user.is_authenticated and current_user.cargo == 'Gerente'

@bp.route('/dashboard')
@login_required
def dashboard():
    if not is_gerente():
        flash('Acesso negado. Apenas gerentes podem acessar o dashboard.', 'error')
        return redirect(url_for('index'))
    
    # Dados para os gráficos
    hoje = datetime.now().date()
    inicio_mes = hoje.replace(day=1)
    
    # Vendas por dia
    vendas_diarias = db.session.query(
        func.date(Comanda.data_fechamento).label('data'),
        func.sum(Comanda.valor_total).label('total')
    ).filter(
        Comanda.status == 'Fechada',
        Comanda.data_fechamento >= inicio_mes
    ).group_by(
        func.date(Comanda.data_fechamento)
    ).all()
    
    # Produtos mais vendidos
    produtos_vendidos = db.session.query(
        Produto.nome,
        func.sum(ItemComanda.quantidade).label('quantidade')
    ).join(
        ItemComanda, ItemComanda.produto_id == Produto.id
    ).group_by(
        Produto.id, Produto.nome
    ).order_by(
        func.sum(ItemComanda.quantidade).desc()
    ).limit(10).all()
    
    # Desempenho dos garçons
    desempenho_garcons = db.session.query(
        Usuario.nome,
        func.count(Comanda.id).label('comandas'),
        func.sum(Comanda.valor_total).label('total')
    ).select_from(Usuario).join(
        Comanda, Comanda.usuario_id == Usuario.id
    ).filter(
        Usuario.cargo == 'Garçom',
        Comanda.status == 'Fechada',
        Comanda.data_fechamento >= inicio_mes
    ).group_by(
        Usuario.id, Usuario.nome
    ).all()
    
    # Horários de pico
    horarios_pico = db.session.query(
        extract('hour', ItemComanda.data_criacao).label('hora'),
        func.count(ItemComanda.id).label('pedidos')
    ).filter(
        ItemComanda.data_criacao >= inicio_mes
    ).group_by(
        extract('hour', ItemComanda.data_criacao)
    ).all()
    
    # Criar gráficos com Plotly
    vendas_graph = {
        'data': [{
            'x': [v.data.strftime('%d/%m') for v in vendas_diarias],
            'y': [float(v.total) for v in vendas_diarias],
            'type': 'bar',
            'name': 'Vendas Diárias'
        }],
        'layout': {
            'title': 'Vendas Diárias do Mês',
            'xaxis': {'title': 'Data'},
            'yaxis': {'title': 'Valor Total (R$)'}
        }
    }
    
    produtos_graph = {
        'data': [{
            'labels': [p.nome for p in produtos_vendidos],
            'values': [p.quantidade for p in produtos_vendidos],
            'type': 'pie',
            'name': 'Produtos Mais Vendidos'
        }],
        'layout': {
            'title': 'Top 10 Produtos Mais Vendidos'
        }
    }
    
    garcons_graph = {
        'data': [{
            'x': [g.nome for g in desempenho_garcons],
            'y': [float(g.total) if g.total else 0 for g in desempenho_garcons],
            'type': 'bar',
            'name': 'Vendas por Garçom'
        }],
        'layout': {
            'title': 'Desempenho dos Garçons',
            'xaxis': {'title': 'Garçom'},
            'yaxis': {'title': 'Valor Total (R$)'}
        }
    }
    
    horarios_graph = {
        'data': [{
            'x': [f'{h.hora}:00' for h in horarios_pico],
            'y': [h.pedidos for h in horarios_pico],
            'type': 'scatter',
            'mode': 'lines+markers',
            'name': 'Pedidos por Hora'
        }],
        'layout': {
            'title': 'Horários de Pico',
            'xaxis': {'title': 'Hora'},
            'yaxis': {'title': 'Quantidade de Pedidos'}
        }
    }
    
    graphs = {
        'vendas': json.dumps(vendas_graph),
        'produtos': json.dumps(produtos_graph),
        'garcons': json.dumps(garcons_graph),
        'horarios': json.dumps(horarios_graph)
    }
    
    return render_template('dashboard/dashboard.html', graphs=graphs) 