import pandas as pd
from io import BytesIO

from application_layer.adapter.debit_repository import DebitRepository
from domain_layer.models.debit import Debit


class DebitUseCase:
    @classmethod
    def save_debits(cls, file_stream: BytesIO) -> None:
        file_dataframe = pd.read_csv(file_stream, encoding="unicode_escape")

        return Debit.insert_debits(file_dataframe, DebitRepository)
