from unittest import mock

from domain_layer.models.debit import Debit
from src.application_layer.adapter.boleto_service import BoletoService
from src.domain_layer.models.boleto import Boleto


@mock.patch.object(BoletoService, "generate_boletos")
def test_generate_boletos(generate_boletos_mock):

    debit = Debit(
        debtAmount=7811,
        debtID="ea23f2ca-663a-4266-a742-9da4c9f4fcb3",
        email="janet95@example.com",
        name="Elijah Santos",
        debtDueDate="2024-06-26",
        governmentId=9558,
    )

    debits = [debit]

    Boleto.generate_boletos(debits, BoletoService)

    generate_boletos_mock.assert_called_once_with(debits)
