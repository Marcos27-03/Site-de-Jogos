from flask import render_template,request,redirect,session,flash,url_for,send_from_directory
from classes import Jogos
from app import db,app
from helpers import recupera_imagem, deleta_arquivo,FormularioJogos
import time


@app.route('/')
def inicio():
    lista_jogos = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html',titulo='Jogos', jogos = lista_jogos)

@app.route('/novo')
def novojogo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Faça Login para adcionar um novo jogo.')
        return redirect(url_for('login', proxima=url_for('novojogo')))
    form = FormularioJogos()
    return render_template('novojogo.html', titulo = 'Novo Jogo', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioJogos(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novojogo'))
    
    nome=form.nome.data
    categoria=form.categoria.data
    console=form.console.data
    
    jogo=Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já cadastrado no site!')
        return redirect(url_for('inicio'))
     
    novojogo= Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novojogo)
    db.session.commit()
    
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novojogo.id}-{timestamp}.jpg')

    return redirect(url_for('inicio'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Faça Login para editar um novo jogo.')
        return redirect(url_for('login', proxima=url_for('editar',id=id)))
    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioJogos()
    
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo = 'Edicão de Jogo', jogo=jogo, capa_jogo=capa_jogo, form=form)
    

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioJogos(request.form)
    if form.validate_on_submit():
    
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        


        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data
        
        db.session.add(jogo)
        db.session.commit()
        
        if 'arquivo' in request.files and request.files['arquivo'].filename != '':
            arquivo = request.files['arquivo']
            upload_path = app.config['UPLOAD_PATH']
            timestamp = time.time()
            deleta_arquivo(jogo.id)
            arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('inicio'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Faça Login para excluir um novo jogo.')
        return redirect(url_for('login'))
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('jogo deletado com sucesso')

    return redirect(url_for('inicio'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

