from server.db.recreate_sample_data import recreate_sample_test_data
from server.db.models import db

if __name__ == "__main__":
    from server.apps.app import create_app

    app = create_app()
    # db = SQLAlchemy(app)
    db.drop_all()
    db.create_all()
    
    with app.app_context():
        recreate_sample_test_data()
