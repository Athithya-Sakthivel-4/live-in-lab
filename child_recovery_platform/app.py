from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import sqlite3
import os
import cv2
import numpy as np
import onnxruntime as ort
from starlette.staticfiles import StaticFiles

app = FastAPI()

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mount static folder for serving images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load ONNX face recognition model (ResNet)
onnx_model_path = "models/resnet_face_recognition.onnx"
ort_session = ort.InferenceSession(onnx_model_path)

# OpenCV Face Detector
face_detector = cv2.dnn.readNetFromCaffe(
    "models/deploy.prototxt", "models/res10_300x300_ssd_iter_140000.caffemodel"
)

def extract_face_embedding(image_path):
    """Extract face embedding using OpenCV DNN + ONNX model"""
    img = cv2.imread(image_path)
    if img is None:
        return None

    h, w = img.shape[:2]
    
    # Face detection
    blob = cv2.dnn.blobFromImage(img, scalefactor=1.0, size=(300, 300), mean=(104.0, 177.0, 123.0))
    face_detector.setInput(blob)
    detections = face_detector.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")

            face = img[y1:y2, x1:x2]
            if face.size == 0:
                continue
            
            # Convert to 1x3x112x112 format (for ONNX model)
            face = cv2.resize(face, (112, 112))
            face = face.transpose(2, 0, 1).astype(np.float32)  # HWC to CHW
            face = np.expand_dims(face, axis=0)

            # Extract embedding using ONNX model
            ort_inputs = {ort_session.get_inputs()[0].name: face}
            embedding = ort_session.run(None, ort_inputs)[0]

            return embedding.flatten()

    return None

# Function to find a match in the database
def find_match(image_path):
    conn = sqlite3.connect("children.db")
    c = conn.cursor()
    c.execute("SELECT id, name, age, image_path FROM missing_children")
    children = c.fetchall()

    uploaded_embedding = extract_face_embedding(image_path)
    if uploaded_embedding is None:
        return None  # No face detected

    for child in children:
        try:
            db_embedding = extract_face_embedding(child[3])
            if db_embedding is not None:
                similarity = np.dot(uploaded_embedding, db_embedding) / (
                    np.linalg.norm(uploaded_embedding) * np.linalg.norm(db_embedding)
                )

                if similarity > 0.6:  # Threshold for a match
                    conn.close()
                    return {
                        "match": {"name": child[1], "age": child[2], "image": f"/static/{os.path.basename(child[3])}"},
                        "confidence": round(similarity * 100, 2)
                    }
        except Exception as e:
            print(f"Error processing {child[3]}: {e}")

    conn.close()
    return None

# Homepage (Simple HTML Response)
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h2>Welcome to the Missing Children Recovery API</h2>
    <p>Upload an image to search for a missing child.</p>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">Upload</button>
    </form>
    """

# Upload Image & Search
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    match = find_match(filepath)

    if match:
        return JSONResponse(content={"message": "Match found", "match": match["match"], "confidence": match["confidence"]})
    else:
        raise HTTPException(status_code=404, detail="No match found")

# View Database of Missing Children
@app.get("/database")
async def database():
    conn = sqlite3.connect("children.db")
    c = conn.cursor()
    c.execute("SELECT name, age, image_path, last_seen FROM missing_children")
    children = [
        {"name": row[0], "age": row[1], "image": f"/static/{os.path.basename(row[2])}", "last_seen": row[3]}
        for row in c.fetchall()
    ]
    conn.close()
    
    return JSONResponse(content={"children": children})

# Run FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
