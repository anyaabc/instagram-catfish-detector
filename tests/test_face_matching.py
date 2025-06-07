import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.face_matching import find_potential_catfish_accounts

def main():
    uploaded_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/uploads/test.jpg'))
    results = find_potential_catfish_accounts(uploaded_image_path)

    if results:
        print(f"✅ Ditemukan {len(results)} potensi akun catfishing:")
        for r in results:
            date = r.get("date_posted") or "N/A"
            print(f"- {r['username']} | Score: {r['similarity']} | Date: {date}")
    else:
        print("🚫 Tidak ditemukan wajah serupa (kemungkinan bukan catfish atau wajah tidak terdeteksi).")

if __name__ == "__main__":
    main()


