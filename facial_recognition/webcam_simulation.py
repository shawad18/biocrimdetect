import cv2
import time
import random
import numpy as np
from threading import Thread
from datetime import datetime

class WebcamSimulation:
    """Real webcam integration with simulated face detection overlay"""
    
    def __init__(self):
        self.cap = None
        self.frame = None
        self.stopped = False
        self.face_locations = []
        self.face_names = []
        self.last_detection_time = 0
        self.detection_interval = 3.0  # Process every 3 seconds
        self.animation_frame = 0
        self.webcam_available = False
        self.known_names = ['John Doe', 'Jane Smith', 'Robert Johnson', 'Maria Garcia', 'David Wilson']
        
        # Try to initialize webcam
        self._init_webcam()
    
    def _init_webcam(self):
        """Initialize webcam connection"""
        try:
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                # Set camera properties
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
                
                # Test if we can read a frame
                ret, test_frame = self.cap.read()
                if ret:
                    self.webcam_available = True
                    print("Webcam initialized successfully")
                else:
                    self.cap.release()
                    self.cap = None
                    print("Webcam test failed")
            else:
                self.cap = None
                print("Could not open webcam")
        except Exception as e:
            print(f"Webcam initialization error: {e}")
            self.cap = None
    
    def start(self):
        """Start the webcam thread"""
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        """Main webcam loop with overlay effects"""
        while not self.stopped:
            if self.webcam_available and self.cap is not None:
                ret, frame = self.cap.read()
                if ret:
                    # Flip frame horizontally for mirror effect
                    frame = cv2.flip(frame, 1)
                    
                    # Add overlay effects
                    self.frame = self._add_overlay_effects(frame)
                    
                    # Simulate face detection
                    current_time = time.time()
                    if current_time - self.last_detection_time >= self.detection_interval:
                        self._simulate_face_detection(frame)
                        self.last_detection_time = current_time
                else:
                    # Webcam read failed, create fallback frame
                    self.frame = self._create_fallback_frame()
            else:
                # No webcam available, create fallback frame
                self.frame = self._create_fallback_frame()
            
            time.sleep(0.03)  # ~30 fps
            self.animation_frame += 1
    
    def _add_overlay_effects(self, frame):
        """Add professional overlay effects to webcam feed"""
        overlay_frame = frame.copy()
        
        # Add semi-transparent overlay
        overlay = np.zeros_like(frame)
        
        # Add corner brackets
        h, w = frame.shape[:2]
        bracket_size = 30
        bracket_thickness = 3
        
        corners = [
            (20, 20), (w-20, 20), (20, h-20), (w-20, h-20)
        ]
        
        for i, (x, y) in enumerate(corners):
            if i == 0:  # Top-left
                cv2.line(overlay, (x, y), (x + bracket_size, y), (0, 255, 136), bracket_thickness)
                cv2.line(overlay, (x, y), (x, y + bracket_size), (0, 255, 136), bracket_thickness)
            elif i == 1:  # Top-right
                cv2.line(overlay, (x, y), (x - bracket_size, y), (0, 255, 136), bracket_thickness)
                cv2.line(overlay, (x, y), (x, y + bracket_size), (0, 255, 136), bracket_thickness)
            elif i == 2:  # Bottom-left
                cv2.line(overlay, (x, y), (x + bracket_size, y), (0, 255, 136), bracket_thickness)
                cv2.line(overlay, (x, y), (x, y - bracket_size), (0, 255, 136), bracket_thickness)
            elif i == 3:  # Bottom-right
                cv2.line(overlay, (x, y), (x - bracket_size, y), (0, 255, 136), bracket_thickness)
                cv2.line(overlay, (x, y), (x, y - bracket_size), (0, 255, 136), bracket_thickness)
        
        # Add center crosshair
        center_x, center_y = w // 2, h // 2
        cv2.line(overlay, (center_x - 15, center_y), (center_x + 15, center_y), (0, 255, 136), 2)
        cv2.line(overlay, (center_x, center_y - 15), (center_x, center_y + 15), (0, 255, 136), 2)
        cv2.circle(overlay, (center_x, center_y), 40, (0, 255, 136), 2)
        
        # Add status bar
        cv2.rectangle(overlay, (0, 0), (w, 40), (0, 0, 0), -1)
        cv2.rectangle(overlay, (0, 0), (w, 40), (0, 255, 136), 2)
        
        # Add timestamp and status
        timestamp = datetime.now().strftime("%H:%M:%S")
        cv2.putText(overlay, f"LIVE CAMERA - {timestamp}", (10, 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 136), 2)
        cv2.putText(overlay, "DEMO MODE", (w - 120, 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # Blend overlay with frame
        result = cv2.addWeighted(overlay_frame, 0.8, overlay, 0.2, 0)
        
        return result
    
    def _simulate_face_detection(self, frame):
        """Simulate face detection on the webcam feed"""
        # Use OpenCV's built-in face detection for more realism
        try:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            self.face_locations = []
            self.face_names = []
            
            for (x, y, w, h) in faces:
                # Convert to face_recognition format (top, right, bottom, left)
                top, right, bottom, left = y, x + w, y + h, x
                self.face_locations.append((top, right, bottom, left))
                
                # Randomly assign names (20% chance of match)
                if random.random() < 0.2:
                    name = random.choice(self.known_names)
                    self.face_names.append(name)
                else:
                    self.face_names.append("Unknown")
                    
        except Exception as e:
            print(f"Face detection error: {e}")
            # Fallback to random detection
            self.face_locations = []
            self.face_names = []
    
    def _create_fallback_frame(self):
        """Create a fallback frame when webcam is not available"""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add gradient background
        for y in range(480):
            intensity = int(20 + (y / 480) * 30)
            frame[y, :] = [intensity, intensity, intensity + 10]
        
        # Add message
        cv2.putText(frame, "WEBCAM NOT AVAILABLE", (180, 220), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, "Using Simulation Mode", (220, 260), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Add animated elements
        pulse = int(128 + 127 * np.sin(self.animation_frame * 0.1))
        cv2.circle(frame, (320, 240), 50, (0, pulse, 0), 2)
        
        return frame
    
    def get_frame(self):
        """Return the current frame as JPEG bytes"""
        if self.frame is None:
            return None
        
        try:
            # Add face detection boxes
            display_frame = self.frame.copy()
            
            for i, (top, right, bottom, left) in enumerate(self.face_locations):
                name = self.face_names[i] if i < len(self.face_names) else "Unknown"
                
                # Draw face box with animation
                if name != "Unknown":
                    color = (0, 255, 0)  # Green for matches
                    label = f"MATCH: {name}"
                    confidence = random.randint(85, 98)
                else:
                    color = (0, 165, 255)  # Orange for unknown
                    label = "SCANNING..."
                    confidence = 0
                
                # Animated box thickness
                thickness = 2 + int(2 * np.sin(self.animation_frame * 0.2))
                cv2.rectangle(display_frame, (left, top), (right, bottom), color, thickness)
                
                # Label background
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_DUPLEX, 0.5, 1)[0]
                cv2.rectangle(display_frame, (left, bottom), (left + label_size[0] + 10, bottom + 25), color, -1)
                cv2.putText(display_frame, label, (left + 5, bottom + 18), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                
                if confidence > 0:
                    cv2.putText(display_frame, f"{confidence}%", (right - 40, top - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
            
            # Encode as JPEG
            ret, buffer = cv2.imencode('.jpg', display_frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if ret:
                return buffer.tobytes()
            else:
                return None
                
        except Exception as e:
            print(f"Frame encoding error: {e}")
            return None
    
    def stop(self):
        """Stop the webcam and cleanup"""
        self.stopped = True
        if self.cap is not None:
            self.cap.release()
    
    def get_recognition_results(self):
        """Return current recognition results"""
        results = []
        
        for i, (top, right, bottom, left) in enumerate(self.face_locations):
            name = self.face_names[i] if i < len(self.face_names) else "Unknown"
            
            results.append({
                'location': (top, right, bottom, left),
                'name': name,
                'match': name != "Unknown",
                'confidence': random.randint(85, 98) if name != "Unknown" else 0,
                'timestamp': time.time()
            })
        
        return results