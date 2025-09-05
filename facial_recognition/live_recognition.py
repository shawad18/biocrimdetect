import cv2
import face_recognition
import pickle
import os
import time
from threading import Thread

class LiveFaceRecognition:
    def __init__(self):
        self.encodings_file = os.path.join('facial_recognition', 'encodings.pkl')
        self.known_encodings = None
        self.known_names = None
        self.load_encodings()
        self.frame = None
        self.stopped = False
        self.face_locations = []
        self.face_names = []
        self.last_detection_time = 0
        self.detection_interval = 0.5  # Process every 0.5 seconds
    
    def load_encodings(self):
        """Load the known face encodings and names from the pickle file"""
        if not os.path.exists(self.encodings_file):
            print('[ERROR] Encodings file not found. Run facial_recognition/train_model.py first.')
            return False
        
        with open(self.encodings_file, 'rb') as f:
            data = pickle.load(f)
        
        self.known_encodings = data['encodings']
        self.known_names = data['names']
        return True
    
    def start(self):
        """Start the thread to read frames from the video stream"""
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        """Keep looping infinitely until the thread is stopped"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            self.stopped = True
            return
        
        while not self.stopped:
            ret, self.frame = cap.read()
            if not ret:
                self.stopped = True
                break
            
            # Process face detection at intervals to reduce CPU usage
            current_time = time.time()
            if current_time - self.last_detection_time >= self.detection_interval:
                self.process_frame()
                self.last_detection_time = current_time
        
        cap.release()
    
    def process_frame(self):
        """Process the current frame for face recognition"""
        if self.frame is None or self.known_encodings is None:
            return
        
        # Convert the image from BGR color (OpenCV) to RGB color (face_recognition)
        rgb_frame = self.frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame
        self.face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, self.face_locations)
        
        self.face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
            name = "Unknown"
            
            # If a match was found in known_face_encodings, use the first one
            if True in matches:
                index = matches.index(True)
                name = self.known_names[index]
            
            self.face_names.append(name)
    
    def get_frame(self):
        """Return the current frame with face recognition results"""
        if self.frame is None:
            return None
        
        # Draw the results on a copy of the frame
        output_frame = self.frame.copy()
        
        # Display the results
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Draw a box around the face
            cv2.rectangle(output_frame, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # Draw a label with a name below the face
            cv2.rectangle(output_frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(output_frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)
        
        # Encode the frame in JPEG format
        ret, jpeg = cv2.imencode('.jpg', output_frame)
        return jpeg.tobytes()
    
    def stop(self):
        """Indicate that the thread should be stopped"""
        self.stopped = True
    
    def get_recognition_results(self):
        """Return the current recognition results"""
        results = []
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            results.append({
                'name': name,
                'location': (top, right, bottom, left),
                'match': name != "Unknown"
            })
        return results