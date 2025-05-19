from deepface import DeepFace

# Define the image paths
img1_path = r"C:\Users\karin\OneDrive - Bina Nusantara\Documents\deepface\img3.jpg"
img2_path = r"C:\Users\karin\OneDrive - Bina Nusantara\Documents\deepface\img5.jpg"

# List of models to use
models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace"]

# Initialize a dictionary to store verification results
verification_results = {}

# Verify the two images using each model
for model in models:
    try:
        result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path, model_name=model)
        verification_results[model] = result
    except Exception as e:
        verification_results[model] = str(e)  # store error message as string

# Print the aggregated verification results
for model, result in verification_results.items():
    print(f"\nModel: {model}")
    if isinstance(result, dict):
        print(f"  Verified: {result['verified']} (Distance: {result['distance']})")
    else:
        print(f"  Error: {result}")
