from flask import render_template,request,redirect,session,flash,url_for
from classes import Usuarios
from app import app
from helpers import formLogin
from flask_bcrypt import check_password_hash


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = formLogin()
    return render_template('login.html', proxima = proxima, form=form)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = formLogin(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
        session['usuario_logado'] = usuario.nickname
        flash(f'{usuario.nickname} foi logado com sucesso!')
        prox_pagina = request.form['proxima']
        return redirect(prox_pagina)
    else:
        flash('Erro no nome do usuário ou senha, tente fazer login novamente ')
        return redirect(url_for('login'))

    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário Deslogado')
    return redirect(url_for('login'))