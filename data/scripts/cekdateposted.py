# file: data/scripts/cek_date_posted_db.py

import mysql.connector
import os
import sys

# Import DB config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from backend.config import DB_CONFIG

def main():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT post_id, date_posted FROM instagram_posts ORDER BY id ASC LIMIT 10;
        """)

        results = cursor.fetchall()

        print("📅 10 Data date_posted pertama:")
        for post_id, date_posted in results:
            print(f"- {post_id} | {date_posted}")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"🚫 Database error: {err}")

if __name__ == "__main__":
    main()
