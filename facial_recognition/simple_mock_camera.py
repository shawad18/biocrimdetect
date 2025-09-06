import os
import time
import random
import base64
from io import BytesIO
from threading import Thread
from datetime import datetime

class SimpleMockCamera:
    """Simple mock camera that works without OpenCV dependencies"""
    
    def __init__(self):
        self.known_names = ['John Doe', 'Jane Smith', 'Robert Johnson', 'Maria Garcia', 'David Wilson']
        self.frame = None
        self.stopped = False
        self.face_locations = []
        self.face_names = []
        self.last_detection_time = 0
        self.detection_interval = 3.0  # Process every 3 seconds
        self.frame_count = 0
        self.detection_active = False
        
    def _create_simple_frame(self):
        """Create a simple mock frame as base64 encoded JPEG"""
        try:
            # Try to use PIL if available
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a simple image
            img = Image.new('RGB', (640, 480), color=(30, 30, 50))
            draw = ImageDraw.Draw(img)
            
            # Add some text and shapes to simulate camera feed
            draw.rectangle([50, 50, 590, 430], outline=(0, 255, 100), width=2)
            
            # Add scanning line effect
            scan_y = (self.frame_count * 5) % 480
            draw.line([(0, scan_y), (640, scan_y)], fill=(0, 255, 100), width=2)
            
            # Add timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            draw.text((10, 10), f"Camera Feed - {timestamp}", fill=(255, 255, 255))
            
            # Add detection status
            if self.detection_active:
                draw.text((10, 450), "SCANNING FOR FACES...", fill=(255, 255, 0))
                # Add face detection box
                draw.rectangle([200, 150, 440, 350], outline=(255, 0, 0), width=3)
                draw.text((210, 130), "FACE DETECTED", fill=(255, 0, 0))
            else:
                draw.text((10, 450), "Monitoring...", fill=(0, 255, 100))
            
            # Convert to JPEG bytes
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            return buffer.getvalue()
            
        except ImportError:
            # Fallback: create a minimal frame without PIL
            return self._create_minimal_frame()
    
    def _create_minimal_frame(self):
        """Create a minimal frame without any image libraries"""
        # Create a simple JPEG header for a minimal image
        # This is a very basic 1x1 pixel JPEG
        minimal_jpeg = bytes([
            0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01,
            0x01, 0x01, 0x00, 0x48, 0x00, 0x48, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43,
            0x00, 0x08, 0x06, 0x06, 0x07, 0x06, 0x05, 0x08, 0x07, 0x07, 0x07, 0x09,
            0x09, 0x08, 0x0A, 0x0C, 0x14, 0x0D, 0x0C, 0x0B, 0x0B, 0x0C, 0x19, 0x12,
            0x13, 0x0F, 0x14, 0x1D, 0x1A, 0x1F, 0x1E, 0x1D, 0x1A, 0x1C, 0x1C, 0x20,
            0x24, 0x2E, 0x27, 0x20, 0x22, 0x2C, 0x23, 0x1C, 0x1C, 0x28, 0x37, 0x29,
            0x2C, 0x30, 0x31, 0x34, 0x34, 0x34, 0x1F, 0x27, 0x39, 0x3D, 0x38, 0x32,
            0x3C, 0x2E, 0x33, 0x34, 0x32, 0xFF, 0xC0, 0x00, 0x11, 0x08, 0x00, 0x01,
            0x00, 0x01, 0x01, 0x01, 0x11, 0x00, 0x02, 0x11, 0x01, 0x03, 0x11, 0x01,
            0xFF, 0xC4, 0x00, 0x14, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0xFF, 0xC4,
            0x00, 0x14, 0x10, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xDA, 0x00, 0x0C,
            0x03, 0x01, 0x00, 0x02, 0x11, 0x03, 0x11, 0x00, 0x3F, 0x00, 0xB2, 0xC0,
            0x07, 0xFF, 0xD9
        ])
        return minimal_jpeg
    
    def start(self):
        """Start the mock camera thread"""
        self.stopped = False
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        return self
    
    def update(self):
        """Update the mock camera frames"""
        while not self.stopped:
            try:
                self.frame_count += 1
                
                # Simulate face detection every few seconds
                current_time = time.time()
                if current_time - self.last_detection_time > self.detection_interval:
                    self.detection_active = not self.detection_active
                    if self.detection_active:
                        # Simulate finding a face
                        self.face_locations = [(150, 440, 350, 200)]  # top, right, bottom, left
                        self.face_names = [random.choice(self.known_names)]
                    else:
                        self.face_locations = []
                        self.face_names = []
                    self.last_detection_time = current_time
                
                # Generate new frame
                self.frame = self._create_simple_frame()
                
                # Control frame rate
                time.sleep(0.1)  # ~10 FPS
                
            except Exception as e:
                print(f"Error in mock camera update: {str(e)}")
                time.sleep(1)
    
    def get_frame(self):
        """Get the current frame as JPEG bytes"""
        if self.frame is not None:
            return self.frame
        else:
            # Return a default frame if none available
            return self._create_minimal_frame()
    
    def stop(self):
        """Stop the mock camera"""
        self.stopped = True
        if hasattr(self, 'thread'):
            self.thread.join()
    
    def get_recognition_results(self):
        """Get current recognition results"""
        results = []
        for i, name in enumerate(self.face_names):
            if i < len(self.face_locations):
                location = self.face_locations[i]
                results.append({
                    'name': name,
                    'confidence': random.uniform(0.7, 0.95),
                    'location': location,
                    'timestamp': time.time()
                })
        return results
    
    def is_running(self):
        """Check if camera is running"""
        return not self.stopped