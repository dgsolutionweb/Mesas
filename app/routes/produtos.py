from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models.models import db, Produto

bp = Blueprint('produtos', __name__)

@bp.route('/produtos')
@login_required
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('produtos/listar.html', produtos=produtos)

@bp.route('/produtos/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_produto():
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = float(request.form.get('preco'))
        categoria = request.form.get('categoria')
        
        novo_produto = Produto(
            nome=nome,
            descricao=descricao,
            preco=preco,
            categoria=categoria
        )
        
        db.session.add(novo_produto)
        db.session.commit()
        
        return redirect(url_for('produtos.listar_produtos'))
    return render_template('produtos/adicionar.html')

@bp.route('/produtos/<int:produto_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    
    if request.method == 'POST':
        produto.nome = request.form.get('nome')
        produto.descricao = request.form.get('descricao')
        produto.preco = float(request.form.get('preco'))
        produto.categoria = request.form.get('categoria')
        produto.disponivel = bool(request.form.get('disponivel'))
        
        db.session.commit()
        return redirect(url_for('produtos.listar_produtos'))
    
    return render_template('produtos/editar.html', produto=produto)

@bp.route('/produtos/<int:produto_id>/toggle_disponivel', methods=['POST'])
@login_required
def toggle_disponivel(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    produto.disponivel = not produto.disponivel
    db.session.commit()
    return redirect(url_for('produtos.listar_produtos')) 