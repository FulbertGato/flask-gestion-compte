#from flask_sqlalchemy import SQLAlchemy
import datetime

from app import db
from models import Customer

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(150), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    secret = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    customer = db.relationship('Customer', back_populates="accounts")
    transactions = db.relationship('Transaction', back_populates="account",cascade="all, delete", passive_deletes=True)
    vouchers = db.relationship('Voucher', back_populates="account",cascade="all, delete", passive_deletes=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, account_number, balance, secret, customer_id):
        self.account_number = account_number
        self.balance = balance
        self.secret = secret
        self.customer_id = customer_id
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

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
            'updated_at': self.updated_at,
            'transactions': self.transactions.serialize(),
            #list of vouchers
            'vouchers': [voucher.serialize() for voucher in self.vouchers]
            
        }

    

def add_account(account):
    db.session.add(account)
    db.session.commit()


def get_account(account_number):
    return Account.query.filter_by(account_number=account_number).first()


def get_accounts():
    return Account.query.all()


def update_account(account_number, account):
    account_to_update = get_account(account_number)
    account_to_update.account_number = account.account_number
    account_to_update.balance = account.balance
    account_to_update.secret = account.secret
    account_to_update.customer_id = account.customer_id
    account_to_update.updated_at = datetime.datetime.now()
    db.session.commit()


def delete_account(account_number):
    account_to_delete = get_account(account_number)
    db.session.delete(account_to_delete)
    db.session.commit()


def get_account_by_customer_id(customer_id):
    return Account.query.filter_by(customer_id=customer_id).all()


def get_acount_by_customer_phone_and_secret(phone, secret):
    return Account.query.filter_by(customer_id=Customer.get_customer_by_phone(phone).id, secret=secret).first()
    
