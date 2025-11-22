import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from PIL import Image
import io

class StreamCapture:
    """Handles capturing video stream from VDO.Ninja"""
    
    def __init__(self, view_id):
        self.view_id = view_id
        self.stream_url = f"https://vdo.ninja/?view={view_id}"
        self.driver = None
        self.is_running = False
        
    def setup_browser(self):
        """Setup Chrome browser with appropriate options for streaming"""
        chrome_options = Options()
        
        # Enable media stream
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        chrome_options.add_argument("--enable-usermedia-screen-capturing")
        chrome_options.add_argument("--allow-http-screen-capture")
        chrome_options.add_argument("--auto-select-desktop-capture-source=Screen")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Disable unnecessary features for better performance
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Set window size
        chrome_options.add_argument("--window-size=640,480")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def start(self, wait_time=5):
        """Start the stream capture"""
        print(f"Opening stream: {self.stream_url}")
        self.setup_browser()
        self.driver.get(self.stream_url)
        
        print(f"Waiting {wait_time} seconds for stream to load...")
        time.sleep(wait_time)
        
        self.is_running = True
        print("Stream capture started!")
        
    def get_frame(self):
        """Capture and return current frame from the stream"""
        if not self.is_running or not self.driver:
            return None
            
        try:
            # Capture screenshot from browser
            screenshot = self.driver.get_screenshot_as_png()
            
            # Convert to OpenCV format
            img = Image.open(io.BytesIO(screenshot))
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            return frame
        except Exception as e:
            print(f"Error capturing frame: {e}")
            return None
    
    def stop(self):
        """Stop the stream capture and cleanup"""
        self.is_running = False
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        print("Stream capture stopped")
