from app.config.database import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("SELECT 1")
result = cursor.fetchone()

print("DB Connected:", result)