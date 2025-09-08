import cv2
import os
import time
from threading import Thread
import numpy as np

class SimpleCameraDetection:
    def __init__(self):
        self.frame = None
        self.stopped = False
        self.face_locations = []
        self.detection_results = []
        self.last_detection_time = 0
        self.detection_interval = 0.5  # Process every 0.5 seconds
        
        # Load OpenCV's pre-trained face detection classifier
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Load known faces from uploads folder
        self.known_faces = self.load_known_faces()
    
    def load_known_faces(self):
        """Load known faces from the uploads/face_images directory"""
        known_faces = []
        uploads_dir = os.path.join('uploads', 'face_images')
        
        if os.path.exists(uploads_dir):
            for filename in os.listdir(uploads_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    filepath = os.path.join(uploads_dir, filename)
                    # Extract name from filename (remove extension)
                    name = os.path.splitext(filename)[0]
                    known_faces.append({
                        'name': name,
                        'image_path': filepath
                    })
        
        return known_faces
    
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
        
        # Set camera properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        while not self.stopped:
            ret, self.frame = cap.read()
            if not ret:
                self.stopped = True
                break
            
            # Process frame for face detection
            current_time = time.time()
            if current_time - self.last_detection_time > self.detection_interval:
                self.process_frame()
                self.last_detection_time = current_time
            
            time.sleep(0.03)  # ~30 FPS
        
        cap.release()
    
    def process_frame(self):
        """Process the current frame for face detection"""
        if self.frame is None:
            return
        
        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the frame
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        self.face_locations = []
        self.detection_results = []
        
        for (x, y, w, h) in faces:
            # Store face location
            self.face_locations.append((x, y, w, h))
            
            # For now, we'll just detect faces without recognition
            # In a real implementation, you could add template matching or other techniques
            self.detection_results.append({
                'location': (x, y, w, h),
                'name': 'Unknown Person',
                'confidence': 0.8,
                'timestamp': time.time()
            })
    
    def get_frame_with_detections(self):
        """Get the current frame with face detection boxes drawn"""
        if self.frame is None:
            return None
        
        frame_copy = self.frame.copy()
        
        # Draw rectangles around detected faces
        for (x, y, w, h) in self.face_locations:
            cv2.rectangle(frame_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Add label
            cv2.putText(frame_copy, 'Face Detected', (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame_copy
    
    def get_frame(self):
        """Return the current frame as JPEG bytes for streaming"""
        if self.frame is None:
            return None
        
        # Get frame with detections
        frame_with_detections = self.get_frame_with_detections()
        if frame_with_detections is None:
            return None
        
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame_with_detections)
        if ret:
            return buffer.tobytes()
        return None
    
    def get_raw_frame(self):
        """Return the current raw frame"""
        return self.frame
    
    def stop(self):
        """Indicate that the thread should be stopped"""
        self.stopped = True
    
    def get_detection_results(self):
        """Get the latest detection results"""
        return self.detection_results
    
    def is_running(self):
        """Check if the camera is still running"""
        return not self.stopped
    
    def get_face_count(self):
        """Get the number of faces currently detected"""
        return len(self.face_locations)

# Test function
if __name__ == "__main__":
    print("Starting simple camera detection...")
    detector = SimpleCameraDetection()
    detector.start()
    
    try:
        while detector.is_running():
            frame = detector.get_frame_with_detections()
            if frame is not None:
                cv2.imshow('Simple Face Detection', frame)
                
                # Print detection results
                results = detector.get_detection_results()
                if results:
                    print(f"Detected {len(results)} face(s)")
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nStopping camera detection...")
    
    finally:
        detector.stop()
        cv2.destroyAllWindows()
        print("Camera detection stopped.")