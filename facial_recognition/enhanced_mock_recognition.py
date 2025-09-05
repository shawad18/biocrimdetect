import os
import time
import random
import pickle
import math
from threading import Thread
from datetime import datetime

class EnhancedMockFaceRecognition:
    """Enhanced mock implementation with realistic camera simulation and animations"""
    
    def __init__(self):
        self.encodings_file = os.path.join('facial_recognition', 'encodings.pkl')
        self.known_names = self._load_names()
        self.frame = None
        self.stopped = False
        self.face_locations = []
        self.face_names = []
        self.last_detection_time = 0
        self.detection_interval = 2.0  # Process every 2 seconds
        self.animation_frame = 0
        self.scan_line_pos = 0
        self.mock_frame = self._create_enhanced_mock_frame()
        self.detection_active = False
        self.last_scan_time = 0
        
    def _load_names(self):
        """Load criminal names from database or use mock names if not available"""
        try:
            if os.path.exists(self.encodings_file):
                with open(self.encodings_file, 'rb') as f:
                    data = pickle.load(f)
                return data['names']
        except Exception as e:
            print(f"Error loading names: {str(e)}")
        
        # Return mock criminal names
        return ['John Doe', 'Jane Smith', 'Robert Johnson', 'Maria Garcia', 'David Wilson']
    
    def _create_enhanced_mock_frame(self):
        """Create an enhanced mock frame with professional camera simulation"""
        try:
            import cv2
            import numpy as np
            
            # Create a dark background with gradient
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            
            # Add gradient background
            for y in range(480):
                intensity = int(30 + (y / 480) * 20)
                frame[y, :] = [intensity, intensity, intensity + 5]
            
            # Add grid pattern for camera realism
            for i in range(0, 640, 40):
                cv2.line(frame, (i, 0), (i, 480), (40, 40, 40), 1)
            for i in range(0, 480, 30):
                cv2.line(frame, (0, i), (640, i), (40, 40, 40), 1)
            
            # Add camera info overlay
            cv2.rectangle(frame, (10, 10), (630, 60), (0, 0, 0), -1)
            cv2.rectangle(frame, (10, 10), (630, 60), (0, 255, 136), 2)
            
            # Camera status text
            cv2.putText(frame, "BIOMETRIC SURVEILLANCE SYSTEM", (20, 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 136), 2)
            cv2.putText(frame, "STATUS: DEMO MODE - FACE RECOGNITION OFFLINE", (20, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
            
            # Add timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, timestamp, (450, 470), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            # Add center crosshair
            center_x, center_y = 320, 240
            cv2.line(frame, (center_x - 20, center_y), (center_x + 20, center_y), (0, 255, 136), 2)
            cv2.line(frame, (center_x, center_y - 20), (center_x, center_y + 20), (0, 255, 136), 2)
            cv2.circle(frame, (center_x, center_y), 50, (0, 255, 136), 2)
            
            # Add corner markers
            corners = [(50, 50), (590, 50), (50, 430), (590, 430)]
            for corner in corners:
                cv2.line(frame, (corner[0] - 10, corner[1]), (corner[0] + 10, corner[1]), (0, 255, 136), 2)
                cv2.line(frame, (corner[0], corner[1] - 10), (corner[0], corner[1] + 10), (0, 255, 136), 2)
            
            # Add main message
            cv2.putText(frame, "DEMO CAMERA SIMULATION", (180, 200), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            cv2.putText(frame, "Simulating Real-Time Face Detection", (160, 230), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            
            # Add instruction text
            cv2.putText(frame, "Click 'Capture & Identify' to simulate detection", (140, 350), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 200, 255), 1)
            cv2.putText(frame, "System will randomly detect mock suspects", (160, 370), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 200, 255), 1)
            
            return frame
        except ImportError:
            return None
    
    def start(self):
        """Start the thread to simulate video stream"""
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        """Simulate a video stream with animated elements"""
        while not self.stopped:
            if self.mock_frame is not None:
                self.frame = self.mock_frame.copy()
                
                # Add animated elements
                self._add_animations()
                
                # Process face detection at intervals
                current_time = time.time()
                if current_time - self.last_detection_time >= self.detection_interval:
                    self._simulate_face_detection()
                    self.last_detection_time = current_time
                
                # Add scanning animation
                if self.detection_active:
                    self._add_scanning_effect()
            
            # Simulate camera frame rate
            time.sleep(0.03)  # ~30 fps
            self.animation_frame += 1
    
    def _add_animations(self):
        """Add animated elements to the frame"""
        try:
            import cv2
            import numpy as np
            
            # Pulsing corner indicators
            pulse = int(128 + 127 * math.sin(self.animation_frame * 0.1))
            corners = [(20, 20), (620, 20), (20, 460), (620, 460)]
            for corner in corners:
                cv2.circle(self.frame, corner, 5, (0, pulse, 0), -1)
            
            # Moving scan line
            scan_y = int(100 + 280 * (0.5 + 0.5 * math.sin(self.animation_frame * 0.05)))
            cv2.line(self.frame, (100, scan_y), (540, scan_y), (0, 255, 136), 1)
            
            # Blinking status indicator
            if self.animation_frame % 60 < 30:  # Blink every 2 seconds
                cv2.circle(self.frame, (600, 30), 8, (0, 255, 0), -1)
                cv2.putText(self.frame, "ACTIVE", (550, 35), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
            
        except ImportError:
            pass
    
    def _add_scanning_effect(self):
        """Add scanning effect when detection is active"""
        try:
            import cv2
            import numpy as np
            
            # Scanning overlay
            overlay = self.frame.copy()
            cv2.rectangle(overlay, (0, 0), (640, 480), (0, 255, 136), 3)
            cv2.putText(overlay, "SCANNING...", (250, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 136), 2)
            
            # Blend with original frame
            alpha = 0.3 + 0.2 * math.sin(self.animation_frame * 0.3)
            self.frame = cv2.addWeighted(self.frame, 1 - alpha, overlay, alpha, 0)
            
        except ImportError:
            pass
    
    def _simulate_face_detection(self):
        """Simulate face detection with random results"""
        # Clear previous detections
        self.face_locations = []
        self.face_names = []
        
        # Randomly decide if faces are detected (70% chance)
        if random.random() < 0.7:
            num_faces = random.randint(1, 2)  # 1-2 faces
            
            for i in range(num_faces):
                # Generate random face location
                top = random.randint(100, 300)
                left = random.randint(100, 400)
                bottom = top + random.randint(80, 120)
                right = left + random.randint(80, 120)
                
                self.face_locations.append((top, right, bottom, left))
                
                # Randomly assign a name (30% chance of match)
                if random.random() < 0.3 and self.known_names:
                    name = random.choice(self.known_names)
                    self.face_names.append(name)
                else:
                    self.face_names.append("Unknown")
            
            # Activate scanning effect
            self.detection_active = True
            self.last_scan_time = time.time()
        else:
            self.detection_active = False
    
    def get_frame(self):
        """Return the current frame as JPEG bytes"""
        if self.frame is None:
            return None
        
        try:
            import cv2
            
            # Add face detection boxes if any
            display_frame = self.frame.copy()
            
            for i, (top, right, bottom, left) in enumerate(self.face_locations):
                name = self.face_names[i] if i < len(self.face_names) else "Unknown"
                
                # Draw face box
                if name != "Unknown":
                    color = (0, 255, 0)  # Green for known faces
                    label = f"MATCH: {name}"
                else:
                    color = (0, 165, 255)  # Orange for unknown faces
                    label = "UNKNOWN PERSON"
                
                cv2.rectangle(display_frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(display_frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                cv2.putText(display_frame, label, (left + 6, bottom - 6), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)
            
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', display_frame)
            if ret:
                return buffer.tobytes()
            else:
                return None
                
        except ImportError:
            return None
    
    def stop(self):
        """Stop the video stream"""
        self.stopped = True
    
    def get_recognition_results(self):
        """Return current recognition results"""
        results = []
        
        for i, (top, right, bottom, left) in enumerate(self.face_locations):
            name = self.face_names[i] if i < len(self.face_names) else "Unknown"
            
            results.append({
                'location': (top, right, bottom, left),
                'name': name,
                'match': name != "Unknown",
                'confidence': random.randint(75, 95) if name != "Unknown" else 0,
                'timestamp': time.time()
            })
        
        return results