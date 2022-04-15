from app import db
from datetime import date
from lib.service.service import decrypt_password, encrypt_password
from routes.admin import distributeur_add

class Distributeur(db.Model):
    __tablename__ = 'distributeur'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    vouchers = db.relationship('Voucher', back_populates="distributeur",cascade="all, delete", passive_deletes=True)
    date_creation = db.Column(db.Date, nullable=False)
    date_modification = db.Column(db.Date, nullable=False)

    def __init__(self, nom, prenom, email, password):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.password = encrypt_password(password)
        self.status = 'active'
        self.date_creation = date.today()
        self.date_modification = date.today()

    def __repr__(self):
        return '<Distributeur %r>' % self.nom

    def serialize(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'email': self.email,
            'date_creation': self.date_creation,
            'date_modification': self.date_modification,     
            'status': self.status,
            'role': 'distributeur'
        }


def query_by_email(email):
    return Distributeur.query.filter_by(email=email).first()

def password_is_correct(post_encrypted_password,post_password):
    password=decrypt_password(post_encrypted_password)
    return password == post_password

def add_distributeur(distributeur):
    distributeur.password = encrypt_password("DISTRIBUTEUR")
    db.session.add(distributeur)
    db.session.commit()


def all_distributeurs():
    distributeurs= Distributeur.query.all()
    distributeurs_serialized = [distributeur.serialize() for distributeur in distributeurs]
    return distributeurs_serialized

def query_by_id(id):
    return Distributeur.query.filter_by(id=id).first()


def delete_distributeur(id):
    distributeur = query_by_id(id)
    db.session.delete(distributeur)
    db.session.commit()


def update_distributeur(id, nom, prenom, email):
    distributeur = query_by_id(id)
    distributeur.nom = nom
    distributeur.prenom = prenom
    distributeur.email = email
    distributeur.date_modification = date.today()
    db.session.commit()

def update_distributeur_status(id, status):
    distributeur = query_by_id(id)
    distributeur.status = status
    distributeur.date_modification = date.today()
    db.session.commit()

def update_distributeur_password(id, password):
    distributeur = query_by_id(id)
    distributeur.password = encrypt_password(password)
    distributeur.date_modification = date.today()
    db.session.commit()