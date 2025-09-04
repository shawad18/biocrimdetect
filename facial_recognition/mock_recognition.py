import os
import time
import random
import pickle
from threading import Thread

class MockFaceRecognition:
    """A mock implementation of face recognition for demonstration purposes
    when the actual face recognition libraries are not available."""
    
    def __init__(self):
        self.encodings_file = os.path.join('facial_recognition', 'encodings.pkl')
        self.known_names = self._load_names()
        self.frame = None
        self.stopped = False
        self.face_locations = []
        self.face_names = []
        self.last_detection_time = 0
        self.detection_interval = 1.0  # Process every 1 second
        self.mock_frame = self._create_mock_frame()
    
    def _load_names(self):
        """Load criminal names from database or use mock names if not available"""
        try:
            if os.path.exists(self.encodings_file):
                with open(self.encodings_file, 'rb') as f:
                    data = pickle.load(f)
                return data['names']
        except Exception as e:
            print(f"Error loading names: {str(e)}")
        
        # Return mock names if can't load from file
        return ["John Doe", "Jane Smith", "Robert Johnson", "Unknown"]
    
    def _create_mock_frame(self):
        """Create a mock frame with a gray background and text"""
        try:
            import cv2
            import numpy as np
            
            # Create a gray background
            frame = np.ones((480, 640, 3), dtype=np.uint8) * 200
            
            # Add text
            cv2.putText(frame, "MOCK CAMERA FEED", (150, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(frame, "Face recognition modules not available", (100, 280), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            return frame
        except ImportError:
            return None
    
    def start(self):
        """Start the thread to simulate video stream"""
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        """Simulate a video stream with random face detections"""
        while not self.stopped:
            # Simulate frame capture
            if self.mock_frame is not None:
                self.frame = self.mock_frame.copy()
            
            # Process face detection at intervals
            current_time = time.time()
            if current_time - self.last_detection_time >= self.detection_interval:
                self._simulate_face_detection()
                self.last_detection_time = current_time
            
            # Simulate camera frame rate
            time.sleep(0.03)  # ~30 fps
    
    def _simulate_face_detection(self):
        """Simulate face detection with random results"""
        # Clear previous detections
        self.face_locations = []
        self.face_names = []
        
        # 70% chance to detect a face
        if random.random() < 0.7:
            # Generate a random face location (top, right, bottom, left)
            top = random.randint(100, 200)
            right = random.randint(350, 450)
            bottom = random.randint(250, 350)
            left = random.randint(200, 300)
            
            self.face_locations.append((top, right, bottom, left))
            
            # 50% chance to recognize the face as someone in the database
            if random.random() < 0.5:
                name = random.choice(self.known_names[:-1])  # Exclude "Unknown"
            else:
                name = "Unknown"
                
            self.face_names.append(name)
    
    def get_frame(self):
        """Return the current frame with simulated face recognition results"""
        if self.frame is None:
            return None
        
        try:
            import cv2
            
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
                
                # Add a note that this is simulated
                cv2.putText(output_frame, "DEMO MODE", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Encode the frame in JPEG format
            ret, jpeg = cv2.imencode('.jpg', output_frame)
            return jpeg.tobytes()
        except Exception as e:
            print(f"Error in get_frame: {str(e)}")
            return None
    
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