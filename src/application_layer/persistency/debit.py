from src.server import db

debit_table = db.Table(
    'debit',
    db.metadata,
    db.Column('name', db.String(100), nullable=False),
    db.Column('governmentId', db.Integer, nullable=False),
    db.Column('email', db.String(100), nullable=False),
    db.Column('debtAmount', db.Float, nullable=False),
    db.Column('debtDueDate', db.Date, nullable=False),
    db.Column('debtID', db.UUID, primary_key=True, nullable=False),
    db.Column('inserted_at', db.DateTime, nullable=False)
)