from dataclasses import dataclass

from domain_layer.abstract.boleto import Boleto as BoletoService


@dataclass
class Boleto:
    client_name:str
    value: float
    due_date: str
    client_email:str

    @classmethod
    def generate_boletos(self, debits: list, using_service:BoletoService):
        return using_service.generate_boletos(debits)