import sys
from datetime import datetime

from media_classifier import classify_media
from method_recommender import recommend_method
from safety import safety_check
from hashing import calculate_sha256
from sanitizer import sanitize_file
from verification import verify_sanitization
from audit_logger import generate_audit_log


def main():

    if len(sys.argv) != 2:
        print("Usage: python main.py <test_image>")
        return

    target = sys.argv[1]

    print("\n========================================")
    print("     TEAM 1 SANITIZATION ENGINE")
    print("========================================")

    print(f"Target: {target}")

    # 1. Media Classification
    media_type = classify_media(target)
    print(f"[✓] Media Classification → {media_type}")

    # 2. Method Recommendation
    method = recommend_method(media_type)
    print(f"[✓] Method Recommendation → {method}")

    # 3. Safety Check
    safe, message = safety_check(target)

    if not safe:
        print(f"[✗] {message}")
        return

    print("[✓] Safety Check → PASSED")

    # Start Time
    start_time = datetime.now().isoformat()

    # 4. Pre-Sanitization Hash
    pre_hash = calculate_sha256(target)
    print(f"[✓] Pre-Sanitization SHA-256 → {pre_hash}")

    # 5. Sanitization
    sanitize_file(target)
    print("[✓] Sanitization → COMPLETED")

    # 6. Verification
    verified = verify_sanitization(target)

    if verified:
        verification_status = "PASSED"
        print("[✓] Verification → PASSED")
    else:
        verification_status = "FAILED"
        print("[✗] Verification → FAILED")

    # End Time
    end_time = datetime.now().isoformat()

    # 7. Audit Log
    generate_audit_log(
        target,
        media_type,
        method,
        pre_hash,
        verification_status,
        start_time,
        end_time
    )

    print("[✓] Audit Log → audit_log.json")

    print("========================================")

    if verified:
        print("STATUS: SUCCESS")
    else:
        print("STATUS: FAILED")

    print("========================================")


if __name__ == "__main__":
    main()