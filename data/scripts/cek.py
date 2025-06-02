# # file: data/scripts/cek.py

# import sys
# import os

# # Tambahkan path ke folder src/
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# import mysql.connector
# from backend.config import DB_CONFIG

# # Cek isi tabel
# conn = mysql.connector.connect(**DB_CONFIG)
# cursor = conn.cursor()

# cursor.execute("SELECT COUNT(*) FROM instagram_users;")
# users_count = cursor.fetchone()[0]
# print(f"👤 Users: {users_count}")

# cursor.execute("SELECT COUNT(*) FROM instagram_posts;")
# posts_count = cursor.fetchone()[0]
# print(f"📷 Posts: {posts_count}")

# cursor.execute("SELECT COUNT(*) FROM face_embeddings;")
# embeddings_count = cursor.fetchone()[0]
# print(f"🧠 Embeddings: {embeddings_count}")

# cursor.close()
# conn.close()



# cek database

import sys
import os

# Tambahkan path ke folder src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import mysql.connector
from backend.config import DB_CONFIG


def cek_tabel():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("Tables in DB:")
    for t in tables:
        print(t[0])

    cursor.execute("DESCRIBE instagram_users")
    print("\nStructure of instagram_users:")
    for row in cursor.fetchall():
        print(row)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    cek_tabel()

