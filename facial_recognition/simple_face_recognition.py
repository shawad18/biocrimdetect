import cv2
import numpy as np
import os
import pickle
from datetime import datetime

class SimpleFaceRecognition:
    """A simplified face recognition system using OpenCV instead of dlib"""
    
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.encodings_file = os.path.join('facial_recognition', 'encodings.pkl')
        self.known_faces = self._load_known_faces()
        
    def _load_known_faces(self):
        """Load known faces from encodings file or create empty dict"""
        if os.path.exists(self.encodings_file):
            try:
                with open(self.encodings_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading encodings: {e}")
                return {'encodings': [], 'names': []}
        return {'encodings': [], 'names': []}
    
    def detect_faces(self, image):
        """Detect faces in an image using OpenCV"""
        if isinstance(image, str):
            # If image is a file path, load it
            image = cv2.imread(image)
        
        if image is None:
            return []
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        face_locations = []
        for (x, y, w, h) in faces:
            # Convert to face_recognition format (top, right, bottom, left)
            face_locations.append((y, x + w, y + h, x))
        
        return face_locations
    
    def extract_face_encoding(self, image, face_location):
        """Extract a simple face encoding using histogram features"""
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        
        if face_image.size == 0:
            return None
        
        # Resize face to standard size
        face_image = cv2.resize(face_image, (100, 100))
        
        # Convert to grayscale and calculate histogram
        gray_face = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray_face], [0], None, [256], [0, 256])
        
        # Normalize histogram
        hist = hist.flatten()
        hist = hist / (hist.sum() + 1e-7)
        
        return hist
    
    def compare_faces(self, known_encodings, face_encoding, tolerance=0.6):
        """Compare face encodings using histogram correlation"""
        if face_encoding is None:
            return [False] * len(known_encodings)
        
        matches = []
        for known_encoding in known_encodings:
            if known_encoding is None:
                matches.append(False)
                continue
            
            # Calculate correlation coefficient
            correlation = cv2.compareHist(known_encoding.astype(np.float32), 
                                        face_encoding.astype(np.float32), 
                                        cv2.HISTCMP_CORREL)
            
            matches.append(correlation > tolerance)
        
        return matches
    
    def recognize_from_image(self, image_path):
        """Recognize faces from an image file"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return False, "Could not load image"
            
            face_locations = self.detect_faces(image)
            
            if not face_locations:
                return False, "No faces detected"
            
            # Process first face found
            face_location = face_locations[0]
            face_encoding = self.extract_face_encoding(image, face_location)
            
            if face_encoding is None:
                return False, "Could not extract face features"
            
            # Compare with known faces
            if self.known_faces['encodings']:
                matches = self.compare_faces(self.known_faces['encodings'], face_encoding)
                
                if any(matches):
                    match_index = matches.index(True)
                    name = self.known_faces['names'][match_index]
                    return True, name
            
            return False, "No match found"
            
        except Exception as e:
            return False, f"Error during recognition: {str(e)}"
    
    def add_known_face(self, image_path, name):
        """Add a new face to the known faces database"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return False, "Could not load image"
            
            face_locations = self.detect_faces(image)
            
            if not face_locations:
                return False, "No faces detected in image"
            
            # Use first face found
            face_location = face_locations[0]
            face_encoding = self.extract_face_encoding(image, face_location)
            
            if face_encoding is None:
                return False, "Could not extract face features"
            
            # Add to known faces
            self.known_faces['encodings'].append(face_encoding)
            self.known_faces['names'].append(name)
            
            # Save to file
            self._save_known_faces()
            
            return True, f"Face added for {name}"
            
        except Exception as e:
            return False, f"Error adding face: {str(e)}"
    
    def _save_known_faces(self):
        """Save known faces to encodings file"""
        try:
            os.makedirs(os.path.dirname(self.encodings_file), exist_ok=True)
            with open(self.encodings_file, 'wb') as f:
                pickle.dump(self.known_faces, f)
        except Exception as e:
            print(f"Error saving encodings: {e}")

# Create a global instance
simple_face_recognition = SimpleFaceRecognition()

# Functions to maintain compatibility with existing code
def recognize_from_image(image_path):
    """Recognize faces from image - compatibility function"""
    return simple_face_recognition.recognize_from_image(image_path)

def add_known_face(image_path, name):
    """Add known face - compatibility function"""
    return simple_face_recognition.add_known_face(image_path, name)