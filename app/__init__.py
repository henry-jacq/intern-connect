from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from auth import auth
from views import views
import os

db = SQLAlchemy()

def create_app():
    app=Flask(__name__)

    user = os.getenv('DB_USER')
    passwd = os.getenv('DB_USER')
    db_name = os.getenv('DB_NAME')
    db_host = os.getenv('DB_HOST')

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{user}:{passwd}@{db_host}/{db_name}"

    # Initialize extensions
    db.init_app(app)

    app.config['SECRET_KEY']='hhh123'

    app.register_blueprint(auth,url_prefix=str('/'))
    app.register_blueprint(views,url_prefix=str('/'))
    return app
