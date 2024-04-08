
from flask import jsonify, Flask
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException
from flask_jwt_extended.exceptions import JWTExtendedException


def init_api_errorhandlers(app : Flask):
    # This function is connected to app

    @app.errorhandler(HTTPException)
    def api_errors_AuthErrorHTTPException(error):
        return jsonify({
            "ok": False,
            "error_code": error.code,
            "description": error.description or 'Bad request.'
            }), error.code or 400
    

def init_jwt_errorhandlers(jwt : JWTManager):

    @jwt.expired_token_loader
    def my_expired_token_callback(jwt_header, jwt_payload):
        return jsonify(code="dave", err="I can't let you do that"), 401





