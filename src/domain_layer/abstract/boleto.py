from abc import ABC


class Boleto(ABC):
    @classmethod
    def generate_boletos(debits) -> None:
        return NotImplementedError
