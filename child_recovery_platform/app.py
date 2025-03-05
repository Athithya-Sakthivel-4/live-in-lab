from flask import Flask, request, render_template, jsonify
import sqlite3
from deepface import DeepFace
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to find a match in the database
def find_match(image_path):
    conn = sqlite3.connect("children.db")
    c = conn.cursor()
    c.execute("SELECT id, name, age, image_path FROM missing_children")
    children = c.fetchall()

    for child in children:
        try:
            result = DeepFace.verify(image_path, child[3])
            if result["verified"]:
                conn.close()
                return f"✅ Match Found: {child[1]}, Age: {child[2]}"
        except:
            continue

    conn.close()
    return "❌ No match found in our database."

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# Upload Image & Find Match
@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return "No file part"
    
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"
    
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    match = find_match(filepath)
    return match

if __name__ == "__main__":
    app.run(debug=True)
