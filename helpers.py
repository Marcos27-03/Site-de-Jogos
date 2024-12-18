import os
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,validators, PasswordField

class formLogin(FlaskForm):
    nickname = StringField('Nickname', [validators.data_required(), validators.length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.data_required(), validators.length(min=1, max=100)])
    login = SubmitField('Login')

class FormularioJogos(FlaskForm):
    nome = StringField('nome do jogo', [validators.data_required(), validators.length(min=1, max=50)])
    categoria = StringField('categoria', [validators.data_required(), validators.length(min=1, max=40)])
    console = StringField('console', [validators.data_required(), validators.length(min=1, max=20)])
    salvar = SubmitField('salvar')
    
def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
    return 'capa_padrao.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo)) 