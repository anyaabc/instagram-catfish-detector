#SCRIPT DB SET UP menggunakan SQLite, jangan dijalankan
import os
import json
import sqlite3
import requests
from tqdm import tqdm

# --- CONFIGURATIONS ---
DATASET_FILE = 'data/dataset.json'            # Dataset location
DB_FILE = 'data/instagram_posts.db'           # Output SQLite DB path
DOWNLOAD_DIR = 'data/downloads'               # Folder for downloaded images

# --- INITIAL SETUP ---
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

# --- CONNECT TO DATABASE ---
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# --- CREATE TABLE IF NOT EXISTS ---
cur.execute('''
CREATE TABLE IF NOT EXISTS posts (
    post_id TEXT PRIMARY KEY,
    username TEXT,
    user_id TEXT,
    profile_url TEXT,
    profile_image_url TEXT,     -- URL asli dari JSON
    profile_image_local TEXT,   -- path lokal foto profil
    followers INTEGER,
    posts_count INTEGER,
    is_verified BOOLEAN,
    shortcode TEXT,
    post_url TEXT,
    content_type TEXT,
    date_posted TEXT,
    num_comments INTEGER,
    likes INTEGER,
    image_local_paths TEXT
)
''')
conn.commit()

# --- IMAGE DOWNLOAD FUNCTION ---
def download_image(url, save_path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"⚠️ Failed to download {url}: {e}")
        return False

# --- MAIN PROCESSING LOOP ---
inserted_count = 0

with open(DATASET_FILE, 'r', encoding='utf-8') as f:
    for line in tqdm(f, desc="🔄 Processing posts"):
        try:
            post = json.loads(line.strip())
            username = post.get("user_posted")
            shortcode = post.get("shortcode")
            post_id = post.get("post_id")

            if not (username and post_id and shortcode):
                continue  # skip incomplete entries

            # Create folder for this user's images
            user_dir = os.path.join(DOWNLOAD_DIR, username)
            os.makedirs(user_dir, exist_ok=True)

            # --- Download profile picture ---
            profile_image_url = post.get("profile_image_link")
            profile_image_local_path = None
            if profile_image_url:
                profile_image_local_path = os.path.join(user_dir, 'profile.jpg')
                download_image(profile_image_url, profile_image_local_path)

            # --- Download post images ---
            image_paths = []
            for i, img_url in enumerate(post.get("photos", [])):
                filename = f"{shortcode}_{i}.jpg"
                save_path = os.path.join(user_dir, filename)
                if download_image(img_url, save_path):
                    image_paths.append(save_path)

            # Save metadata into DB
            cur.execute('''
                INSERT OR IGNORE INTO posts (
                    post_id, username, user_id, profile_url, profile_image_url, profile_image_local,
                    followers, posts_count, is_verified, shortcode,
                    post_url, content_type, date_posted,
                    num_comments, likes, image_local_paths
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                post_id,
                username,
                post.get("user_posted_id"),
                post.get("profile_url"),
                profile_image_url,
                profile_image_local_path,
                post.get("followers"),
                post.get("posts_count"),
                int(post.get("is_verified", False)),
                shortcode,
                post.get("url"),
                post.get("content_type"),
                post.get("date_posted"),
                post.get("num_comments"),
                post.get("likes"),
                json.dumps(image_paths)
            ))

            inserted_count += 1

        except Exception as e:
            print(f"❌ Error processing post: {e}")

# --- FINALIZE ---
conn.commit()
conn.close()

print("\n✅ DONE")
print(f"📄 Database saved at: {DB_FILE}")
print(f"🖼️  Images saved under: {DOWNLOAD_DIR}")
print(f"🧮 Total posts inserted: {inserted_count}")
