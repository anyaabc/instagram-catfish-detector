#SCRIPT untuk sql
import os
import json
import sqlite3
from tqdm import tqdm
from deepface import DeepFace

# --- CONFIG ---
DB_PATH = "data/instagram_posts.db"
MODEL_NAMES = ["ArcFace", "Facenet512", "VGG-Face"]

# --- CONNECT TO DB ---
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# --- CREATE TABLE ---
cur.execute('''
CREATE TABLE IF NOT EXISTS face_embeddings (
    embedding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    image_type TEXT,  -- 'profile' or 'post'
    image_path TEXT,
    embedding TEXT     -- JSON string: {model_name: embedding_list}
)
''')
conn.commit()

# --- FACE EMBEDDING FUNCTION ---
def get_face_embeddings(image_path):
    """
    Extract embeddings for all models from one image.
    Returns dict {model_name: embedding_list} or None if no face detected for any model.
    """
    embeddings = {}
    for model_name in MODEL_NAMES:
        try:
            result = DeepFace.represent(
                img_path=image_path,
                model_name=model_name,
                enforce_detection=True
            )
            if result:
                embeddings[model_name] = result[0]["embedding"]
        except Exception as e:
            print(f"⚠️ No face detected in {image_path} for {model_name}: {e}")

    return embeddings if embeddings else None

# --- PROCESS DB POSTS ---
cur.execute("SELECT username, profile_image_local, image_local_paths FROM posts")
rows = cur.fetchall()

count_inserted = 0
for username, profile_img_path, image_paths_json in tqdm(rows, desc="🔍 Extracting face embeddings"):

    # --- PROFILE IMAGE ---
    if profile_img_path and os.path.isfile(profile_img_path):
        embeddings = get_face_embeddings(profile_img_path)
        if embeddings:
            cur.execute('''
                INSERT INTO face_embeddings (username, image_type, image_path, embedding)
                VALUES (?, 'profile', ?, ?)
            ''', (username, profile_img_path, json.dumps(embeddings)))
            conn.commit()
            count_inserted += 1

    # --- POST IMAGES ---
    try:
        image_paths = json.loads(image_paths_json)
    except json.JSONDecodeError:
        image_paths = []

    for img_path in image_paths:
        if img_path and os.path.isfile(img_path):
            embeddings = get_face_embeddings(img_path)
            if embeddings:
                cur.execute('''
                    INSERT INTO face_embeddings (username, image_type, image_path, embedding)
                    VALUES (?, 'post', ?, ?)
                ''', (username, img_path, json.dumps(embeddings)))
                conn.commit()
                count_inserted += 1

# --- DONE ---
conn.close()
print("\n✅ All embeddings processed and stored.")
print(f"🧠 Total embeddings inserted: {count_inserted}")
