# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# from core.face_matching import find_potential_catfish_accounts

# def main():
#     uploaded_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/uploads/test.jpg'))
#     results = find_potential_catfish_accounts(uploaded_image_path)

#     if results:
#         print(f"✅ Ditemukan {len(results)} potensi akun catfishing:")
#         for r in results:
#             date = r.get("date_posted") or "N/A"
#             print(f"- {r['username']} | Score: {r['similarity']} | Date: {date}")
#     else:
#         print("🚫 Tidak ditemukan wajah serupa (kemungkinan bukan catfish atau wajah tidak terdeteksi).")

# if __name__ == "__main__":
#     main()


#SCRIPT 2
import sys
import os

# Tambahkan path agar bisa import dari src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.face_matching import find_potential_catfish_accounts

def main():
    # Path ke gambar yang akan diuji
    uploaded_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/uploads/DKQ7msOzt3k_0.jpg '))

    if not os.path.exists(uploaded_image_path):
        print(f"🚫 File tidak ditemukan: {uploaded_image_path}")
        return

    # Panggil fungsi untuk mendeteksi akun catfishing
    results = find_potential_catfish_accounts(uploaded_image_path)

    # Cetak hasil
    if results:
        print(f"✅ Ditemukan {len(results)} potensi akun catfishing:\n")
        for match in results:
            sumber = "dari foto profil" if match['source_type'] == 'profile' else "dari postingan"
            print(f"- {match['username']} | Score: {match['similarity']} | Source: {sumber} | Date: {match['date_posted'] or 'N/A'}")
    else:
        print("❌ Tidak ada akun catfishing yang terdeteksi.")

if __name__ == "__main__":
    main()
