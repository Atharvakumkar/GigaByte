import json
from datetime import datetime


def generate_audit_log(
    target,
    media_type,
    method,
    pre_hash,
    verification_status,
    start_time,
    end_time
):

    audit_data = {
        "target": target,
        "media_type": media_type,
        "method": method,
        "start_time": start_time,
        "end_time": end_time,
        "pre_sanitization_sha256": pre_hash,
        "sanitization_status": "COMPLETED",
        "verification_status": verification_status,
        "result": "SUCCESS" if verification_status == "PASSED" else "FAILED"
    }

    with open("audit_log.json", "w") as file:
        json.dump(audit_data, file, indent=4)

    return audit_data