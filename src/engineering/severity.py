"""
Severity logic based on relative area of the damage.
"""
from typing import Dict, Any
from src.engineering.utils import load_config

def assess_severity(detection: Dict[str, Any], config: dict = None) -> str:
    """
    Assess severity of a defect based on its relative area.
    """
    if config is None:
        config = load_config()
        
    thresholds = config["severity_thresholds"]
    relative_area = detection["relative_area"]
    
    class_name = detection.get("class_name", "")
    conf = detection.get("confidence", 0.0)
    
    if relative_area < thresholds["low"]:
        severity = "Low"
        explanation = f"• Damaged area: {relative_area*100:.1f}%\n• Below standard threshold\n• Superficial distress"
    elif relative_area < thresholds["medium"]:
        severity = "Medium"
        explanation = f"• Damaged area: {relative_area*100:.1f}%\n• Moderate distress level\n• Corrective action required"
    elif relative_area < thresholds["high"]:
        severity = "High"
        explanation = f"• Damaged area: {relative_area*100:.1f}%\n• Significant deterioration\n• Structural failure risk"
    else:
        severity = "Critical"
        explanation = f"• Damaged area: {relative_area*100:.1f}%\n• Full-depth failure\n• Immediate safety hazard"
        
    if conf > 0.90:
        explanation += f"\n• High AI confidence ({conf:.2f})"
        
    # Estimate Crack Width
    estimated_width_mm = 0.0
    if "crack" in class_name.lower():
        if severity == "Low":
            estimated_width_mm = 3.5
        elif severity == "Medium":
            estimated_width_mm = 8.0
        elif severity == "High":
            estimated_width_mm = 15.0
        else:
            estimated_width_mm = 25.0
            
    return severity, explanation, estimated_width_mm

def assess_all_severities(detections: list, config: dict = None) -> list:
    """
    Append severity to all detections.
    """
    if config is None:
        config = load_config()
        
    for det in detections:
        sev, exp, width = assess_severity(det, config)
        det["severity"] = sev
        det["severity_explanation"] = exp
        det["estimated_crack_width_mm"] = width
    return detections
