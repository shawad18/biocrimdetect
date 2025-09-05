import face_recognition
import pickle
import os

ENCODINGS_FILE = os.path.join(os.path.dirname(__file__), 'encodings.pkl')

def recognize_from_image(image_path):
    if not os.path.exists(ENCODINGS_FILE):
        return "No encodings file. Run train_model.py", None

    with open(ENCODINGS_FILE, 'rb') as f:
        data = pickle.load(f)

    unknown_img = face_recognition.load_image_file(image_path)
    unknown_encodings = face_recognition.face_encodings(unknown_img)

    if not unknown_encodings:
        return "No face detected", None

    unknown_encoding = unknown_encodings[0]
    results = face_recognition.compare_faces(data["encodings"], unknown_encoding)

    if True in results:
        index = results.index(True)
        return "Match Found", data["names"][index]
    else:
        return "No Match", None
