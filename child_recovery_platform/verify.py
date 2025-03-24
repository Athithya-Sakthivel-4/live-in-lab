import sqlite3
import cv2
import numpy as np

DB_PATH = "children.db"

def find_match(image_path):
    # Load uploaded image
    uploaded_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if uploaded_image is None:
        print("❌ Could not load uploaded image")
        return None

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Fetch all stored images
    c.execute("SELECT id, name, image_path FROM missing_children")
    children = c.fetchall()
    
    sift = cv2.SIFT_create()
    uploaded_kp, uploaded_des = sift.detectAndCompute(uploaded_image, None)

    if uploaded_des is None:
        print("❌ No keypoints found in the uploaded image")
        conn.close()
        return None

    bf = cv2.BFMatcher()

    for child in children:
        db_image_path = child[2]
        db_image = cv2.imread(db_image_path, cv2.IMREAD_GRAYSCALE)

        if db_image is None:
            continue

        db_kp, db_des = sift.detectAndCompute(db_image, None)

        if db_des is None:
            continue

        # Match keypoints
        matches = bf.knnMatch(uploaded_des, db_des, k=2)
        
        # Apply Lowe’s ratio test
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        # If enough good matches are found, we consider it a match
        if len(good_matches) > 10:
            conn.close()
            return child[1]

    conn.close()
    return None
