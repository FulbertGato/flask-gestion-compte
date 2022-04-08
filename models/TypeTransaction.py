from app import db



class TypeTransaction(db.Model):
    __tablename__ = 'type_transaction'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    transaction=db.relationship('Transaction', back_populates="type_transaction",cascade="all, delete",
        passive_deletes=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, name, created_at, updated_at):
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<TypeTransaction %r>' % self.name
    