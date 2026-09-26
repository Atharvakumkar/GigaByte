from typing import List, Dict, Any

def compare_results(baseline_artifacts: List[Dict[str, Any]], post_artifacts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compares the pre-sanitization baseline with post-sanitization recovery results.
    """
    baseline_hashes = {a.get('sha256') for a in baseline_artifacts if a.get('sha256')}
    post_hashes = {a.get('sha256') for a in post_artifacts if a.get('sha256')}
    
    # Artifacts that were in the baseline AND are still recoverable
    surviving_artifacts = baseline_hashes.intersection(post_hashes)
    
    return {
        "pre_sanitization_count": len(baseline_artifacts),
        "post_sanitization_count": len(post_artifacts),
        "surviving_count": len(surviving_artifacts),
        "surviving_hashes": list(surviving_artifacts),
        "is_clean": len(surviving_artifacts) == 0
    }
