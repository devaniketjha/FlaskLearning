# This is for testing purposes only.

from hello import app, db

with app.app_context():
    db.create_all()
    print("Database tables created!")
