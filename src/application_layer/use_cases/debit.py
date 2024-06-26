from io import BytesIO
import pandas as pd
from domain_layer.models.debit import Debit
from application_layer.adapter.debit_repository import DebitRepository

class DebitUseCase:
    @classmethod
    def save_debits(cls, file_stream:BytesIO) -> None:
        file_dataframe = pd.read_csv(file_stream, encoding='unicode_escape')

        return Debit.insert_debits(
            file_dataframe,
            DebitRepository
        )