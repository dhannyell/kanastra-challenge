from flask_restx import Model, fields

upload_file_model = Model(
    "file", {"filename": fields.String(nullable=False, required=True)}
)
