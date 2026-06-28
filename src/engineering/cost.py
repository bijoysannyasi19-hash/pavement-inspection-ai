"""
Cost estimation logic for recommended maintenance.
"""
from typing import Dict, Any
from src.engineering.utils import load_config

# Assume an average road image covers roughly 10 square meters of road surface
# for conversion from relative area to physical square meters.
IMAGE_PHYSICAL_AREA_SQM = 10.0 

def estimate_cost(detection: Dict[str, Any], road_category: str = "Local", config: dict = None) -> float:
    """
    Estimate the repair cost based on recommendation, physical area, and road category.
    """
    if config is None:
        config = load_config()
        
    costs = config["unit_costs"]
    multipliers = config.get("road_category_multipliers", {})
    recommendation = detection.get("recommendation")
    relative_area = detection.get("relative_area", 0)
    
    if recommendation not in costs:
        return 0.0
        
    unit_cost = costs[recommendation]
    multiplier = multipliers.get(road_category, 1.0)
    
    # If it's a fixed cost item (e.g. Manhole Repair)
    if recommendation == "Manhole Repair":
        return float(unit_cost * multiplier)
        
    # Else calculate based on area
    physical_area = relative_area * IMAGE_PHYSICAL_AREA_SQM
    
    # Minimum repair area of 0.5 sqm assumption
    physical_area = max(physical_area, 0.5)
    
    total_cost = physical_area * unit_cost * multiplier
    
    # Calculate Repair Duration (Hours)
    productivity_rates = config.get("productivity_rates", {})
    prod_rate = productivity_rates.get(recommendation, 1.0)
    
    if recommendation == "Manhole Repair":
        duration_hours = 1.0
    else:
        duration_hours = physical_area / prod_rate
        
    # Assign Priority
    priority_map = config.get("priority_mapping", {})
    severity = detection.get("severity", "Low")
    priority = priority_map.get(severity, "Low (Next Cycle)")
    
    # Save metrics in the detection dictionary
    detection["physical_area_sqm"] = round(physical_area, 2)
    detection["unit_cost_applied"] = unit_cost
    detection["repair_duration_hours"] = round(duration_hours, 2)
    detection["priority"] = priority
    
    # Calculate Cost Breakdown
    breakdown = config.get("cost_breakdown", {})
    ratios = breakdown.get(recommendation, {"labor": 0.25, "materials": 0.25, "equipment": 0.25, "traffic": 0.25})
    
    detection["labor_cost"] = round(total_cost * ratios.get("labor", 0.25), 2)
    detection["materials_cost"] = round(total_cost * ratios.get("materials", 0.25), 2)
    detection["equipment_cost"] = round(total_cost * ratios.get("equipment", 0.25), 2)
    detection["traffic_management_cost"] = round(total_cost * ratios.get("traffic", 0.25), 2)
    
    return round(total_cost, 2)

def calculate_total_cost(detections: list, road_category: str = "Local", config: dict = None) -> float:
    """
    Calculate total estimated cost for all detections.
    """
    if config is None:
        config = load_config()
        
    total = 0.0
    for det in detections:
        cost = estimate_cost(det, road_category, config)
        det["estimated_cost"] = cost
        total += cost
    return round(total, 2)
