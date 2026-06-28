import yaml
from pathlib import Path

def load_config(config_path: str = "config/parameters.yaml") -> dict:
    """Load the system configuration parameters."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
