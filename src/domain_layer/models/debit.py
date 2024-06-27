from datetime import date

from dataclasses import dataclass
from pandas import DataFrame

from domain_layer.abstract.debit import Debit as DebitRepository


@dataclass
class Debit:
    name: str
    governmentId: str
    email: str
    debtAmount: float
    debtDueDate: date
    debtID: str

    @classmethod
    def insert_debits(
        self, dataframe: DataFrame, using_repository: DebitRepository
    ) -> int | None:
        return using_repository.insert_debits(dataframe)

    @classmethod
    def get_debit_by_due_date(
        self, due_date: str, using_repository: DebitRepository
    ) -> list | None:
        return using_repository.get_debit_by_due_date(due_date)
