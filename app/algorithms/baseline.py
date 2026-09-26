import json
import os
from typing import List, Dict, Any

class BaselineManager:
    def __init__(self, baseline_path: str = "data/baseline.json"):
        self.baseline_path = baseline_path
        os.makedirs(os.path.dirname(self.baseline_path), exist_ok=True)
        
    def create_baseline(self, target: str, recovered_artifacts: List[Dict[str, Any]]) -> dict:
        """
        Creates and saves a pre-sanitization baseline of recovered artifacts.
        """
        baseline_data = {
            "target": target,
            "artifact_count": len(recovered_artifacts),
            "artifacts": recovered_artifacts
        }
        
        with open(self.baseline_path, 'w') as f:
            json.dump(baseline_data, f, indent=4)
            
        return baseline_data
        
    def load_baseline(self) -> dict:
        """
        Loads the most recent baseline.
        """
        if not os.path.exists(self.baseline_path):
            return None
            
        with open(self.baseline_path, 'r') as f:
            return json.load(f)
