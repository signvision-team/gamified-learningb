import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",   # IMPORTANT (not localhost)
        port=3307,          # because docker exposes 3307
        user="gamify_user",
        password="gamify_pass",
        database="gamify_db"
    )