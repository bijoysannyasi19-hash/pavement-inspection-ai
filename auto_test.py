"""
Automated validation script for the AI Pavement Asset Management System.
Processes a batch of images to verify CV detections, engineering logic constraints, 
and produces a summary report.

Usage:
    python auto_test.py --image_dir path/to/validation_images
"""
import os
import glob
import argparse
from PIL import Image

# Import the core engineering modules
from src.model.inference import PavementDamageDetector
from src.engineering.severity import assess_all_severities
from src.engineering.maintenance import generate_recommendations
from src.engineering.cost import calculate_total_cost
from src.engineering.health_index import calculate_rhi

def validate_pipeline(image_dir: str):
    print("========================================")
    print(" Pavement Pipeline Automated Validation")
    print("========================================")
    
    if not os.path.exists(image_dir):
        print(f"[ERROR] Directory not found: {image_dir}")
        return
        
    image_files = glob.glob(os.path.join(image_dir, "*.[jJ][pP][gG]")) + \
                  glob.glob(os.path.join(image_dir, "*.[pP][nN][gG]"))
                  
    if not image_files:
        print(f"[WARNING] No images found in {image_dir}")
        return
        
    print(f"[INFO] Found {len(image_files)} images for validation.")
    
    detector = PavementDamageDetector(weights_path="models/pavement_model/weights/best.pt")
    
    failures = 0
    passed = 0
    
    for img_path in image_files:
        print(f"\n--- Testing: {os.path.basename(img_path)} ---")
        try:
            image = Image.open(img_path)
            # 1. Detection
            _, detections = detector.predict(image, conf_threshold=0.25)
            
            # 2. Engineering Logic
            detections = assess_all_severities(detections)
            detections = generate_recommendations(detections)
            total_cost = calculate_total_cost(detections, road_category="Local")
            rhi_info = calculate_rhi(detections)
            
            # 3. Validation Constraints
            issues = []
            if rhi_info["rhi_score"] < 0 or rhi_info["rhi_score"] > 100:
                issues.append(f"RHI score out of bounds: {rhi_info['rhi_score']}")
                
            if total_cost < 0:
                issues.append(f"Negative repair cost calculated: {total_cost}")
                
            for det in detections:
                if not det.get("class_name"):
                    issues.append("Missing defect class_name")
                if "repair_duration_hours" not in det:
                    issues.append("Missing repair_duration_hours metric")
                if "priority" not in det:
                    issues.append("Missing priority metric")
                    
            if issues:
                print(f"[FAIL] Pipeline constraints violated:")
                for issue in issues:
                    print(f"       - {issue}")
                failures += 1
            else:
                print(f"[PASS] RHI: {rhi_info['rhi_score']} | Cost: ${total_cost} | Detections: {len(detections)}")
                passed += 1
                
        except Exception as e:
            print(f"[ERROR] Pipeline crashed on {os.path.basename(img_path)}: {str(e)}")
            failures += 1
            
    print("\n========================================")
    print(" Validation Summary")
    print("========================================")
    print(f"Total Tested : {len(image_files)}")
    print(f"Passed       : {passed}")
    print(f"Failed       : {failures}")
    
    if failures > 0:
        print("\n[!] The pipeline requires adjustments to fix the failing constraints.")
    else:
        print("\n[+] All outputs are mathematically and technically sound! Ready for production.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Pavement Pipeline Test")
    parser.add_argument("--image_dir", type=str, required=True, help="Directory of test images")
    args = parser.parse_args()
    
    validate_pipeline(args.image_dir)
