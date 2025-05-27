import sys
import os
import sqlite3
import json

# --- Allow import from root directory ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.core.face_matching import extract_face_embeddings, match_embeddings

DB_PATH = "data/instagram_posts.db"
TOP_K = 3

def fetch_sample_images(limit=5):
    """Fetch a few sample images from DB for testing."""
    if not os.path.exists(DB_PATH):
        print(f"🚫 Database not found at {DB_PATH}")
        return []

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT username, profile_image_local, image_local_paths 
        FROM posts 
        WHERE profile_image_local IS NOT NULL 
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()

    test_cases = []
    for username, profile_path, image_paths_json in rows:
        try:
            image_paths = json.loads(image_paths_json)
            if image_paths:
                test_cases.append({
                    "username": username,
                    "profile_image": profile_path,
                    "post_image": image_paths[0]
                })
        except json.JSONDecodeError:
            continue

    return test_cases


def test_image(image_path, expected_username):
    """Run embedding + match on an image."""
    embeddings = extract_face_embeddings(image_path)
    if not embeddings:
        print("❌ No face detected or failed to extract embeddings.")
        return False

    matches = match_embeddings(embeddings, top_k=TOP_K)
    for match in matches:
        if match['username'] == expected_username:
            print(f"✅ Match found: {match['username']} (score: {match['match_score']})")
            return True

    print("❌ No correct match found.")
    return False


def run_tests():
    """Run face matching tests using sample images from DB."""
    test_cases = fetch_sample_images()
    total = len(test_cases) * 2
    passed = 0

    print(f"\n🧪 Running {total} tests on {len(test_cases)} users...\n")

    for i, case in enumerate(test_cases):
        print(f"--- Test Case {i + 1}: {case['username']} ---")

        print("📸 Testing profile image...")
        if test_image(case['profile_image'], case['username']):
            passed += 1

        print("🖼️ Testing post image...")
        if test_image(case['post_image'], case['username']):
            passed += 1

        print()

    print(f"✅ {passed}/{total} tests passed.")
    print("✔️ Test completed.\n")


if __name__ == "__main__":
    run_tests()
