import os
from .enhanced_mock_recognition import EnhancedMockFaceRecognition
from .webcam_simulation import WebcamSimulation
from .mock_recognition import MockFaceRecognition

class CameraManager:
    """Manages different camera simulation modes"""
    
    MODES = {
        'enhanced_mock': 'Enhanced Mock Camera (Animated)',
        'webcam_sim': 'Real Webcam with Simulation',
        'basic_mock': 'Basic Mock Camera (Simple)',
        'auto': 'Auto-detect Best Option'
    }
    
    def __init__(self, mode='auto'):
        self.mode = mode
        self.camera_instance = None
        
    def get_camera_instance(self):
        """Get the appropriate camera instance based on mode"""
        if self.mode == 'auto':
            return self._auto_detect_camera()
        elif self.mode == 'enhanced_mock':
            return EnhancedMockFaceRecognition()
        elif self.mode == 'webcam_sim':
            return WebcamSimulation()
        elif self.mode == 'basic_mock':
            return MockFaceRecognition()
        else:
            # Default to enhanced mock
            return EnhancedMockFaceRecognition()
    
    def _auto_detect_camera(self):
        """Auto-detect the best camera option available"""
        try:
            # First try webcam simulation
            webcam = WebcamSimulation()
            if webcam.webcam_available:
                print("Auto-detected: Using real webcam with simulation overlay")
                return webcam
            else:
                webcam.stop()
        except Exception as e:
            print(f"Webcam detection failed: {e}")
        
        try:
            # Fall back to enhanced mock
            print("Auto-detected: Using enhanced mock camera simulation")
            return EnhancedMockFaceRecognition()
        except Exception as e:
            print(f"Enhanced mock failed: {e}")
            # Final fallback to basic mock
            print("Auto-detected: Using basic mock camera")
            return MockFaceRecognition()
    
    @classmethod
    def get_available_modes(cls):
        """Get list of available camera modes"""
        return cls.MODES
    
    def set_mode(self, mode):
        """Change camera mode"""
        if mode in self.MODES:
            self.mode = mode
            # Stop current instance if running
            if self.camera_instance:
                try:
                    self.camera_instance.stop()
                except:
                    pass
            self.camera_instance = None
            return True
        return False

# Global camera manager instance
camera_manager = CameraManager()

def get_camera_instance():
    """Get the current camera instance"""
    if camera_manager.camera_instance is None:
        camera_manager.camera_instance = camera_manager.get_camera_instance()
    return camera_manager.camera_instance

def set_camera_mode(mode):
    """Set the camera mode"""
    return camera_manager.set_mode(mode)

def get_camera_modes():
    """Get available camera modes"""
    return CameraManager.get_available_modes()