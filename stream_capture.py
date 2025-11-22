import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        
        # Set window size and position (move off-screen)
        chrome_options.add_argument("--window-size=640,480")
        chrome_options.add_argument("--window-position=-2000,-2000")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Move window off-screen after creation
        self.driver.set_window_position(-2000, -2000)
        
    def start(self, wait_time=5):
        """Start the stream capture"""
        print(f"Opening stream: {self.stream_url}")
        self.setup_browser()
        self.driver.get(self.stream_url)
        
        print("Waiting for stream to load...")
        time.sleep(3)
        
        # Try to auto-click play button if it exists
        try:
            print("Attempting to find and click play button...")
            wait = WebDriverWait(self.driver, 10)
            
            # VDO.Ninja specific - try to find video element and any overlays
            try:
                # First, try to click on the entire page body to trigger play
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.click()
                print("Clicked page body")
                time.sleep(1)
            except:
                pass
            
            # Try to find and play video element directly
            try:
                video_elements = self.driver.find_elements(By.TAG_NAME, "video")
                for video in video_elements:
                    try:
                        # Use JavaScript to play the video
                        self.driver.execute_script("""
                            arguments[0].play();
                            arguments[0].muted = false;
                        """, video)
                        print(f"Video element played via JavaScript!")
                        time.sleep(1)
                    except Exception as e:
                        print(f"Could not play video: {e}")
            except:
                pass
            
            # Try clicking common play button patterns
            play_selectors = [
                (By.CSS_SELECTOR, "button.play"),
                (By.CSS_SELECTOR, "button[aria-label*='play' i]"),
                (By.CSS_SELECTOR, "div.play-button"),
                (By.XPATH, "//button[contains(text(), 'Play')]"),
                (By.XPATH, "//button[contains(text(), 'play')]"),
                (By.XPATH, "//*[contains(@class, 'play')]"),
                (By.CSS_SELECTOR, ".video-overlay"),
                (By.ID, "container"),
            ]
            
            for by_type, selector in play_selectors:
                try:
                    elements = self.driver.find_elements(by_type, selector)
                    for element in elements:
                        try:
                            element.click()
                            print(f"Clicked element: {selector}")
                            time.sleep(0.5)
                        except:
                            pass
                except:
                    continue
                    
        except Exception as e:
            print(f"Auto-play attempt finished: {e}")
        
        print(f"Waiting additional {wait_time} seconds...")
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
