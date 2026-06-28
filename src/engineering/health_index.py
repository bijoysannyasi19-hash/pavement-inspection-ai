"""
Road Health Index calculation.
"""
from src.engineering.utils import load_config

def calculate_rhi(detections: list, config: dict = None) -> dict:
    """
    Calculate the Road Health Index (0-100) based on detected defects.
    """
    if config is None:
        config = load_config()
        
    deductions_logic = config["rhi_deductions"]
    
    rhi = 100.0
    total_deductions = 0.0
    
    max_severity_found = "low"
    severity_rank = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    
    for det in detections:
        class_name = det.get("class_name")
        severity = det.get("severity", "low").lower()
        confidence = det.get("confidence", 1.0)
        relative_area = det.get("relative_area", 0.0)
        
        # Track maximum severity for hard capping
        if severity_rank.get(severity, 1) > severity_rank.get(max_severity_found, 1):
            max_severity_found = severity
            
        if class_name in deductions_logic:
            base_deduction = deductions_logic[class_name].get(severity, 0.0)
            # Mathematical Model for RHI Deduction:
            # Deduction = Base_Deduction * (1 + Area_Multiplier) * Confidence_Factor
            area_multiplier = relative_area * 10.0  # Scales deduction based on size
            confidence_factor = confidence  # Lower confidence -> lower deduction impact
            
            calculated_deduction = base_deduction * (1.0 + area_multiplier) * confidence_factor
            total_deductions += calculated_deduction
            det["rhi_deduction"] = round(calculated_deduction, 2)
            
    rhi = max(0.0, rhi - total_deductions)
    
    # Apply Engineering Structural Constraints (Hard Caps)
    # A severely damaged road mathematically cannot score above certain thresholds
    if max_severity_found == "critical":
        rhi = min(rhi, 40.0)
    elif max_severity_found == "high":
        rhi = min(rhi, 70.0)
        
    # Determine Status
    if rhi >= 85:
        status = "Excellent"
    elif rhi >= 70:
        status = "Good"
    elif rhi >= 50:
        status = "Fair"
    elif rhi >= 30:
        status = "Poor"
    else:
        status = "Critical"
        
    return {
        "rhi_score": round(rhi, 2),
        "status": status,
        "total_deductions": round(total_deductions, 2)
    }
