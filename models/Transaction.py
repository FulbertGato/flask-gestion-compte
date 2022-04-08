from app import db


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    type_transaction_id = db.Column(db.Integer, db.ForeignKey('type_transaction.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    type_transaction = db.relationship('TypeTransaction', back_populates="transaction")
    account_id = db.Column(db.Integer, db.ForeignKey('account.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    account = db.relationship('Account', back_populates="transactions")
    amount = db.Column(db.Float, nullable=False)
    status=db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, type_transaction_id, amount, status, created_at, updated_at):
        self.type_transaction_id = type_transaction_id
        self.amount = amount
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at