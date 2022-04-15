from app import db
from datetime import date

class Voucher(db.Model):
    __tablename__ = 'voucher'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), nullable=False, unique=True)
    date_creation = db.Column(db.Date, nullable=False)
    date_modification = db.Column(db.Date, nullable=False)
    distributeur_id = db.Column(db.Integer, db.ForeignKey('distributeur.id'), nullable=False)
    distributeur = db.relationship('Distributeur', back_populates="vouchers",cascade="all, delete", passive_deletes=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account', back_populates="vouchers",cascade="all, delete", passive_deletes=True)
    is_used = db.Column(db.Boolean, nullable=False)
    date_used = db.Column(db.Date, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    status=db.Column(db.String(255), nullable=False)


    def __init__(self, code, distributeur_id, account_id, amount):
        self.code = code
        self.date_creation = date.today()
        self.date_modification = date.today()
        self.distributeur_id = distributeur_id
        self.account_id = account_id
        self.is_used = False
        self.amount = amount
        self.status = 'active'
        
    

    def __repr__(self):
        return '<Voucher %r>' % self.code




def add_voucher(voucher):
    db.session.add(voucher)
    db.session.commit()


def query_by_distributeur_id(id):
    return Voucher.query.filter_by(distributeur_id=id).all()
    
def update_voucher_status(id, status):
    voucher = Voucher.query_by_id(id)
    if voucher:
        voucher.status = status
        db.session.commit()
        return True
    return False


def query_by_id(id):
    return Voucher.query.filter_by(id=id).first()

def voucher_by_code(code):
    return Voucher.query.filter_by(code=code).first()

def update_voucher(voucher):
    voucher.date_modification = date.today()
    voucher.is_used = True
    voucher.date_used = date.today()
    db.session.commit()
    return voucher

