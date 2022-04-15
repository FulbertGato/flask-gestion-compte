from app import db
from datetime import date
from lib.service.service import decrypt_password, encrypt_password

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    customers = db.relationship('Customer', back_populates='admin', cascade="all, delete",passive_deletes=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.created_at = date.today()
        self.updated_at = date.today()

    def __repr__(self):
        return '<Admin %r>' % self.username

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': 'admin',
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


def all_admins():
    admins= Admin.query.all()
    admins_serialized = [admin.serialize() for admin in admins]
    
    return admins_serialized

def query_by_email(email):
    return Admin.query.filter_by(email=email).first()

def get_admin_by_id(id):
    return Admin.query.filter_by(id=id).first()

def add_admin(admin):
    admin.password = encrypt_password(admin.password)
    db.session.add(admin)
    db.session.commit()

def update_admin(admin,post_username,post_email):
    admin.username = post_username
    admin.email = post_email
    admin.updated_at = date.today()
    db.session.commit() 


def remove_admin(admin):
    db.session.delete(admin)
    db.session.commit()

    
def password_is_correct(post_encrypted_password,post_password):
    password=decrypt_password(post_encrypted_password)
    return password == post_password