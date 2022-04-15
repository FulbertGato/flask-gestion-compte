#from flask_sqlalchemy import SQLAlchemy
from datetime import date
from app import db


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status=db.Column(db.String(50), nullable=False)
    accounts = db.relationship('Account', back_populates="customer",cascade="all, delete",uselist=False, passive_deletes=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    admin = db.relationship('Admin', back_populates="customers")
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

    
    def __init__(self, firstname, lastname, email, phone, password, admin_id):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.password = password
        self.status = 'active'
        self.admin_id = admin_id
        self.created_at = date.today()
        self.updated_at = date.today()
    
    def __repr__(self):
        return '<Customer %r>' % self.firstname
    
    def serialize(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'phone': self.phone,
            'status': self.status,
            'admin_id': self.admin_id,
            'role': 'customer'
        }
    
def query_by_email(email):
    return Customer.query.filter_by(email=email).first()

def query_by_id(id):
    return Customer.query.filter_by(id=id).first()

def add_customer(customer):
    db.session.add(customer)
    db.session.commit()

def get_customer_by_phone(phone):
    return Customer.query.filter_by(phone=phone).first()
    

def update_customer(customer):
    customer_to_update = query_by_id(customer.id)
    customer_to_update.firstname = customer.firstname
    customer_to_update.lastname = customer.lastname
    customer_to_update.email = customer.email
    customer_to_update.phone = customer.phone
    customer_to_update.updated_at = date.today()
    db.session.commit()


def status_update(customer):
    customer_to_update = query_by_id(customer.id)
    customer_to_update.status = customer.status
    customer_to_update.updated_at = date.today()
    db.session.commit()

def all_customers():
    customers = Customer.query.all()
    #customers_serialized = [customer.serialize() for customer in customers]
    return customers



def remove_customer(customer):
    db.session.delete(customer.accounts)
    db.session.delete(customer)
    db.session.commit()

