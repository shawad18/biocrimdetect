#!/usr/bin/env python3
"""
Initialize Face Recognition for Production Deployment
This script creates basic face encodings for the deployed environment.
"""

import os
import pickle
import numpy as np
from pathlib import Path

def create_default_encodings():
    """Create default face encodings for demo purposes"""
    
    # Create facial_recognition directory if it doesn't exist
    face_dir = Path('facial_recognition')
    face_dir.mkdir(exist_ok=True)
    
    # Create encodings file path
    encodings_file = face_dir / 'encodings.pkl'
    
    # Create some demo face encodings (random vectors for demo)
    # In production, these would be real face encodings from training images
    demo_encodings = [
        np.random.rand(128).tolist(),  # Demo encoding 1
        np.random.rand(128).tolist(),  # Demo encoding 2
        np.random.rand(128).tolist(),  # Demo encoding 3
    ]
    
    demo_names = [
        "John Doe",
        "Jane Smith", 
        "Mike Johnson"
    ]
    
    # Create the data structure
    data = {
        "encodings": demo_encodings,
        "names": demo_names
    }
    
    # Save to pickle file
    try:
        with open(encodings_file, 'wb') as f:
            pickle.dump(data, f)
        print(f"✅ Created face encodings file: {encodings_file}")
        print(f"📊 Added {len(demo_names)} demo face encodings")
        return True
    except Exception as e:
        print(f"❌ Error creating encodings file: {e}")
        return False

def check_face_recognition_setup():
    """Check if face recognition is properly set up"""
    
    try:
        import face_recognition
        print("✅ face_recognition library available")
    except ImportError:
        print("❌ face_recognition library not available")
        return False
    
    try:
        import dlib
        print("✅ dlib library available")
    except ImportError:
        print("❌ dlib library not available")
        return False
    
    try:
        import cv2
        print("✅ OpenCV library available")
    except ImportError:
        print("❌ OpenCV library not available")
        return False
    
    return True

def main():
    """Main initialization function"""
    print("🚀 Initializing Face Recognition for Production...")
    print("=" * 50)
    
    # Check if libraries are available
    if not check_face_recognition_setup():
        print("⚠️  Face recognition libraries not fully available")
        print("📝 The system will use mock face recognition instead")
        return
    
    # Create default encodings
    if create_default_encodings():
        print("\n🎉 Face Recognition Initialization Complete!")
        print("\n📋 Next Steps:")
        print("1. Upload real face images to train the system")
        print("2. Run train_model.py to create real encodings")
        print("3. Test face matching functionality")
    else:
        print("\n❌ Face Recognition Initialization Failed!")
        print("📝 The system will use mock face recognition")

if __name__ == '__main__':
    main()