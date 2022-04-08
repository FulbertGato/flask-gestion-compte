import os
import pymysql
SECRET_KEY = os.urandom(32)
# Indique le dossier dans lequel scripts s’exécute
basedir = os.path.abspath(os.path.dirname(__file__))
# Activer le mode debug
DEBUG = True
SESSION_TYPE = 'redis'
# Connexion à la base de données
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/python_flask_devoir'

# désactiver le système d’évènement/warning de Flask-SQLAlchemy 
#SQLALCHEMY_TRACK_MODIFICATIONS = False