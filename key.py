from helpers import get_db

db = get_db()

cursor = db.execute("SELECT * FROM categories")
row = cursor.fetchone()

print(row)
db.close()