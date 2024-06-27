from unittest import mock

import pandas as pd
import pytest
from flask import current_app

from application_layer.adapter.debit_repository import DebitRepository
from application_layer.persistency.debit import debit_table


@pytest.fixture()
def create_debit(app):
    debit = debit_table.insert().values(
        name="Luiz Da Silva",
        governmentId="98754321",
        email="teste@teste.com",
        debtAmount=123,
        debtDueDate="2024-06-26",
        debtId="teste debtId",
    )
    current_app.db.session.execute(debit)
    current_app.db.session.flush()


def test_insert_debits_success(csv_string, app):
    dataframe = pd.read_csv(csv_string)

    inserted_rows = DebitRepository.insert_debits(dataframe)

    assert inserted_rows == 1


@pytest.mark.skip
def test_get_debit_by_due_date_success(create_debit, app):
    debtDueDate = "2024-06-26"

    debits = DebitRepository.get_debit_by_due_date(due_date=debtDueDate)

    assert len(debits) == 1
    assert debits[0].name == "Luiz Da Silva"


@mock.patch("src.application_layer.adapter.debit_repository.logger.exception")
@mock.patch("src.application_layer.adapter.debit_repository.server.db.session.query")
def test_get_by_debtDueDate_when_return_exception(
    mock_db_query, mock_log_exception, app
):

    message = "Error When Trying to get Debits by Due Date"
    mock_db_query.side_effect = Exception(message)
    debtDueDate = "2024-06-26"

    with pytest.raises(Exception, match=message):
        DebitRepository.get_debit_by_due_date(due_date=debtDueDate)

    mock_log_exception.assert_called_once_with(
        message,
        extra={
            "props": {
                "service": "DebitRepository",
                "method": "get_debit_by_due_date",
                "due_date": debtDueDate,
                "exception": str(Exception(message)),
            }
        },
    )
