"""
data/scripts/cek_date_posted_db.py

Fungsi: Mengecek 10 data postingan Instagram pertama (post_id & tanggal) dari database.
Output: Menampilkan hasil dalam format mudah dibaca.
Error: Menangkap dan menampilkan error koneksi database.
"""

import os
import sys
import mysql.connector
import json

# Tambahkan path ke folder src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))
from backend.config import DB_CONFIG
def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT post_id, embedding FROM face_embeddings LIMIT 10
    """)
    results = cursor.fetchall()

    print("🔎 Sample post_id from face_embeddings:")
    for row in results:
        print(f"- post_id: {row['post_id']}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
