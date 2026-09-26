from typing import Dict, Any

def calculate_recoverability_score(file_size: int, validation_status: str) -> Dict[str, Any]:
    """
    Summarizes how recoverable an artifact is.
    This metric combines file size (meaningfulness of the artifact) and its structural integrity.
    """
    # Base score out of 10
    score = 0.0
    
    if validation_status.upper() == "VALID":
        score += 7.0
    elif validation_status.upper() == "PARTIAL":
        score += 3.0
        
    # Reward larger files up to a point, as they represent more substantial recovered data
    if file_size > 1024 * 1024:  # > 1MB
        score += 3.0
    elif file_size > 1024:       # > 1KB
        score += 1.5
    elif file_size > 0:
        score += 0.5
        
    score = min(score, 10.0)
    
    return {
        "recoverability_score": score,
        "max_score": 10.0,
        "category": "HIGH" if score >= 7.0 else "MEDIUM" if score >= 4.0 else "LOW"
    }
