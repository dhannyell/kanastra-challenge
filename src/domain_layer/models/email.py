from dataclasses import dataclass

from domain_layer.models.debit import Debit
from domain_layer.abstract.email import Email as EmailRepository


@dataclass
class Email:
    @classmethod
    def send_email(self, debits: Debit, using_service: EmailRepository):
        return using_service.send_email(debits)