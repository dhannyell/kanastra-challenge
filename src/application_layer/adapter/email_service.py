import logging

from domain_layer.abstract.email import Email
from domain_layer.models.debit import Debit

logger = logging.getLogger("Email Service.")


class EmailService(Email):
    @classmethod
    def send_email(cls, debits: list[Debit]) -> None:
        for debit in debits:
            logger.info(
                f"Sending Email to client {debit.name}",
                extra={
                    "service": "EmailService",
                    "method": "send_email",
                },
            )
