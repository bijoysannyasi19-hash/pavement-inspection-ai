"""
Evaluation script to compute metrics (Precision, Recall, mAP, etc.) for the trained YOLO model.
This script is intended to be run locally or in Colab on the actual validation dataset.
"""
import os
import argparse
from ultralytics import YOLO

def main(weights_path: str, data_yaml: str):
    print("========================================")
    print(" Pavement Damage Model Evaluation Script")
    print("========================================")
    
    if not os.path.exists(weights_path):
        print(f"[ERROR] Weights file not found: {weights_path}")
        print("Please provide the correct path to your trained best.pt weights.")
        return
        
    if not os.path.exists(data_yaml):
        print(f"[ERROR] Dataset configuration not found: {data_yaml}")
        print("Please provide the correct path to your data.yaml.")
        return

    print(f"Loading model from {weights_path}...")
    model = YOLO(weights_path)
    
    print(f"Starting evaluation on validation set defined in {data_yaml}...")
    # The validate() method computes mAP@0.5, mAP@0.5:0.95, Precision, Recall
    # and automatically saves confusion matrices and PR curves in the runs/val directory.
    metrics = model.val(data=data_yaml, split='val', verbose=True)
    
    print("\n--- Evaluation Results ---")
    print(f"Precision: {metrics.results_dict.get('metrics/precision(B)', 0):.4f}")
    print(f"Recall:    {metrics.results_dict.get('metrics/recall(B)', 0):.4f}")
    print(f"mAP@0.5:   {metrics.results_dict.get('metrics/mAP50(B)', 0):.4f}")
    print(f"mAP@0.5:0.95: {metrics.results_dict.get('metrics/mAP50-95(B)', 0):.4f}")
    
    print("\n[INFO] Confusion matrix and PR curves have been saved to the 'runs/val' directory.")
    print("You can include these plots directly in your portfolio report.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate YOLO Pavement Model")
    parser.add_argument("--weights", type=str, default="models/pavement_model/weights/best.pt", help="Path to best.pt")
    parser.add_argument("--data", type=str, default="data/dataset.yaml", help="Path to data.yaml")
    args = parser.parse_args()
    
    main(args.weights, args.data)
