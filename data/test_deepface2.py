from deepface import DeepFace

# Paths to the images to compare
img1_path = r"C:\Users\karin\OneDrive - Bina Nusantara\Documents\skripsi\instagram-catfish-detector\data\img3.jpg"
img2_path = r"C:\Users\karin\OneDrive - Bina Nusantara\Documents\skripsi\instagram-catfish-detector\data\img5.jpg"

# Compare faces
try:
    result = DeepFace.verify(img1_path, img2_path, model_name="VGG-Face")
    print("Are they the same person?", result["verified"])
    print("Distance between embeddings:", result["distance"])
except Exception as e:
    print("Error during face verification:", e)
