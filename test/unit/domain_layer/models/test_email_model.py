from unittest import mock

from domain_layer.models.debit import Debit
from src.application_layer.adapter.email_service import EmailService
from src.domain_layer.models.email import Email


@mock.patch.object(EmailService, "send_email")
def test_send_email(send_email_mock):

    debit = Debit(
        debtAmount=7811,
        debtID="ea23f2ca-663a-4266-a742-9da4c9f4fcb3",
        email="janet95@example.com",
        name="Elijah Santos",
        debtDueDate="2024-06-26",
        governmentId=9558,
    )

    debits = [debit]

    Email.send_email(debits, EmailService)

    send_email_mock.assert_called_once_with(debits)
