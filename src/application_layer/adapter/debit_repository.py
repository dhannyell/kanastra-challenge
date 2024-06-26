import logging
from pandas import DataFrame
from flask import current_app as server
from domain_layer.abstract.debit import DebitRepository, InsertDebitsException

logger = logging.getLogger("Debit Repository.")

class DebitRepository(DebitRepository):
    @classmethod
    def insert_debits(cls, dataframe: DataFrame) -> int|None:
        logger.info(
            "Inserting Debit Data From CSV File",
            extra={
                "props": {
                    "method": "insert_debit",
                    "file_lenght": dataframe.size
                }
            },
        )

        try:
            return dataframe.to_sql('debits', server.db.get_engine(), index=True, index_label='id', if_exists="replace")
        except Exception as exception:
            logger.exception(
                "Error When Trying to Insert Debit Data From CSV",
                extra={
                    "props": {
                        "method": "insert_debit",
                        "file_lenght": dataframe.size,
                        "exception": str(exception)
                    }
                },
            )

            raise InsertDebitsException(exception)