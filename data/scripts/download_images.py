""""
data/scripts/download_images.py
Fungsi:
1. Mengimpor data user dan post Instagram dari file JSON ke database MariaDB
2. Mendownload gambar profil user dan gambar post
3. Menyimpan path lokal gambar ke database
Struktur:
- download_image(): Fungsi utilitas untuk download gambar
- main(): Fungsi utama untuk proses:
  * Baca file dataset JSON
  * Simpan data user ke tabel instagram_users
  * Simpan data post ke tabel instagram_posts
  * Download dan simpan gambar terkait
"""
import os
import sys
import json
import requests
from tqdm import tqdm
from datetime import datetime
import mysql.connector

# Path fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from backend.config import DB_CONFIG

# File dan folder
DATASET_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../dataset.json'))
DOWNLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../images'))

def download_image(url, save_path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return save_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def main():
    inserted_users = set()
    inserted_posts = 0

    with open(DATASET_FILE, 'r', encoding='utf-8') as f:
        dataset = json.load(f)

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for post in tqdm(dataset, desc="🔄 Memproses data"):
            try:
                user_id = post.get("user_posted_id")
                username = post.get("user_posted")

                if not user_id or not username:
                    continue

                user_folder = os.path.join(DOWNLOAD_DIR, username)

                # Download profile image
                if user_id not in inserted_users:
                    profile_image_url = post.get("profile_image_link")
                    profile_image_local = None

                    if profile_image_url:
                        profile_image_local = os.path.join(user_folder, 'profile.jpg')
                        download_image(profile_image_url, profile_image_local)

                    cursor.execute("""
                        INSERT IGNORE INTO instagram_users (
                            user_id, username, profile_url, profile_image_url,
                            profile_image_local, followers, posts_count, is_verified
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        user_id,
                        username,
                        post.get("profile_url"),
                        profile_image_url,
                        profile_image_local,
                        post.get("followers", 0),
                        post.get("posts_count", 0),
                        bool(post.get("is_verified", False))
                    ))
                    inserted_users.add(user_id)

                post_id = post.get("post_id")
                if not post_id:
                    continue

                shortcode = post.get("shortcode")
                post_url = post.get("url")
                image_urls = post.get("photos", [])
                content_type = post.get("content_type")

                image_paths = []
                for i, img_url in enumerate(image_urls):
                    filename = f"{shortcode}_{i}.jpg"
                    local_path = os.path.join(user_folder, filename)
                    if download_image(img_url, local_path):
                        image_paths.append(local_path)

                image_paths_json = json.dumps(image_paths)

                try:
                    date_posted = datetime.fromisoformat(post.get("date_posted").replace("Z", "+00:00"))
                except:
                    date_posted = None

                cursor.execute("""
                    INSERT IGNORE INTO instagram_posts (
                        post_id, user_id, shortcode, post_url,
                        content_type, date_posted, num_comments,
                        likes, image_local_paths
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    post_id,
                    user_id,
                    shortcode,
                    post_url,
                    content_type,
                    date_posted,
                    post.get("num_comments", 0),
                    post.get("likes", 0),
                    image_paths_json
                ))

                inserted_posts += 1

            except Exception as e:
                print(f"There's a mistake with post processing: {e}")

        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Mistake regarding database: {err}")

    print("\n COMPLETED")
    print(f"New users: {len(inserted_users)}")
    print(f"Inserted posts: {inserted_posts}")
    print(f"Picture folder: {DOWNLOAD_DIR}")

if __name__ == "__main__":
    main()
