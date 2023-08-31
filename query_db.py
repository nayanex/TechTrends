import sqlite3
from flask import g

db_connection_count = 0  # Global counter to track database connections


def get_db_connection():
    global db_connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connection_count += 1  # Increment the connection counter
    g.db_connection = connection  # Set the connection in the g object
    return connection


def get_db_connection_count():
    return db_connection_count


def get_post_count():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM posts")
    post_count = cursor.fetchone()[0]
    connection.close()
    return post_count
