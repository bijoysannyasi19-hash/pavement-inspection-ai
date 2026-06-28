"""
Training script for the YOLO Pavement Damage Detection model.
Run this script on a machine with a GPU (or Google Colab) to train on your dataset.
"""
import os
import argparse
from ultralytics import YOLO

def main(data_yaml: str, epochs: int, batch_size: int, imgsz: int):
    print("========================================")
    print(" YOLOv8 Pavement Model Training Script")
    print("========================================")
    
    if not os.path.exists(data_yaml):
        print(f"[ERROR] Dataset configuration not found: {data_yaml}")
        print("Please ensure your dataset is prepared and data.yaml exists.")
        return

    # Initialize YOLOv8 model from pretrained weights
    print("Initializing YOLOv8n pretrained model...")
    model = YOLO("yolov8n.pt")
    
    print(f"Starting training for {epochs} epochs...")
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        batch=batch_size,
        imgsz=imgsz,
        project="models",
        name="pavement_model",
        exist_ok=True,
        pretrained=True,
        optimizer="auto",
        verbose=True
    )
    
    print("\n[SUCCESS] Training completed!")
    print("The best weights have been saved to: models/pavement_model/weights/best.pt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train YOLO Pavement Model")
    parser.add_argument("--data", type=str, default="data/dataset.yaml", help="Path to data.yaml")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    args = parser.parse_args()
    
    main(args.data, args.epochs, args.batch, args.imgsz)
