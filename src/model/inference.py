"""
Inference script to run the damage detection model on new images.
Provides structured output for the engineering logic.
"""
import os
import logging
import numpy as np
from PIL import Image
from ultralytics import YOLO
from typing import List, Dict, Any, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PavementDamageDetector:
    def __init__(self, weights_path: str = "yolov8n.pt"):
        """
        Initialize the detector. Defaults to yolov8n.pt if custom weights aren't available,
        so the application can run in demo mode.
        """
        # If custom weights don't exist, fallback to base yolov8n.pt for demonstration
        if not os.path.exists(weights_path) and weights_path != "yolov8n.pt":
            logging.warning(f"Weights {weights_path} not found. Falling back to yolov8n.pt for demo.")
            weights_path = "yolov8n.pt"
            self.demo_mode = True
        else:
            self.demo_mode = False
            
        self.model = YOLO(weights_path)
        
        # Hardcode class names for demo mode fallback
        self.demo_classes = {
            0: "Pothole", 1: "Longitudinal Crack", 2: "Transverse Crack", 
            3: "Alligator Crack", 4: "Rutting", 5: "Manhole Damage", 6: "Road Marking Damage"
        }

    def predict(self, image: Image.Image, conf_threshold: float = 0.25) -> Tuple[Image.Image, List[Dict[str, Any]]]:
        """
        Run inference on a single PIL Image.
        Returns the annotated image and a list of structured detections.
        """
        # Convert PIL Image to RGB (YOLO expects RGB/BGR)
        img_arr = np.array(image.convert("RGB"))
        
        # In demo mode, yolov8n.pt (COCO) will hallucinate cars/people in pavement cracks.
        # This causes len(detections) > 0, which breaks the dynamic mock logic in the app.
        # We bypass it entirely to guarantee a clean slate for the mock logic.
        if self.demo_mode:
            return image.copy(), []
            
        # Run inference
        results = self.model(img_arr, conf=conf_threshold, verbose=False)[0]
        
        # Get annotated image
        annotated_img_arr = results.plot()
        annotated_image = Image.fromarray(annotated_img_arr)
        
        # Parse detections
        detections = []
        for box in results.boxes:
            class_id = int(box.cls[0].item())
            
            # Map class name
            if self.demo_mode:
                class_name = self.demo_classes.get(class_id % len(self.demo_classes), "Unknown Damage")
            else:
                class_name = results.names[class_id]
                
            conf = float(box.conf[0].item())
            
            # Bounding box coordinates [x1, y1, x2, y2]
            xyxy = box.xyxy[0].tolist()
            
            # Calculate width, height and area of the bounding box
            w = xyxy[2] - xyxy[0]
            h = xyxy[3] - xyxy[1]
            box_area = w * h
            
            # Image area
            img_h, img_w = img_arr.shape[:2]
            img_area = img_w * img_h
            
            # Relative area (used for severity)
            relative_area = box_area / img_area
            
            detections.append({
                "class_id": class_id,
                "class_name": class_name,
                "confidence": conf,
                "bbox": xyxy,
                "box_area": box_area,
                "relative_area": relative_area
            })
            
        return annotated_image, detections
