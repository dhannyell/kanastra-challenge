from datetime import date
import logging

from flask import current_app as server
from pandas import DataFrame

from domain_layer.abstract.debit import Debit, DebitRepositoryException
from domain_layer.models.debit import Debit as DebitModel
from application_layer.persistency.debit import debit_table

logger = logging.getLogger("Debit Repository.")

class DebitRepository(Debit):
    @classmethod
    def insert_debits(cls, dataframe: DataFrame) -> int | None:
        logger.info(
            "Inserting Debit Data From CSV File",
            extra={"props": {"service": "DebitRepository","method": "insert_debit", "file_lenght": dataframe.size}},
        )

        try:
            return dataframe.to_sql(
                "debits",
                server.db.get_engine(),
                index=True,
                index_label="id",
                if_exists="replace",
            )
        except Exception as exception:
            logger.exception(
                "Error When Trying to Insert Debit Data From CSV",
                extra={
                    "props": {
                        "service": "DebitRepository",
                        "method": "insert_debit",
                        "file_lenght": dataframe.size,
                        "exception": str(exception),
                    }
                },
            )

            raise DebitRepositoryException(exception)
        
    @classmethod
    def get_debit_by_due_date(cls, due_date: str) -> list[DebitModel] | None:
        logger.info(
            "Getting debits by due date",
            extra={"props": {"service": "DebitRepository","method": "get_debit_by_due_date", "due_date": due_date}},
        )

        try:
            return cls._process_get_debit_by_due_date_response(
                debits = server.db.session.query(debit_table).filter(
                debit_table.c.debtDueDate == due_date
            ).all())

        except Exception as exception:
            logger.exception(
                "Error When Trying to get Debits by Due Date",
                extra={
                    "props": {
                        "service": "DebitRepository",
                        "method": "get_debit_by_due_date",
                        "due_date": due_date,
                        "exception": str(exception),
                    }
                },
            )

            raise DebitRepositoryException(exception)

    @staticmethod
    def _process_get_debit_by_due_date_response(debits) -> list[DebitModel] | None:
        if debits:
            return [DebitModel(
                name=d.name,
                debtAmount=d.debtAmount,
                debtID=d.debtId,
                email=d.email,
                governmentId=d.governmentId,
                debtDueDate=d.debtDueDate
            ) for d in debits]

        return None