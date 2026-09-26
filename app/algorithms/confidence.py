from typing import Dict, Any

def calculate_confidence(validation_status: str, has_fs_metadata: bool = False) -> Dict[str, Any]:
    """
    Calculates the recovery confidence based on forensic evidence.
    Returns a dict with the score and explainable reasons.
    """
    reasons = []
    score = 0.0
    
    if validation_status.upper() == "VALID":
        score += 80.0
        reasons.append("Valid file signature and structure detected")
    elif validation_status.upper() == "PARTIAL":
        score += 40.0
        reasons.append("Partial file structure / valid header but invalid footer")
    else:
        reasons.append("Invalid or unrecognized file structure")
        
    if has_fs_metadata:
        score += 20.0
        reasons.append("Corroborated by filesystem metadata")
        
    # Cap at 100%
    score = min(score, 100.0)
    
    return {
        "confidence_score": score,
        "reasons": reasons,
        "is_high_confidence": score >= 80.0
    }
