import os

SECRET_KEY = 'markin'

SQLALCHEMY_DATABASE_URI='{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(    
    SGBD = 'mysql+mysqlconnector',
    usuario = 'root',
    senha='marc0305',
    servidor = 'localhost',
    database = 'jogoteca'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'


SQLALCHEMY_TRACK_MODIFICATIONS = False