from unittest import mock

import pandas as pd

from src.application_layer.adapter.debit_repository import DebitRepository
from src.domain_layer.models.debit import Debit


@mock.patch.object(DebitRepository, "insert_debits")
def test_insert_debits(insert_debits_mock, csv_string):

    dataframe = pd.read_csv(csv_string)
    insert_debits_mock.return_value = 1

    inserted_rows = Debit.insert_debits(dataframe, DebitRepository)

    assert inserted_rows == 1
    insert_debits_mock.assert_called_once_with(dataframe)


@mock.patch.object(DebitRepository, "get_debit_by_due_date")
def test_get_debit_by_due_date(get_debit_by_due_date_mock):

    get_debit_by_due_date_mock.return_value = []

    due_date = "2024-06-26"

    Debit.get_debit_by_due_date(due_date, DebitRepository)

    get_debit_by_due_date_mock.assert_called_with(due_date)
