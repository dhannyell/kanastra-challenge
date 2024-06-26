from flask_restx import fields, Model

upload_file_model = Model(
    'file',
    {
        'filename': fields.String(nullable=False, required=True)
    }
)