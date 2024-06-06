from flask import Flask
import os
from .extensions import db
from .auth import auth
from .views import views

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')

    user = os.getenv('DB_USER')
    passwd = os.getenv('DB_PASS')
    db_name = os.getenv('DB_NAME')
    db_host = os.getenv('DB_HOST')

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{user}:{passwd}@{db_host}/{db_name}"
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'hhh123')

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    return app
