from unittest import mock

from domain_layer.models.debit import Debit
from src.application_layer.adapter.boleto_service import BoletoService
from src.application_layer.adapter.debit_repository import DebitRepository
from src.application_layer.adapter.email_service import EmailService
from src.application_layer.use_cases.debit import DebitUseCase


@mock.patch.object(Debit, "insert_debits")
@mock.patch.object(DebitRepository, "get_debit_by_due_date")
@mock.patch.object(BoletoService, "generate_boletos")
@mock.patch.object(EmailService, "send_email")
def test_save_debits_without_data_inserted(
    send_email_mock,
    generate_boletos_mock,
    get_debit_by_due_date_mock,
    insert_debits_mock,
    csv_string,
):

    insert_debits_mock.return_value = None

    result = DebitUseCase.save_debits(csv_string)

    assert result is None
    assert get_debit_by_due_date_mock.call_count == 0
    assert send_email_mock.call_count == 0
    assert generate_boletos_mock.call_count == 0
    insert_debits_mock.assert_called_once()


@mock.patch.object(Debit, "insert_debits")
@mock.patch.object(DebitUseCase, "_process_email_and_boleto_in_background")
def test_save_debits_with_data_inserted(
    process_email_and_boleto_in_background_mock, insert_debits_mock, csv_string
):

    insert_debits_mock.return_value = 10

    result = DebitUseCase.save_debits(csv_string)

    assert result == 10
    process_email_and_boleto_in_background_mock.assert_called_once()
    insert_debits_mock.assert_called_once()
