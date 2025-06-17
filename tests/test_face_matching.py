# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# from core.face_matching import find_potential_catfish_accounts

# def main():
#     uploaded_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/uploads/test.jpg'))
#     results = find_potential_catfish_accounts(uploaded_image_path)

#     if results:
#         print(f"✅ Found {len(results)} match(es):"
#         for r in results:
#             date = r.get("date_posted") or "N/A"
#             print(f"- {r['username']} | Score: {r['similarity']} | Date: {date}")
#     else:
#         print("🚫 We can't find similar faces (either face not detected, or our database isn't up-to-date).")

# if __name__ == "__main__":
#     main()


# #SCRIPT 2
import sys
import os

# Tambahkan path agar bisa import dari src/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.face_matching import find_potential_catfish_accounts

def main():
    # Path ke gambar yang akan diuji
    uploaded_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/uploads/DKQ7msOzt3k_0.jpg '))

    if not os.path.exists(uploaded_image_path):
        print(f"File not found: {uploaded_image_path}")
        return

    # Panggil fungsi untuk mendeteksi akun catfishing
    results = find_potential_catfish_accounts(uploaded_image_path)

    # Cetak hasil
    if results:
        print(f"✅ Found {len(results)} match(es):\n")
        for match in results:
            sumber = "Profile Picture" if match['source_type'] == 'profile' else "Post"
            print(f"- {match['username']} | Score: {match['similarity']} | Source: {sumber} | Date: {match['date_posted'] or 'N/A'}")
    else:
        print("❌ We can't find any similar faces to that (either face not detected, or our database isn't up-to-date).")

if __name__ == "__main__":
    main()


# import sys
# import os
# import unittest
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from src.core.face_matching import find_potential_catfish_accounts

# class TestFaceMatching(unittest.TestCase):
#     def setUp(self):
#         self.test_image = "tests/test_images/test_face.jpg"  # Siapkan sample image
    
#     def test_face_matching(self):
#         results = find_potential_catfish_accounts(self.test_image)
#         print("Hasil matching:", results)
#         self.assertIsInstance(results, list)

# if __name__ == "__main__":
#     unittest.main()
