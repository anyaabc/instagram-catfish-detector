"""
Script: data/scripts/cek_date_posted_db.py
Purpose: Retrieves and displays the earliest 10 post entries with their dates from the Instagram posts table.
Use Case: Useful for verifying data integrity or checking timestamp formatting in the database.

Features:
- Connects to MySQL database using configured credentials
- Fetches the first 10 records (by ID) from instagram_posts table
- Displays post_id and date_posted in a readable format
- Includes error handling for database connection issues

Dependencies:
- mysql.connector: For MySQL database interactions
- Python 3.x

Configuration:
- Requires DB_CONFIG from backend.config with valid database credentials

Output Format:
📅 10 Data date_posted pertama:
- [post_id] | [date_posted]
- ...

Error Handling:
- Catches and displays MySQL connection errors with 🚫 prefix
"""

# file: data/scripts/cek_date_posted_db.py

import mysql.connector
import os
import sys

# Import DB config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))
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
        print(f"🚫 Database mistake: {err}")

if __name__ == "__main__":
    main()
