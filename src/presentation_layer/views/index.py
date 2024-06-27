import logging

import io
from flasgger import swag_from
from flask import Blueprint, request
from flask_restx import Api, Resource

from application_layer.use_cases.debit import DebitUseCase
from presentation_layer.schemas import upload_file_model
from util.verify_header import validate_header

logger = logging.getLogger("Debit.")

VERSION = "1.0"
DOC = "API Kanastra"

debit_bp = Blueprint("api", __name__, url_prefix="/api")

api = Api(
    debit_bp,
    version=VERSION,
    title="API Kanastra Backend Challenge Index",
    description=DOC,
    doc=False,
)

ns = api.namespace("", description="API Kanastra Backend Challenge Index")
api.models[upload_file_model.name] = upload_file_model

# Define allowed files
ALLOWED_EXTENSION = "csv"


@ns.route("/upload-file")
class UploadFileResource(Resource):
    @validate_header
    @ns.response(200, "File Uploaded Successfully")
    @ns.response(201, "File Uploaded Successfully")
    @ns.response(500, "Failed to Proccess CSV File")
    @ns.response(400, "Invalid File")
    @swag_from("../../swagger/debit/PUT.yml")
    def put(self):
        received_file = request.files.get("file", None)

        try:
            if received_file and ALLOWED_EXTENSION in received_file.filename:
                data = received_file.read()

                file_object = io.BytesIO(data)

                inserted_number = DebitUseCase.save_debits(file_object)

                if inserted_number and inserted_number > 0:
                    return {"message": "File Uploaded Successfully"}, 201

                return {"message": "File Uploaded Successfully"}, 200

            return {"message": "Invalid File"}, 400
        except Exception as exception:
            message = "Failed to Proccess CSV File"
            logger.exception(
                message,
                extra={
                    "props": {
                        "request": "/api/upload-file",
                        "method": "PUT",
                        "file": received_file.filename if received_file else None,
                        "error_message": str(exception),
                    }
                },
            )

            return {"message": message}, 500
