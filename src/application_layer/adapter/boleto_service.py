import logging
from domain_layer.abstract.boleto import Boleto
from domain_layer.models.debit import Debit

logger = logging.getLogger("Boleto Service.")

class BoletoService(Boleto):
    @classmethod
    def generate_boletos(cls, debits: list[Debit]) -> None:
        for debit in debits:
            logger.info(f'Generating Boleto for client {debit.name}',
                extra={
                    "service": "BoletoService",
                    "method": "generate_boletos",
            })
