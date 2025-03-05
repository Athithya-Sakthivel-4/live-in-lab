import sqlite3
import cv2
from deepface import DeepFace

def find_match(image_path):
    # Connect to the database
    conn = sqlite3.connect('children.db')
    c = conn.cursor()

    # Fetch all stored images
    c.execute("SELECT id, name, image_path FROM missing_children")
    children = c.fetchall()
    
    for child in children:
        db_image_path = child[2]
        
        try:
            # Perform face recognition
            result = DeepFace.verify(image_path, db_image_path, enforce_detection=False)
            
            if result["verified"]:
                print(f"✅ Match found: {child[1]}")
                conn.close()
                return child[1]
        except Exception as e:
            print(f"Error processing image {db_image_path}: {e}")
    
    conn.close()
    print("❌ No match found.")
    return None

# Run verification with an unknown child image
unknown_image = "database_images/unknown_child.png"  # Replace with the actual path
find_match(unknown_image)
