from functools import wraps
from flask import request

def validate_header(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        content_type = request.headers.get("Content-Type", "")

        if "multipart/form-data" not in content_type:
            return {"message":"Invalid Content-Type. Include multipart/form-data in Content-Type Header"},400
        
        return f(*args, **kwargs)
    return decorated_function