from flask_sqlalchemy import SQLAlchemy
from flask import send_from_directory
import os, time
from werkzeug.utils import secure_filename


db = SQLAlchemy()
upload_path = os.path.join(os.path.abspath(os.path.join(os.getcwd())), 'uploads')


# Get random filename
def get_random_filename(name):
    filename = secure_filename(name)
    # Split the filename to add a timestamp before the extension
    name, ext = os.path.splitext(filename)
    timestamp = str(int(time.time()))
    new_filename = f"{name}_{timestamp}{ext}"
    return new_filename

def get_uploads(filename, path=upload_path):
    return send_from_directory(path, filename)
