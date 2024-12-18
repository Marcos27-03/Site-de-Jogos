from flask import Flask
from ext import db
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_pyfile('configs.py')

db.init_app(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

from rotas_jogos import *
from rotas_usuario import *

if __name__=='__main__':
    app.run(debug=True)
