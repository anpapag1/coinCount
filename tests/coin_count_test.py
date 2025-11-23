import numpy as np
import cv2

img =cv2.imread('coin_test/coin4.jpg')
img =cv2.resize(img,(360,480))

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray,(9,9),15)      
# auto find threshold values for cv2.threshold
# using Otsu's method
ret , thresh = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

coutures, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
image_copy = img.copy()
# image_copy = cv2.drawContours(image_copy, coutures, -1, (0,255,0), 3)

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
print(f"Number of circular contours found: {len(circular_contours)}")
for contour in circular_contours:
    x,y,w,h = cv2.boundingRect(contour)
    cv2.rectangle(image_copy, (x,y), (x+w, y+h), (255,0,0), 2)

# show the image with contours and num of coins found in the image window
coin_count = len(circular_contours)
cv2.putText(image_copy, f'Coins: {coin_count}', (10, 30), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.imshow('image', image_copy)
# wait to close the window
cv2.waitKey(0)
cv2.destroyAllWindows()