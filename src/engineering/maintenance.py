"""
Maintenance recommendation engine.
"""
from typing import Dict, Any
from src.engineering.utils import load_config

def get_recommendation(detection: Dict[str, Any], config: dict = None) -> str:
    """
    Get maintenance recommendation based on defect class and severity.
    """
    if config is None:
        config = load_config()
        
    logic = config["maintenance_logic"]
    class_name = detection.get("class_name", "Unknown")
    severity = detection.get("severity", "Low").lower()
    
    if class_name in logic:
        return logic[class_name].get(severity, "Inspect Further")
    
    return "Inspect Further"

def generate_recommendations(detections: list, config: dict = None) -> list:
    """
    Append maintenance recommendation to all detections.
    """
    if config is None:
        config = load_config()
        
    maintenance_details = config.get("maintenance_details", {})
        
    for det in detections:
        rec = get_recommendation(det, config)
        det["recommendation"] = rec
        
        details = maintenance_details.get(rec, {})
        det["crew_size"] = details.get("crew_size", "N/A")
        det["equipment"] = details.get("equipment", "N/A")
        det["materials"] = details.get("materials", "N/A")
        det["service_life"] = details.get("service_life", "N/A")
        
    return detections
