from app import app, db


# It will create tables required for the application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
