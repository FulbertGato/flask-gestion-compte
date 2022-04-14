import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///"+os.path.join(basedir,"db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
db = SQLAlchemy(app)

from models import Customer, Account, Transaction, TypeTransaction, Admin
db.create_all()

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.customer import customer_bp
from routes.google_auth import google_bp

# typeTransactionCredit=TypeTransaction.TypeTransaction(name="credit")
# typeTransactionDebit=TypeTransaction.TypeTransaction(name="debit")
# db.session.add(typeTransactionCredit)
# db.session.add(typeTransactionDebit)
# db.session.commit()
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):

    return render_template('500.html'), 500

if __name__ == '__main__':  
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(customer_bp, url_prefix='/customer')
    app.register_blueprint(google_bp, url_prefix='/google')
    app.run(debug=True)
