import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engineering.cost import estimate_cost
from src.engineering.health_index import calculate_rhi
from src.engineering.severity import assess_severity

def test_estimate_cost():
    # Mock config
    config = {
        "unit_costs": {
            "Crack Sealing": 5.00,
            "Patching": 35.00
        },
        "road_category_multipliers": {
            "Local": 1.0,
            "Highway": 2.0
        }
    }
    
    det = {
        "recommendation": "Crack Sealing",
        "relative_area": 0.05
    }
    
    # 0.05 * 10 (IMAGE_PHYSICAL_AREA_SQM) = 0.5 sqm. 
    # 0.5 * 5.00 = 2.50
    cost = estimate_cost(det, road_category="Local", config=config)
    assert cost == 2.50
    
    # Test multiplier
    # 0.5 * 5.00 * 2.0 = 5.00
    cost_highway = estimate_cost(det, road_category="Highway", config=config)
    assert cost_highway == 5.00

def test_assess_severity():
    config = {
        "severity_thresholds": {
            "low": 0.02,
            "medium": 0.05,
            "high": 0.15
        }
    }
    
    det_low = {"relative_area": 0.01}
    sev, _ = assess_severity(det_low, config)
    assert sev == "Low"
    
    det_crit = {"relative_area": 0.20}
    sev, _ = assess_severity(det_crit, config)
    assert sev == "Critical"

def test_calculate_rhi():
    config = {
        "rhi_deductions": {
            "Pothole": {
                "low": 2.0,
                "high": 10.0
            }
        }
    }
    
    detections = [
        {
            "class_name": "Pothole",
            "severity": "low",
            "relative_area": 0.01,
            "confidence": 1.0
        }
    ]
    
    rhi_info = calculate_rhi(detections, config)
    # Deduction: base 2.0 * (1 + 0.01*10) * 1.0 = 2.0 * 1.1 = 2.2
    # RHI: 100 - 2.2 = 97.8
    assert rhi_info["rhi_score"] == 97.8
    assert rhi_info["status"] == "Excellent"
