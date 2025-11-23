import cv2
import numpy as np

class CoinProcessor:
    """Processes frames to detect coins"""
    
    def __init__(self, blur=15, show_contours=False):
        self.blur = blur
        self.show_contours = show_contours
        
    def detect_coins(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9,9), self.blur)
        
        # Auto-threshold using Otsu's method
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        result = frame.copy()
        
        if self.show_contours:
            cv2.drawContours(result, contours, -1, (0,255,0), 3)

        # Filter for circular shapes
        circles = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 100:  # Skip tiny contours
                continue
            
            perimeter = cv2.arcLength(cnt, True)
            if perimeter > 0:
                # Circularity = 4*pi*area / perimeter^2 (1.0 = perfect circle)
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                if circularity > 0.7:
                    circles.append(cnt)

        # Draw bounding boxes
        for cnt in circles:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(result, (x,y), (x+w, y+h), (255,0,0), 2)
                
        return circles, result
    
    
    def add_info_overlay(self, frame, coin_count):
        cv2.putText(frame, f"Coins: {coin_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
