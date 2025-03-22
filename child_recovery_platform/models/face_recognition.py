import insightface
import numpy as np
from insightface.app import FaceAnalysis
import cv2

# Initialize InsightFace model
face_app = FaceAnalysis(providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))

def extract_face_embedding(image_path):
    """Extract facial embeddings using InsightFace"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image from {image_path}")
    faces = face_app.get(img)

    if len(faces) > 0:
        return faces[0].normed_embedding  # Return first face embedding
    return None

def verify_faces(img1_path, img2_path):
    """Compare two images using InsightFace embeddings"""
    embedding1 = extract_face_embedding(img1_path)
    embedding2 = extract_face_embedding(img2_path)

    if embedding1 is None or embedding2 is None:
        return False  # No face detected in one of the images

    similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    return similarity > 0.6  # Use threshold to determine match
