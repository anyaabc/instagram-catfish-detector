# ini script uji cobaa image matching deepface, ngga dipakai lagi 
deepface import DeepFace

# Paths to the images to compare
img1_path = r"C:\Users\karin\OneDrive - Bina Nusantara\Documents\deepface\images1.jpeg"
img2_path = r"C:\Users\karin\OneDrive - Bina Nusantara\Documents\deepface\images2.jpeg"

# Compare faces
try:
    result = DeepFace.verify(img1_path, img2_path, model_name="VGG-Face")
    print("Are they the same person?", result["verified"])
    print("Distance between embeddings:", result["distance"])
except Exception as e:
    print("Error during face verification:", e)
