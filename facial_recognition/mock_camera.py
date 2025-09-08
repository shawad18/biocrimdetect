import os
import time
from threading import Thread
import base64
from io import BytesIO

class MockCamera:
    """A mock camera class that works without OpenCV for hosted environments"""
    
    def __init__(self):
        self.frame = None
        self.stopped = False
        self.face_locations = []
        self.detection_results = []
        self.last_detection_time = 0
        self.detection_interval = 1.0  # Process every 1 second
        self.frame_count = 0
        
        # Create a simple mock frame
        self.mock_frame_data = self.create_mock_frame()
    
    def create_mock_frame(self):
        """Create a simple mock frame as JPEG bytes"""
        # Create a simple text-based "frame" indicating camera is not available
        mock_html = '''
        <svg width="640" height="480" xmlns="http://www.w3.org/2000/svg">
            <rect width="640" height="480" fill="#1a1a2e"/>
            <text x="320" y="200" font-family="Arial" font-size="24" fill="#16213e" text-anchor="middle">
                Camera Not Available
            </text>
            <text x="320" y="240" font-family="Arial" font-size="16" fill="#0f3460" text-anchor="middle">
                Running in hosted environment
            </text>
            <text x="320" y="280" font-family="Arial" font-size="16" fill="#0f3460" text-anchor="middle">
                OpenCV not available
            </text>
            <circle cx="320" cy="350" r="30" fill="#e94560" opacity="0.7"/>
            <text x="320" y="355" font-family="Arial" font-size="12" fill="white" text-anchor="middle">
                MOCK
            </text>
        </svg>
        '''
        
        # For now, return a simple message as bytes
        # In a real implementation, you could convert SVG to image bytes
        return b'Mock camera frame - OpenCV not available'
    
    def start(self):
        """Start the mock camera thread"""
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        """Mock update loop"""
        while not self.stopped:
            # Simulate frame updates
            self.frame_count += 1
            
            # Simulate face detection every few frames
            current_time = time.time()
            if current_time - self.last_detection_time > self.detection_interval:
                self.process_mock_frame()
                self.last_detection_time = current_time
            
            time.sleep(0.1)  # 10 FPS for mock
    
    def process_mock_frame(self):
        """Process mock frame for simulated face detection"""
        # Simulate occasional face detection
        if self.frame_count % 10 == 0:  # Every 10th frame
            self.face_locations = [(200, 150, 240, 180)]  # Mock face location
            self.detection_results = [{
                'location': (200, 150, 240, 180),
                'name': 'Mock Detection',
                'confidence': 0.5,
                'timestamp': time.time()
            }]
        else:
            self.face_locations = []
            self.detection_results = []
    
    def get_frame(self):
        """Return mock frame as JPEG bytes for streaming"""
        # Create a simple mock JPEG header and data
        # This is a minimal JPEG that browsers can display
        mock_jpeg = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\'\" \x0c\x0c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x01\xe0\x02\x80\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
        
        return mock_jpeg
    
    def get_raw_frame(self):
        """Return mock raw frame"""
        return None  # No raw frame in mock mode
    
    def stop(self):
        """Stop the mock camera"""
        self.stopped = True
    
    def get_detection_results(self):
        """Get mock detection results"""
        return self.detection_results
    
    def is_running(self):
        """Check if mock camera is running"""
        return not self.stopped
    
    def get_face_count(self):
        """Get number of mock detected faces"""
        return len(self.face_locations)
    
    def get_frame_with_detections(self):
        """Return mock frame (same as get_frame for mock)"""
        return self.get_frame()

# Test function
if __name__ == "__main__":
    print("Starting mock camera...")
    camera = MockCamera()
    camera.start()
    
    try:
        for i in range(10):
            frame = camera.get_frame()
            results = camera.get_detection_results()
            print(f"Frame {i}: {len(results)} detections")
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nStopping mock camera...")
    
    finally:
        camera.stop()
        print("Mock camera stopped.")