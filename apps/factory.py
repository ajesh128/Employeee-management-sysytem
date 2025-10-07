import sqlite3
from os import path
from flask import Flask
from apps.routes import test_module

def create_app(config_type="config.Config"):
    app = Flask(__name__)
    app.config.from_object(obj=config_type)

    if not db_has_tables("apps/database.db"):
        init_sqldb()

    app.register_blueprint(test_module)
    return app


def db_has_tables(db_path):
    """Check if the SQLite database has any user tables"""
    if not path.exists(db_path):
        print("hell0oooooooo")
        return False

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    connection.close()
    return len(tables) > 0


def init_sqldb():
    """To create or initialize the database schema"""
    connection = sqlite3.connect("apps/database.db")

    with open('apps/schema.sql', encoding="utf-8") as schema_file:
        connection.executescript(schema_file.read())

    connection.commit()
    connection.close()
