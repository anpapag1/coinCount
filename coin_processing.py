import cv2
import numpy as np

class CoinProcessor:
    """Processes frames to detect coins"""
    
    def __init__(self, min_dist=80, min_radius=15, max_radius=80):
        """
        Initialize coin processor with detection parameters
        
        Args:
            min_dist: Minimum distance between detected coin centers
            min_radius: Minimum coin radius in pixels
            max_radius: Maximum coin radius in pixels
        """
        self.min_dist = min_dist
        self.min_radius = min_radius
        self.max_radius = max_radius
        
    def detect_coins(self, frame):

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray,(9,9),15)      
        # auto find threshold values for cv2.threshold
        # using Otsu's method
        ret , thresh = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        coutures, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        frame_copy = frame.copy()
        # frame_copy = cv2.drawContours(frame_copy, coutures, -1, (0,255,0), 3)

        # in coutures find circular shapes only
        circular_contours = []
        for contour in coutures:
            # Calculate contour area and perimeter
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            
            # Skip very small contours
            if area < 100:
                continue
            
            # Calculate circularity: 4*pi*area / perimeter^2
            # For a perfect circle, this equals 1.0
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                
                # Filter contours with circularity > 0.7 (adjust threshold as needed)
                if circularity > 0.7:
                    circular_contours.append(contour)

        # draw rectangles around contours and print number of contours found
        for contour in circular_contours:
            x,y,w,h = cv2.boundingRect(contour)
            cv2.rectangle(frame_copy, (x,y), (x+w, y+h), (255,0,0), 2)
                
        return circular_contours, frame_copy
    
    
    def add_info_overlay(self, frame, coin_count):
        """
        Add information overlay to the frame
        
        Args:
            frame: Frame to add overlay to (modified in place)
            frame_count: Current frame number
            coin_count: Number of detected coins
        """
        cv2.putText(frame, f"Coins: {coin_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
