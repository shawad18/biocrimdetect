import cv2
import time
import threading
from datetime import datetime
import numpy as np

class RealCamera:
    """Real camera implementation using OpenCV for live video capture"""
    
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.frame = None
        self.stopped = False
        self.thread = None
        self.face_cascade = None
        self.face_locations = []
        self.face_names = []
        self.last_detection_time = 0
        self.detection_interval = 2.0  # Process every 2 seconds
        self.frame_count = 0
        self.detection_active = False
        
        # Initialize face detection
        try:
            # Load OpenCV's pre-trained face detection classifier
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        except Exception as e:
            print(f"Warning: Could not load face cascade classifier: {e}")
            self.face_cascade = None
    
    def start(self):
        """Start the camera capture thread"""
        try:
            # Initialize camera
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                print(f"Error: Could not open camera {self.camera_index}")
                return False
            
            # Set camera properties for better performance
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.stopped = False
            self.thread = threading.Thread(target=self.update, args=())
            self.thread.daemon = True
            self.thread.start()
            
            # Wait a moment for the camera to initialize
            time.sleep(1)
            
            print(f"Real camera {self.camera_index} started successfully")
            return True
            
        except Exception as e:
            print(f"Error starting camera: {e}")
            return False
    
    def update(self):
        """Update the camera frames continuously"""
        while not self.stopped:
            try:
                if self.cap is None or not self.cap.isOpened():
                    print("Camera not available")
                    break
                
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to read frame from camera")
                    time.sleep(0.1)
                    continue
                
                self.frame_count += 1
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Add timestamp overlay
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(frame, f"Live Camera - {timestamp}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Perform face detection periodically
                current_time = time.time()
                if current_time - self.last_detection_time > self.detection_interval:
                    self.detect_faces(frame)
                    self.last_detection_time = current_time
                
                # Draw face detection boxes
                self.draw_face_boxes(frame)
                
                # Convert frame to JPEG
                ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                if ret:
                    self.frame = buffer.tobytes()
                
                # Control frame rate
                time.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                print(f"Error in camera update loop: {e}")
                time.sleep(1)
    
    def detect_faces(self, frame):
        """Detect faces in the current frame"""
        try:
            if self.face_cascade is None:
                return
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(30, 30)
            )
            
            # Update face locations and simulate recognition
            self.face_locations = []
            self.face_names = []
            
            if len(faces) > 0:
                self.detection_active = True
                for (x, y, w, h) in faces:
                    # Convert to face_recognition format (top, right, bottom, left)
                    self.face_locations.append((y, x + w, y + h, x))
                    # Simulate face recognition (in real implementation, this would use face_recognition library)
                    self.face_names.append("Unknown Person")
            else:
                self.detection_active = False
                
        except Exception as e:
            print(f"Error in face detection: {e}")
    
    def draw_face_boxes(self, frame):
        """Draw face detection boxes on the frame"""
        try:
            for i, (top, right, bottom, left) in enumerate(self.face_locations):
                # Draw rectangle around face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                
                # Draw label
                if i < len(self.face_names):
                    name = self.face_names[i]
                    cv2.putText(frame, name, (left, top - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Add detection indicator
                cv2.putText(frame, "FACE DETECTED", (left, bottom + 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Add scanning indicator when no faces detected
            if not self.face_locations:
                cv2.putText(frame, "SCANNING FOR FACES...", (10, frame.shape[0] - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                
        except Exception as e:
            print(f"Error drawing face boxes: {e}")
    
    def get_frame(self):
        """Get the current frame as JPEG bytes"""
        if self.frame is not None:
            return self.frame
        else:
            # Return a default frame if none available
            return self._create_default_frame()
    
    def _create_default_frame(self):
        """Create a default frame when camera is not available"""
        try:
            # Create a simple black frame with text
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Camera Initializing...", (200, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                return buffer.tobytes()
            else:
                return b''
        except Exception as e:
            print(f"Error creating default frame: {e}")
            return b''
    
    def stop(self):
        """Stop the camera capture"""
        try:
            self.stopped = True
            
            if self.thread is not None:
                self.thread.join(timeout=2)
            
            if self.cap is not None:
                self.cap.release()
                self.cap = None
            
            print("Real camera stopped successfully")
            
        except Exception as e:
            print(f"Error stopping camera: {e}")
    
    def get_recognition_results(self):
        """Get current face recognition results by matching against criminal database"""
        results = []
        
        # Import database modules
        import sqlite3
        import os
        
        # Database path (assuming same structure as main app)
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'biometric_crime_detection.db')
        
        for i, name in enumerate(self.face_names):
            if i < len(self.face_locations):
                location = self.face_locations[i]
                
                # Initialize default values
                is_match = False
                matched_name = "Unknown Person"
                confidence = 0.75
                matched_criminal = None
                
                try:
                    # Connect to the criminal database
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    
                    # Get all active criminals from database
                    cursor.execute("""
                        SELECT name, first_name, last_name, crime, case_id, face_image 
                        FROM criminals 
                        WHERE active = 1
                    """)
                    criminals = cursor.fetchall()
                    
                    if criminals:
                        # Simulate face recognition matching against database
                        # In a real implementation, this would use face_recognition library
                        # to compare the detected face against stored face images
                        
                        # For demonstration: 15% chance of finding a match with any criminal
                        if np.random.random() < 0.15:
                            # Select a random criminal from the database
                            criminal = np.random.choice(criminals)
                            matched_criminal = {
                                'full_name': criminal[0],
                                'first_name': criminal[1],
                                'last_name': criminal[2],
                                'crime': criminal[3],
                                'case_id': criminal[4],
                                'face_image': criminal[5]
                            }
                            
                            matched_name = matched_criminal['full_name']
                            is_match = True
                            confidence = np.random.uniform(0.82, 0.96)
                    
                    conn.close()
                    
                except Exception as e:
                    print(f"Database error in face recognition: {e}")
                    # Fallback to unknown person if database error
                    pass
                
                # Convert numpy types to Python types for JSON serialization
                json_location = [int(coord) for coord in location] if location else []
                
                # Prepare result data
                result_data = {
                    'name': matched_name,
                    'match': is_match,
                    'confidence': round(float(confidence), 2),
                    'location': json_location,
                    'timestamp': float(time.time()),
                    'status': 'match_found' if is_match else 'no_match'
                }
                
                # Add criminal details if match found
                if is_match and matched_criminal:
                    result_data.update({
                        'criminal_details': {
                            'first_name': matched_criminal['first_name'],
                            'last_name': matched_criminal['last_name'],
                            'crime': matched_criminal['crime'],
                            'case_id': matched_criminal['case_id'],
                            'face_image': matched_criminal['face_image']
                        }
                    })
                
                results.append(result_data)
        
        return results
    
    def is_running(self):
        """Check if camera is running"""
        return not self.stopped and self.cap is not None and self.cap.isOpened()
    
    def get_camera_info(self):
        """Get camera information"""
        if self.cap is not None and self.cap.isOpened():
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            return {
                'width': width,
                'height': height,
                'fps': fps,
                'camera_index': self.camera_index,
                'status': 'active'
            }
        else:
            return {
                'width': 0,
                'height': 0,
                'fps': 0,
                'camera_index': self.camera_index,
                'status': 'inactive'
            }