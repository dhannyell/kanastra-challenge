from datetime import date, datetime

from dataclasses import dataclass
from pandas import DataFrame

from domain_layer.abstract.debit import DebitRepository


@dataclass
class Debit:
    name: str
    governmentId: str
    email: str
    debtAmount: float
    debtDueDate: date
    debtID: str
    inserted_at: datetime

    @classmethod
    def insert_debits(self, dataframe: DataFrame, using_repository: DebitRepository):
        return using_repository.insert_debits(dataframe)
