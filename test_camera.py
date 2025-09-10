#!/usr/bin/env python3
"""
Camera Test Script
Test if camera hardware is accessible and working
"""

import cv2
import time
import sys

def test_camera():
    print("🔍 Testing camera accessibility...")
    
    # Test different camera indices
    camera_indices = [0, 1, -1]
    working_cameras = []
    
    for index in camera_indices:
        print(f"\n📹 Testing camera index {index}...")
        
        try:
            cap = cv2.VideoCapture(index)
            
            if not cap.isOpened():
                print(f"❌ Camera {index}: Failed to open")
                continue
            
            # Try to read a frame
            ret, frame = cap.read()
            
            if not ret or frame is None:
                print(f"❌ Camera {index}: Failed to read frame")
                cap.release()
                continue
            
            # Check frame properties
            height, width = frame.shape[:2]
            print(f"✅ Camera {index}: Working!")
            print(f"   📐 Resolution: {width}x{height}")
            print(f"   📊 Frame shape: {frame.shape}")
            
            # Test if we can get multiple frames
            frame_count = 0
            start_time = time.time()
            
            for i in range(10):
                ret, frame = cap.read()
                if ret:
                    frame_count += 1
                time.sleep(0.1)
            
            elapsed = time.time() - start_time
            fps = frame_count / elapsed
            
            print(f"   🎬 Captured {frame_count}/10 frames in {elapsed:.2f}s")
            print(f"   ⚡ Estimated FPS: {fps:.2f}")
            
            working_cameras.append({
                'index': index,
                'resolution': (width, height),
                'fps': fps
            })
            
            cap.release()
            
        except Exception as e:
            print(f"❌ Camera {index}: Error - {str(e)}")
    
    return working_cameras

def test_enhanced_detection():
    print("\n🎯 Testing Enhanced Face Detection...")
    
    try:
        from facial_recognition.enhanced_face_detection import EnhancedFaceDetection
        
        print("✅ Enhanced face detection module imported successfully")
        
        # Try to initialize
        detector = EnhancedFaceDetection()
        print("✅ Enhanced face detection initialized")
        
        # Try to start (but don't actually start the camera)
        print("✅ Enhanced face detection ready")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced face detection error: {str(e)}")
        return False

def test_simple_detection():
    print("\n📷 Testing Simple Camera Detection...")
    
    try:
        from facial_recognition.simple_camera_detection import SimpleCameraDetection
        
        print("✅ Simple camera detection module imported successfully")
        
        # Try to initialize
        detector = SimpleCameraDetection()
        print("✅ Simple camera detection initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple camera detection error: {str(e)}")
        return False

def main():
    print("🚀 Camera Hardware and Module Test")
    print("=" * 50)
    
    # Test camera hardware
    working_cameras = test_camera()
    
    if not working_cameras:
        print("\n❌ No working cameras found!")
        print("\n🔧 Possible solutions:")
        print("   1. Check if camera is connected")
        print("   2. Check camera permissions")
        print("   3. Close other applications using camera")
        print("   4. Try a different camera")
        return False
    
    print(f"\n✅ Found {len(working_cameras)} working camera(s):")
    for cam in working_cameras:
        print(f"   📹 Camera {cam['index']}: {cam['resolution'][0]}x{cam['resolution'][1]} @ {cam['fps']:.1f} FPS")
    
    # Test detection modules
    enhanced_ok = test_enhanced_detection()
    simple_ok = test_simple_detection()
    
    print("\n📊 Test Summary:")
    print(f"   📹 Camera Hardware: {'✅ Working' if working_cameras else '❌ Failed'}")
    print(f"   🎯 Enhanced Detection: {'✅ Working' if enhanced_ok else '❌ Failed'}")
    print(f"   📷 Simple Detection: {'✅ Working' if simple_ok else '❌ Failed'}")
    
    if working_cameras and (enhanced_ok or simple_ok):
        print("\n🎉 Camera system should work!")
        print("\n💡 Recommended camera for Flask app:")
        best_cam = max(working_cameras, key=lambda x: x['fps'])
        print(f"   📹 Use camera index {best_cam['index']} ({best_cam['resolution'][0]}x{best_cam['resolution'][1]})")
        return True
    else:
        print("\n❌ Camera system has issues that need to be resolved")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        sys.exit(1)