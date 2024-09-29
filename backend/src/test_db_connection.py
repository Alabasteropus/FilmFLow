# test_db_connection.py
import os
from src import create_app, db
from src.models.user import User
from src.models.script import Script

def test_connection():
    app = create_app()
    with app.app_context():
        try:
            db.create_all()
            print("Database connected and tables created successfully.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()
