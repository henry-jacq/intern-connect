from flask import Flask

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='hhh123'
    
    from .auth import auth

    app.register_blueprint(auth,url_prefix=str('/'))
    
    return app

