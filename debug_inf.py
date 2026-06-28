import os
import sys
from PIL import Image
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.model.inference import PavementDamageDetector

def main():
    print("Testing inference...")
    detector = PavementDamageDetector("models/pavement_model/weights/best.pt")
    print(f"demo_mode: {detector.demo_mode}")
    img = Image.fromarray(np.zeros((640, 640, 3), dtype=np.uint8))
    annotated, det = detector.predict(img)
    print(f"Detections length: {len(det)}")
    print("Detections array:", det)

if __name__ == "__main__":
    main()
