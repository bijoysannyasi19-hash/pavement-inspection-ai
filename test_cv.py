import cv2
import numpy as np
from PIL import Image

def get_damage_bboxes(image_path, num_boxes=1):
    img = cv2.imread(image_path)
    if img is None:
        # Create a dummy image with a dark "crack" in the middle
        img = np.ones((600, 800, 3), dtype=np.uint8) * 200
        cv2.line(img, (200, 300), (600, 350), (50, 50, 50), 20)
        cv2.line(img, (400, 200), (450, 500), (50, 50, 50), 15)
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Dark areas often indicate cracks/potholes (lower pixel values)
    # Apply morphological operations (black hat) to find dark regions against light background
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    
    # 2. Thresholding to isolate the strongest dark regions
    _, thresh = cv2.threshold(blackhat, 30, 255, cv2.THRESH_BINARY)
    
    # 3. Dilation to connect broken crack lines into single blobs
    dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(thresh, dilate_kernel, iterations=2)
    
    # 4. Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    bboxes = []
    if contours:
        # Sort by area descending
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for c in contours[:num_boxes]:
            x, y, w, h = cv2.boundingRect(c)
            # Add some padding
            pad = 20
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(img.shape[1], x + w + pad)
            y2 = min(img.shape[0], y + h + pad)
            bboxes.append([x1, y1, x2, y2])
            
    return bboxes

print(get_damage_bboxes("dummy.jpg", 1))
