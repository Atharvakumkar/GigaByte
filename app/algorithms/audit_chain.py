import hashlib
import json
import os
from datetime import datetime
from typing import Dict, Any

class AuditChain:
    def __init__(self, log_file: str = "data/audit_log.json"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        self.chain = self._load_chain()
        
    def _load_chain(self) -> list:
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
        
    def _save_chain(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.chain, f, indent=4)
            
    def _hash_event(self, event_data: dict, previous_hash: str) -> str:
        # Create a deterministic string representation of the event
        event_str = json.dumps(event_data, sort_keys=True)
        combined = f"{previous_hash}{event_str}".encode('utf-8')
        return hashlib.sha256(combined).hexdigest()

    def log_event(self, action: str, details: Dict[str, Any]) -> str:
        previous_hash = self.chain[-1]["hash"] if self.chain else "GENESIS"
        
        event_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "details": details
        }
        
        current_hash = self._hash_event(event_data, previous_hash)
        
        log_entry = {
            "event": event_data,
            "previous_hash": previous_hash,
            "hash": current_hash
        }
        
        self.chain.append(log_entry)
        self._save_chain()
        return current_hash
        
    def verify_integrity(self) -> bool:
        """
        Recomputes the hashes for the entire chain to ensure no event was tampered with.
        """
        if not self.chain:
            return True
            
        previous_hash = "GENESIS"
        
        for entry in self.chain:
            event_data = entry["event"]
            expected_prev_hash = entry["previous_hash"]
            expected_hash = entry["hash"]
            
            if expected_prev_hash != previous_hash:
                return False
                
            recomputed = self._hash_event(event_data, previous_hash)
            if recomputed != expected_hash:
                return False
                
            previous_hash = recomputed
            
        return True
