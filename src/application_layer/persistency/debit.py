import sqlalchemy as db

metadata = db.MetaData()

debit_table = db.Table(
    "debits",
    metadata,
    db.Column("id", db.Integer, nullable=False),
    db.Column("name", db.String(100), nullable=False),
    db.Column("governmentId", db.Integer, nullable=False),
    db.Column("email", db.String(100), nullable=False),
    db.Column("debtAmount", db.Float, nullable=False),
    db.Column("debtDueDate", db.Date, nullable=False),
    db.Column("debtId", db.UUID, primary_key=True, nullable=False),
)
