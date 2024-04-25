from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .auth import auth
from .views import views
import os
from .extensions import db

def create_app():
    app = Flask(__name__, static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static')),
                         template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')))

    user = os.getenv('DB_USER')
    passwd = os.getenv('DB_PASS')
    db_name = os.getenv('DB_NAME')
    db_host = os.getenv('DB_HOST')

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{user}:{passwd}@{db_host}/{db_name}"
    
    # Initialize extensions
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.config['SECRET_KEY'] = 'hhh123'

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    return app
