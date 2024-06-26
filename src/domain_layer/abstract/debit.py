from abc import ABC

from pandas import DataFrame


class InsertDebitsException(Exception):
    pass

class DebitRepository(ABC):
    @classmethod
    def insert_debits(dataframe: DataFrame) -> int|None:
        return NotImplementedError