import sys
import os
import importlib
from PIL import Image
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src.model.inference
importlib.reload(src.model.inference)
from src.model.inference import PavementDamageDetector

detector = PavementDamageDetector("yolov8n.pt")
img = Image.fromarray(np.zeros((640, 640, 3), dtype=np.uint8))
annotated, det = detector.predict(img)

print(f"Len detections returned from predict: {len(det)}")
