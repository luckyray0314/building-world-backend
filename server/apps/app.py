import os
from flask import Flask, request, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from flask_mail import Mail
from server.db.models import db, setup_db, db_drop_and_create_all
from config import ApplicationConfig
from server.apps.errorhandlers import init_api_errorhandlers
from server.apps.api import init_rest_api
from server.apps.auth import init_rest_api_authentication
from server.mailserver import FlaskMailServer
from ..db.recreate_sample_data import recreate_sample_test_data

app = Flask(__name__, template_folder="../../server/templates")


def create_app(app : Flask = app, test_config=None):

    app.config.from_object(ApplicationConfig)
    # print(app.config)
    app.app_context().push()
    mail = FlaskMailServer(app)

    MIGRATION_DIR = os.path.join('server','db', 'migrations')
    Migrate(app, db, directory=MIGRATION_DIR)


    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})


    if test_config or os.getenv('DB_RESTART', False) == 'true':
        setup_db(app, restart=True)
        recreate_sample_test_data()

    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,PATCH,POST,DELETE,OPTIONS')
        return response

    
    init_rest_api_authentication(app)
    init_rest_api(app)
    init_api_errorhandlers(app)

    return app




