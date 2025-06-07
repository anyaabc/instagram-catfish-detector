#script testing
from flask import Flask, jsonify
import sqlite3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

app = Flask(__name__)

DB_PATH = "data/face_embeddings.db"
SIMILARITY_THRESHOLD = 0.7

def load_embeddings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT username, image_type, image_path, embedding FROM face_embeddings")
    rows = cursor.fetchall()
    conn.close()

    embeddings_dict = {}
    for username, image_type, image_path, embedding_str in rows:
        embedding = np.array(json.loads(embedding_str), dtype=np.float32)
        if username not in embeddings_dict:
            embeddings_dict[username] = {'profile': None, 'posts': []}
        if image_type == 'profile':
            embeddings_dict[username]['profile'] = (image_path, embedding)
        else:
            embeddings_dict[username]['posts'].append((image_path, embedding))
    return embeddings_dict

def compare_embeddings(embeddings_dict):
    results = []
    for username, data in embeddings_dict.items():
        profile = data['profile']
        posts = data['posts']

        if not profile or not posts:
            results.append({
                "username": username,
                "status": "⚠️ Missing profile or post embeddings",
                "similarity": None
            })
            continue

        profile_path, profile_embedding = profile
        matched = False
        for post_path, post_embedding in posts:
            similarity = cosine_similarity([profile_embedding], [post_embedding])[0][0]
            if similarity >= SIMILARITY_THRESHOLD:
                matched = True
                results.append({
                    "username": username,
                    "status": "✅ Match",
                    "similarity": round(similarity, 4)
                })
                break

        if not matched:
            results.append({
                "username": username,
                "status": "❌ No match",
                "similarity": None
            })
    return results

@app.route("/api/face_matching", methods=["GET"])
def face_matching_api():
    embeddings_dict = load_embeddings()
    results = compare_embeddings(embeddings_dict)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
