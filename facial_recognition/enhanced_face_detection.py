#!/usr/bin/env python3
"""
Enhanced Face Detection and Recognition System
Improved algorithm for real face detection and database matching
"""

import cv2
import os
import time
import numpy as np
from threading import Thread
import sqlite3
import mysql.connector
from datetime import datetime
import json

class EnhancedFaceDetection:
    def __init__(self):
        self.frame = None
        self.stopped = False
        self.face_locations = []
        self.detection_results = []
        self.last_detection_time = 0
        self.detection_interval = 0.3  # Process every 0.3 seconds for better responsiveness
        
        # Initialize face detection cascades
        self.init_face_detectors()
        
        # Load criminal database
        self.criminal_database = self.load_criminal_database()
        
        # Face quality thresholds
        self.min_face_size = (50, 50)
        self.max_face_size = (400, 400)
        self.quality_threshold = 0.7
        
        # Detection statistics
        self.total_detections = 0
        self.successful_matches = 0
        self.session_start = time.time()
        
    def init_face_detectors(self):
        """Initialize multiple face detection methods for better accuracy"""
        try:
            # Primary detector - Haar Cascade (frontal faces)
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            
            # Secondary detector - Profile faces
            self.profile_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_profileface.xml'
            )
            
            # Eye detector for face validation
            self.eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )
            
            print("✅ Face detectors initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing face detectors: {e}")
            
    def load_criminal_database(self):
        """Load criminal records from database for matching"""
        criminals = []
        
        try:
            # Try MySQL first
            from database.mysql_config import get_mysql_connection
            conn = get_mysql_connection()
            
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT id, full_name, age, gender, crime_type, 
                           description, image_path, date_added
                    FROM criminals 
                    WHERE image_path IS NOT NULL
                """)
                criminals = cursor.fetchall()
                cursor.close()
                conn.close()
                print(f"✅ Loaded {len(criminals)} criminal records from MySQL")
                
        except Exception as e:
            print(f"⚠️ MySQL connection failed: {e}")
            
            # Fallback to SQLite
            try:
                conn = sqlite3.connect('crime_detection.db')
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, full_name, age, gender, crime_type, 
                           description, image_path, date_added
                    FROM criminals 
                    WHERE image_path IS NOT NULL
                """)
                
                criminals = [dict(row) for row in cursor.fetchall()]
                cursor.close()
                conn.close()
                print(f"✅ Loaded {len(criminals)} criminal records from SQLite")
                
            except Exception as sqlite_e:
                print(f"❌ Database connection failed: {sqlite_e}")
                
        return criminals
    
    def start(self):
        """Start the face detection thread"""
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        """Main camera loop with enhanced error handling"""
        cap = None
        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries and not self.stopped:
            try:
                # Try different camera indices
                for camera_index in [0, 1, -1]:
                    cap = cv2.VideoCapture(camera_index)
                    if cap.isOpened():
                        print(f"✅ Camera {camera_index} opened successfully")
                        break
                    cap.release()
                    
                if not cap or not cap.isOpened():
                    print(f"❌ Failed to open camera (attempt {retry_count + 1})")
                    retry_count += 1
                    time.sleep(2)
                    continue
                
                # Configure camera for optimal performance
                self.configure_camera(cap)
                
                # Main capture loop
                consecutive_failures = 0
                max_consecutive_failures = 10
                
                while not self.stopped:
                    ret, frame = cap.read()
                    
                    if not ret:
                        consecutive_failures += 1
                        if consecutive_failures > max_consecutive_failures:
                            print("❌ Too many consecutive frame failures")
                            break
                        time.sleep(0.1)
                        continue
                    
                    consecutive_failures = 0
                    self.frame = frame
                    
                    # Process frame for face detection
                    current_time = time.time()
                    if current_time - self.last_detection_time > self.detection_interval:
                        self.process_frame_enhanced()
                        self.last_detection_time = current_time
                    
                    time.sleep(0.03)  # ~30 FPS
                
                break  # Exit retry loop if successful
                
            except Exception as e:
                print(f"❌ Camera error: {e}")
                retry_count += 1
                time.sleep(2)
                
            finally:
                if cap:
                    cap.release()
                    
        if retry_count >= max_retries:
            print("❌ Failed to initialize camera after multiple attempts")
            self.stopped = True
    
    def configure_camera(self, cap):
        """Configure camera settings for optimal performance"""
        try:
            # Set resolution
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            # Set frame rate
            cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Auto exposure and focus
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
            cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            
            print("✅ Camera configured successfully")
            
        except Exception as e:
            print(f"⚠️ Camera configuration warning: {e}")
    
    def process_frame_enhanced(self):
        """Enhanced frame processing with multiple detection methods"""
        if self.frame is None:
            return
        
        # Convert to grayscale for detection
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        
        # Apply histogram equalization for better contrast
        gray = cv2.equalizeHist(gray)
        
        # Detect faces using multiple methods
        faces = self.detect_faces_multi_method(gray)
        
        # Validate and filter faces
        validated_faces = self.validate_faces(gray, faces)
        
        # Match faces against criminal database
        self.match_faces_to_database(validated_faces)
        
        self.total_detections += len(validated_faces)
    
    def detect_faces_multi_method(self, gray):
        """Use multiple detection methods for better accuracy"""
        all_faces = []
        
        # Method 1: Frontal face detection
        frontal_faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=self.min_face_size,
            maxSize=self.max_face_size,
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Method 2: Profile face detection
        profile_faces = self.profile_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=self.min_face_size,
            maxSize=self.max_face_size
        )
        
        # Combine and remove duplicates
        all_faces = list(frontal_faces) + list(profile_faces)
        
        # Remove overlapping detections
        filtered_faces = self.remove_overlapping_faces(all_faces)
        
        return filtered_faces
    
    def remove_overlapping_faces(self, faces, overlap_threshold=0.3):
        """Remove overlapping face detections"""
        if len(faces) <= 1:
            return faces
        
        # Convert to list of rectangles
        rects = [(x, y, x + w, y + h) for (x, y, w, h) in faces]
        
        # Calculate areas
        areas = [(x2 - x1) * (y2 - y1) for (x1, y1, x2, y2) in rects]
        
        # Sort by area (largest first)
        indices = sorted(range(len(areas)), key=lambda i: areas[i], reverse=True)
        
        keep = []
        for i in indices:
            keep_this = True
            for j in keep:
                if self.calculate_overlap(rects[i], rects[j]) > overlap_threshold:
                    keep_this = False
                    break
            if keep_this:
                keep.append(i)
        
        return [faces[i] for i in keep]
    
    def calculate_overlap(self, rect1, rect2):
        """Calculate overlap ratio between two rectangles"""
        x1, y1, x2, y2 = rect1
        x3, y3, x4, y4 = rect2
        
        # Calculate intersection
        xi1, yi1 = max(x1, x3), max(y1, y3)
        xi2, yi2 = min(x2, x4), min(y2, y4)
        
        if xi2 <= xi1 or yi2 <= yi1:
            return 0
        
        intersection = (xi2 - xi1) * (yi2 - yi1)
        area1 = (x2 - x1) * (y2 - y1)
        area2 = (x4 - x3) * (y4 - y3)
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0
    
    def validate_faces(self, gray, faces):
        """Validate detected faces using additional criteria"""
        validated = []
        
        for (x, y, w, h) in faces:
            # Extract face region
            face_roi = gray[y:y+h, x:x+w]
            
            # Quality checks
            quality_score = self.calculate_face_quality(face_roi)
            
            if quality_score >= self.quality_threshold:
                # Check for eyes to confirm it's a real face
                eyes = self.eye_cascade.detectMultiScale(face_roi, 1.1, 5)
                
                if len(eyes) >= 1:  # At least one eye detected
                    validated.append({
                        'location': (x, y, w, h),
                        'quality': quality_score,
                        'eyes_detected': len(eyes),
                        'roi': face_roi
                    })
        
        return validated
    
    def calculate_face_quality(self, face_roi):
        """Calculate face quality score based on various factors"""
        if face_roi.size == 0:
            return 0
        
        # Factor 1: Sharpness (Laplacian variance)
        laplacian_var = cv2.Laplacian(face_roi, cv2.CV_64F).var()
        sharpness_score = min(laplacian_var / 500.0, 1.0)
        
        # Factor 2: Contrast
        contrast = face_roi.std()
        contrast_score = min(contrast / 50.0, 1.0)
        
        # Factor 3: Size appropriateness
        h, w = face_roi.shape
        size_score = min(min(h, w) / 80.0, 1.0)
        
        # Combined quality score
        quality = (sharpness_score * 0.4 + contrast_score * 0.3 + size_score * 0.3)
        
        return quality
    
    def match_faces_to_database(self, validated_faces):
        """Match detected faces against criminal database"""
        self.face_locations = []
        self.detection_results = []
        
        for face_data in validated_faces:
            x, y, w, h = face_data['location']
            self.face_locations.append((x, y, w, h))
            
            # Perform template matching against criminal database
            match_result = self.template_match_criminal(face_data['roi'])
            
            result = {
                'location': (x, y, w, h),
                'quality': face_data['quality'],
                'eyes_detected': face_data['eyes_detected'],
                'match_result': match_result,
                'timestamp': time.time(),
                'confidence': match_result.get('confidence', 0)
            }
            
            self.detection_results.append(result)
            
            if match_result.get('match_found', False):
                self.successful_matches += 1
    
    def template_match_criminal(self, face_roi):
        """Match face against criminal database using template matching"""
        best_match = {
            'match_found': False,
            'criminal_id': None,
            'criminal_name': 'Unknown',
            'confidence': 0,
            'crime_type': None
        }
        
        if not self.criminal_database:
            return best_match
        
        try:
            # Resize face for consistent comparison
            face_resized = cv2.resize(face_roi, (100, 100))
            
            for criminal in self.criminal_database:
                if not criminal.get('image_path'):
                    continue
                
                # Load criminal image
                criminal_img_path = criminal['image_path']
                if not os.path.exists(criminal_img_path):
                    continue
                
                criminal_img = cv2.imread(criminal_img_path, cv2.IMREAD_GRAYSCALE)
                if criminal_img is None:
                    continue
                
                # Detect face in criminal image
                criminal_faces = self.face_cascade.detectMultiScale(criminal_img, 1.1, 5)
                
                if len(criminal_faces) > 0:
                    # Use the largest face
                    (cx, cy, cw, ch) = max(criminal_faces, key=lambda f: f[2] * f[3])
                    criminal_face = criminal_img[cy:cy+ch, cx:cx+cw]
                    criminal_face_resized = cv2.resize(criminal_face, (100, 100))
                    
                    # Calculate similarity using template matching
                    result = cv2.matchTemplate(face_resized, criminal_face_resized, cv2.TM_CCOEFF_NORMED)
                    confidence = float(result.max())
                    
                    # Update best match if this is better
                    if confidence > best_match['confidence'] and confidence > 0.6:  # Threshold for match
                        best_match = {
                            'match_found': True,
                            'criminal_id': criminal['id'],
                            'criminal_name': criminal['full_name'],
                            'confidence': confidence,
                            'crime_type': criminal.get('crime_type', 'Unknown'),
                            'age': criminal.get('age'),
                            'gender': criminal.get('gender')
                        }
        
        except Exception as e:
            print(f"❌ Error in template matching: {e}")
        
        return best_match
    
    def get_frame_with_detections(self):
        """Get frame with enhanced detection visualization"""
        if self.frame is None:
            return None
        
        frame_copy = self.frame.copy()
        
        # Draw detection results
        for result in self.detection_results:
            x, y, w, h = result['location']
            match_result = result['match_result']
            
            # Choose color based on match result
            if match_result['match_found']:
                color = (0, 0, 255)  # Red for criminal match
                label = f"CRIMINAL: {match_result['criminal_name']}"
                confidence_text = f"Confidence: {match_result['confidence']:.2f}"
            else:
                color = (0, 255, 0)  # Green for unknown person
                label = "Unknown Person"
                confidence_text = f"Quality: {result['quality']:.2f}"
            
            # Draw rectangle
            cv2.rectangle(frame_copy, (x, y), (x + w, y + h), color, 2)
            
            # Draw label background
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            cv2.rectangle(frame_copy, (x, y - 30), (x + label_size[0], y), color, -1)
            
            # Draw label text
            cv2.putText(frame_copy, label, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Draw confidence/quality
            cv2.putText(frame_copy, confidence_text, (x, y + h + 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Draw statistics
        stats_text = f"Detections: {self.total_detections} | Matches: {self.successful_matches}"
        cv2.putText(frame_copy, stats_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame_copy
    
    def get_frame(self):
        """Return frame as JPEG bytes for streaming"""
        frame_with_detections = self.get_frame_with_detections()
        if frame_with_detections is None:
            return None
        
        ret, buffer = cv2.imencode('.jpg', frame_with_detections)
        if ret:
            return buffer.tobytes()
        return None
    
    def get_detection_results(self):
        """Get current detection results"""
        return self.detection_results
    
    def get_statistics(self):
        """Get detection statistics"""
        session_duration = time.time() - self.session_start
        return {
            'total_detections': self.total_detections,
            'successful_matches': self.successful_matches,
            'session_duration': session_duration,
            'detection_rate': self.total_detections / max(session_duration / 60, 1),  # per minute
            'match_rate': self.successful_matches / max(self.total_detections, 1) * 100  # percentage
        }
    
    def stop(self):
        """Stop the detection system"""
        self.stopped = True
    
    def is_running(self):
        """Check if system is running"""
        return not self.stopped

# Test function
if __name__ == "__main__":
    print("🚀 Starting Enhanced Face Detection System...")
    detector = EnhancedFaceDetection()
    detector.start()
    
    try:
        while detector.is_running():
            frame = detector.get_frame_with_detections()
            if frame is not None:
                cv2.imshow('Enhanced Face Detection', frame)
                
                # Print statistics every 5 seconds
                if int(time.time()) % 5 == 0:
                    stats = detector.get_statistics()
                    print(f"📊 Stats: {stats['total_detections']} detections, "
                          f"{stats['successful_matches']} matches, "
                          f"{stats['match_rate']:.1f}% match rate")
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n⏹️ Stopping Enhanced Face Detection...")
    
    finally:
        detector.stop()
        cv2.destroyAllWindows()
        print("✅ Enhanced Face Detection stopped.")