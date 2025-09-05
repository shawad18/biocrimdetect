# Biometric Crime Detection System (Demo)
This is a demo project for a Biometric Crime Detection System using **Facial Recognition** and **Fingerprint Matching**.
## What's included
- Flask web app for registering suspects (face + fingerprint)
- Face encoding and recognition using `face_recognition` (dlib)
- Fingerprint matching using OpenCV SIFT feature matching
- SQLite database for storing suspect records
- Live webcam face recognition script

## Setup (local)
1. Create a Python virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python database/init_db.py
   ```
4. Run the Flask app:
   ```bash
   python app.py
   ```
5. Register a suspect (Admin account is created by default: username=`admin`, password=`admin123`).
6. Use the Live Camera script after encoding faces:
   ```bash
   python facial_recognition/train_model.py
   python live_camera.py
   ```

## Notes
- `face_recognition` requires `dlib` and C++ build tools. Installing on some platforms may need extra steps.
- This project is a demo and must not be used in production without strong legal, ethical, and security considerations.
