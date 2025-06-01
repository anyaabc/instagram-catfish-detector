import sqlite3

conn = sqlite3.connect('data/face_embeddings.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)
conn.close()
