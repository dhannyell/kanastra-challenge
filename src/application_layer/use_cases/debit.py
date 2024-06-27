from datetime import datetime
import logging
from celery import shared_task
from celery.contrib.abortable import AbortableTask
import pandas as pd
from io import BytesIO

from application_layer.adapter.boleto_service import BoletoService
from application_layer.adapter.debit_repository import DebitRepository
from application_layer.adapter.email_service import EmailService
from domain_layer.models.boleto import Boleto
from domain_layer.models.debit import Debit
from domain_layer.models.email import Email


logger = logging.getLogger("Debit Use Case.")

class DebitUseCase:
    @classmethod
    def save_debits(cls, file_stream: BytesIO) -> None:
        file_dataframe = pd.read_csv(file_stream, encoding="unicode_escape")

        inserted_rows =  Debit.insert_debits(file_dataframe, DebitRepository)

        if inserted_rows > 0:
            cls._process_email_and_boleto_in_background()
        
        return inserted_rows
    
    @shared_task(bind=True, base=AbortableTask)
    def _process_email_and_boleto_in_background(cls):
        logger.info(
            "Starting Background Service"
        )

        current_date = datetime.today().strftime('%Y-%m-%d')

        debits_pending = Debit.get_debit_by_due_date(
            current_date,
            DebitRepository
        )

        Boleto.generate_boletos(
            debits_pending,
            BoletoService
        )

        Email.send_email(
            debits_pending,
            EmailService
        )


