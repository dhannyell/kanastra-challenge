from abc import ABC
from pandas import DataFrame


class DebitRepositoryException(Exception):
    pass


class Debit(ABC):
    @classmethod
    def insert_debits(self, dataframe: DataFrame) -> int | None:
        return NotImplementedError

    @classmethod
    def get_debit_by_due_date(self, due_date: str) -> list | None:
        return NotImplementedError
