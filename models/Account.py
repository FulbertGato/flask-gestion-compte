#from flask_sqlalchemy import SQLAlchemy
import datetime
from app import db


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(150), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    secret = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    customer = db.relationship('Customer', back_populates="accounts")
    transactions = db.relationship('Transaction', back_populates="account",cascade="all, delete", passive_deletes=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self,account_number,  balance, secret, customer_id):
        self.account_number = account_number
        self.balance = balance
        self.secret = secret
        self.customer_id = customer_id
        self.created_at = datetime.datetime.now()
        self.updated_at =   datetime.datetime.now()
    
    def __repr__(self):
        return '<Account %r>' % self.account_number

    def serialize(self):
        return {
            'id': self.id,
            'account_number': self.account_number,
            'balance': self.balance,
            'secret': self.secret,
            'customer_id': self.customer_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

def add_account(account):
    db.session.add(account)
    db.session.commit()