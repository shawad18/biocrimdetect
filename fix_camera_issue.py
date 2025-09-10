#!/usr/bin/env python3
"""
Camera Issue Fix Script
Disable virtual cameras and force real camera usage
"""

import cv2
import time
import sys
import os

def find_real_cameras():
    """Find real physical cameras (not virtual ones)"""
    print("🔍 Scanning for real cameras...")
    
    real_cameras = []
    virtual_cameras = []
    
    # Test camera indices 0-10
    for index in range(11):
        try:
            cap = cv2.VideoCapture(index)
            
            if not cap.isOpened():
                continue
            
            # Try to read a frame
            ret, frame = cap.read()
            
            if not ret or frame is None:
                cap.release()
                continue
            
            # Get camera properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # Check if it's likely a virtual camera
            is_virtual = False
            
            # Common virtual camera indicators
            virtual_indicators = [
                'camo',
                'obs',
                'virtual',
                'snap',
                'zoom',
                'teams',
                'skype'
            ]
            
            # Check backend name if available
            backend = cap.getBackendName() if hasattr(cap, 'getBackendName') else 'unknown'
            
            # Analyze frame content for virtual camera patterns
            if frame is not None:
                # Check for text patterns that indicate virtual cameras
                import numpy as np
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Look for high contrast text areas (common in virtual camera setup screens)
                edges = cv2.Canny(gray, 50, 150)
                edge_ratio = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
                
                # Virtual cameras often have more structured/artificial content
                if edge_ratio > 0.1:  # High edge density might indicate text/UI
                    is_virtual = True
            
            camera_info = {
                'index': index,
                'resolution': (width, height),
                'fps': fps,
                'backend': backend,
                'is_virtual': is_virtual
            }
            
            if is_virtual:
                virtual_cameras.append(camera_info)
                print(f"🎭 Virtual Camera {index}: {width}x{height} @ {fps:.1f}fps ({backend})")
            else:
                real_cameras.append(camera_info)
                print(f"📹 Real Camera {index}: {width}x{height} @ {fps:.1f}fps ({backend})")
            
            cap.release()
            
        except Exception as e:
            print(f"❌ Error testing camera {index}: {str(e)}")
    
    return real_cameras, virtual_cameras

def test_camera_content(camera_index):
    """Test camera content to see if it shows real video"""
    print(f"\n🎬 Testing camera {camera_index} content...")
    
    try:
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"❌ Cannot open camera {camera_index}")
            return False
        
        # Capture multiple frames to analyze
        frames = []
        for i in range(10):
            ret, frame = cap.read()
            if ret and frame is not None:
                frames.append(frame)
            time.sleep(0.1)
        
        cap.release()
        
        if not frames:
            print(f"❌ No frames captured from camera {camera_index}")
            return False
        
        # Analyze frames for motion/changes (real cameras usually have some variation)
        import numpy as np
        
        if len(frames) >= 2:
            # Calculate frame differences
            diffs = []
            for i in range(1, len(frames)):
                diff = cv2.absdiff(frames[i-1], frames[i])
                diff_score = np.mean(diff)
                diffs.append(diff_score)
            
            avg_diff = np.mean(diffs)
            print(f"   📊 Average frame difference: {avg_diff:.2f}")
            
            # Real cameras usually have some variation, virtual cameras might be static
            if avg_diff < 1.0:
                print(f"   🎭 Likely virtual/static camera (low variation)")
                return False
            else:
                print(f"   📹 Likely real camera (good variation)")
                return True
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing camera {camera_index}: {str(e)}")
        return False

def update_camera_config():
    """Update camera configuration in the application"""
    print("\n🔧 Updating camera configuration...")
    
    # Find the best real camera
    real_cameras, virtual_cameras = find_real_cameras()
    
    if not real_cameras:
        print("❌ No real cameras found!")
        return False
    
    # Test each real camera for actual content
    best_camera = None
    for camera in real_cameras:
        if test_camera_content(camera['index']):
            best_camera = camera
            break
    
    if not best_camera:
        print("❌ No working real cameras found!")
        return False
    
    print(f"\n✅ Best real camera: Index {best_camera['index']} ({best_camera['resolution'][0]}x{best_camera['resolution'][1]})")
    
    # Update the enhanced face detection to use this camera
    try:
        # Read the current file
        enhanced_file = 'facial_recognition/enhanced_face_detection.py'
        with open(enhanced_file, 'r') as f:
            content = f.read()
        
        # Update the camera index priority
        old_line = "for camera_index in [1, 0, -1]:"
        new_line = f"for camera_index in [{best_camera['index']}, 1, 0, -1]:"
        
        if old_line in content:
            content = content.replace(old_line, new_line)
            
            with open(enhanced_file, 'w') as f:
                f.write(content)
            
            print(f"✅ Updated enhanced face detection to prioritize camera {best_camera['index']}")
        
        # Update simple camera detection too
        simple_file = 'facial_recognition/simple_camera_detection.py'
        with open(simple_file, 'r') as f:
            content = f.read()
        
        if old_line in content:
            content = content.replace(old_line, new_line)
            
            with open(simple_file, 'w') as f:
                f.write(content)
            
            print(f"✅ Updated simple camera detection to prioritize camera {best_camera['index']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating camera configuration: {str(e)}")
        return False

def main():
    print("🚀 Camera Issue Fix Tool")
    print("=" * 40)
    
    print("\n📋 Issue Analysis:")
    print("   - Camera showing 'Configure Camo Studio'")
    print("   - This indicates virtual camera is being used")
    print("   - Need to find and use real physical camera")
    
    # Find cameras
    real_cameras, virtual_cameras = find_real_cameras()
    
    print(f"\n📊 Camera Summary:")
    print(f"   📹 Real cameras found: {len(real_cameras)}")
    print(f"   🎭 Virtual cameras found: {len(virtual_cameras)}")
    
    if virtual_cameras:
        print("\n🎭 Virtual cameras detected:")
        for cam in virtual_cameras:
            print(f"   - Camera {cam['index']}: {cam['resolution'][0]}x{cam['resolution'][1]} (likely Camo Studio or similar)")
    
    if not real_cameras:
        print("\n❌ No real cameras found!")
        print("\n💡 Solutions:")
        print("   1. Disable Camo Studio or other virtual camera apps")
        print("   2. Check if physical camera is connected")
        print("   3. Restart computer to reset camera drivers")
        print("   4. Check camera permissions in Windows settings")
        return False
    
    # Update configuration
    if update_camera_config():
        print("\n🎉 Camera configuration updated successfully!")
        print("\n📋 Next steps:")
        print("   1. Restart the Flask application")
        print("   2. Test the live face verification")
        print("   3. Camera should now show real video instead of Camo Studio")
        return True
    else:
        print("\n❌ Failed to update camera configuration")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Fix interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        sys.exit(1)