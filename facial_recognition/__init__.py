# Facial recognition package initialization

try:
    from .simple_face_recognition import recognize_from_image, add_known_face
    from .train_model import train_model
    print("Facial recognition modules loaded successfully")
except ImportError as e:
    print(f"Error importing facial recognition modules: {e}")
    # Fallback imports
    try:
        from .mock_recognition import MockFaceRecognition
        print("Using mock recognition as fallback")
    except ImportError:
        print("No facial recognition modules available")