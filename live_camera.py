import cv2
import face_recognition
import pickle
import os

ENCODINGS_FILE = os.path.join('facial_recognition', 'encodings.pkl')

def load_encodings():
    if not os.path.exists(ENCODINGS_FILE):
        print('[ERROR] Encodings file not found. Run facial_recognition/train_model.py first.')
        return None, None
    with open(ENCODINGS_FILE, 'rb') as f:
        data = pickle.load(f)
    return data['encodings'], data['names']

def start_camera():
    known_encodings, known_names = load_encodings()
    if known_encodings is None:
        return

    cap = cv2.VideoCapture(0)
    print('[INFO] Starting webcam. Press Q to quit.')
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = 'Unknown'
            if True in matches:
                index = matches.index(True)
                name = known_names[index]
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)

        cv2.imshow('Live Camera - Press Q to Quit', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    start_camera()
