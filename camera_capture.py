import cv2


class CameraCapture:
    """Handles capturing video stream from a camera"""
    
    def __init__(self, camera_index):
        self.camera_index = camera_index
        self.cap = None
        self.is_running = False
        
    def start(self):
        """Start the camera capture"""
        print(f"Opening camera: {self.camera_index}")
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            print(f"Failed to open camera {self.camera_index}")
            return False
        
        # Read a test frame
        ret, frame = self.cap.read()
        if not ret:
            print(f"Failed to read from camera {self.camera_index}")
            self.cap.release()
            return False
        
        self.is_running = True
        print("Camera capture started!")
        return True
        
    def get_frame(self):
        """Capture and return current frame from the camera"""
        if not self.is_running or not self.cap:
            return None
            
        try:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to read frame from camera")
                return None
            return frame
        except Exception as e:
            print(f"Error capturing frame: {e}")
            return None
    
    def stop(self):
        """Stop the camera capture and cleanup"""
        self.is_running = False
        if self.cap:
            try:
                self.cap.release()
            except:
                pass
        print("Camera capture stopped")
