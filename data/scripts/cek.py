# import sqlite3
# import pandas as pd

# conn = sqlite3.connect("data/instagram_posts.db")
# df = pd.read_sql("SELECT * FROM posts LIMIT 5", conn)
# print(df)
#SCRIPT untuk mengecek gambar dan meta data dalam database

import sqlite3
import argparse
import json
import os

DB_FILE = 'data/instagram_posts.db'

def print_post(post):
    print(f"\n🧾 Post ID      : {post['post_id']}")
    print(f"👤 Username     : {post['username']}")
    print(f"🆔 User ID      : {post['user_id']}")
    print(f"📸 Profile Pic  : {post['profile_image_local']}")
    print(f"📅 Date Posted  : {post['date_posted']}")
    print(f"💬 Comments     : {post['num_comments']}  ❤️ Likes: {post['likes']}")
    print(f"🖼️ Post Images  :")
    for img_path in json.loads(post['image_local_paths']):
        print(f"   - {img_path}")
    print("------------------------------------------------")

def main(username=None):
    if not os.path.exists(DB_FILE):
        print(f"❌ Database not found at: {DB_FILE}")
        return

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if username:
        cur.execute("SELECT * FROM posts WHERE username = ? ORDER BY date_posted DESC", (username,))
    else:
        cur.execute("SELECT * FROM posts ORDER BY date_posted DESC LIMIT 5")

    rows = cur.fetchall()
    if not rows:
        print("⚠️ No data found.")
    else:
        for row in rows:
            print_post(dict(row))

    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🔍 Inspect Instagram Post DB")
    parser.add_argument("--user", help="Filter by Instagram username")
    args = parser.parse_args()

    main(username=args.user)
