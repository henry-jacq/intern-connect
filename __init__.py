from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app=Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hari@local@localhost/internship'
    # Other configuration settings...

    # Initialize extensions
    db.init_app(app)

    app.config['SECRET_KEY']='hhh123'
    
    from .auth import auth

    app.register_blueprint(auth,url_prefix=str('/'))
    
    return app

