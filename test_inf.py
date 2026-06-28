import os
import sys
from PIL import Image
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.model.inference import PavementDamageDetector

def main():
    detector = PavementDamageDetector("yolov8n.pt")
    # create a dummy image
    img = Image.fromarray(np.zeros((640, 640, 3), dtype=np.uint8))
    annotated, det = detector.predict(img)
    print("Detections:", det)
    print("Success")

if __name__ == "__main__":
    main()
