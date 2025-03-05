from deepface import DeepFace

def verify_faces(img1_path, img2_path):
    try:
        result = DeepFace.verify(img1_path, img2_path)
        return result["verified"]
    except:
        return False
