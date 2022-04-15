from app import db
from datetime import date


class TypeTransaction(db.Model):
    __tablename__ = 'type_transaction'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    transaction=db.relationship('Transaction', back_populates="type_transaction",cascade="all, delete",passive_deletes=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, name):
        self.name = name
        self.created_at = date.today()
        self.updated_at = date.today()

    def __repr__(self):
        return '<TypeTransaction %r>' % self.name

def get_all_type_transaction():
    return TypeTransaction.query.all()


def get_type_transaction_by_id(id):
    return TypeTransaction.query.filter_by(id=id).first()


def add_type_transaction(name):
    type_transaction = TypeTransaction(name)
    db.session.add(type_transaction)
    db.session.commit()
    return type_transaction


def update_type_transaction(id, name):
    type_transaction = get_type_transaction_by_id(id)
    if type_transaction:
        type_transaction.name = name
        type_transaction.updated_at = date.today()
        db.session.commit()
        return True
    return False


def remove_type_transaction(id):
    type_transaction = get_type_transaction_by_id(id)
    if type_transaction:
        db.session.delete(type_transaction)
        db.session.commit()
        return True
    return False


def get_type_transaction_by_name(name):
    return TypeTransaction.query.filter_by(name=name).first()
    