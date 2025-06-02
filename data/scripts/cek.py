# file: data/scripts/cek.py

import sys
import os

# Tambahkan path ke folder src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import mysql.connector
from backend.config import DB_CONFIG

# Cek isi tabel
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM instagram_users;")
users_count = cursor.fetchone()[0]
print(f"👤 Users: {users_count}")

cursor.execute("SELECT COUNT(*) FROM instagram_posts;")
posts_count = cursor.fetchone()[0]
print(f"📷 Posts: {posts_count}")

cursor.execute("SELECT COUNT(*) FROM face_embeddings;")
embeddings_count = cursor.fetchone()[0]
print(f"🧠 Embeddings: {embeddings_count}")

cursor.close()
conn.close()
