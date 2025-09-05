import cv2
import os

FINGERPRINT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads', 'fingerprint_images')

def match_fingerprint(uploaded_image_path):
    sift = cv2.SIFT_create()

    input_img = cv2.imread(uploaded_image_path, 0)
    kp1, des1 = sift.detectAndCompute(input_img, None)
    if des1 is None:
        return "No fingerprint features detected", None

    bf = cv2.BFMatcher()
    best_match = None
    highest_matches = 0

    for file in os.listdir(FINGERPRINT_DIR):
        stored_path = os.path.join(FINGERPRINT_DIR, file)
        db_img = cv2.imread(stored_path, 0)
        kp2, des2 = sift.detectAndCompute(db_img, None)
        if des2 is None:
            continue

        matches = bf.knnMatch(des1, des2, k=2)
        good_matches = []
        for m_n in matches:
            if len(m_n) == 2:
                m, n = m_n
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)

        if len(good_matches) > highest_matches:
            highest_matches = len(good_matches)
            best_match = os.path.splitext(file)[0]

    if best_match and highest_matches > 15:
        return "Match Found", best_match
    else:
        return "No Match", None
