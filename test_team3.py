
from app.algorithms.confidence import calculate_confidence
from app.algorithms.recoverability import calculate_recoverability_score
from app.algorithms.baseline import BaselineManager
from app.algorithms.comparison import compare_results
from app.algorithms.verification import verify_sanitization_outcome
from app.algorithms.audit_chain import AuditChain

print("Testing Confidence:")
print(calculate_confidence("VALID", True))

print("\nTesting Recoverability:")
print(calculate_recoverability_score(2048 * 1024, "VALID"))

print("\nTesting Baseline & Comparison:")
bm = BaselineManager("data/test_baseline.json")
pre = [{"id": 1, "sha256": "hash1"}, {"id": 2, "sha256": "hash2"}]
bm.create_baseline("test.img", pre)
post = [{"id": 2, "sha256": "hash2"}]
comp = compare_results(pre, post)
print(comp)

print("\nTesting Verification:")
print(verify_sanitization_outcome(comp))

print("\nTesting Audit Chain:")
audit = AuditChain("data/test_audit.json")
audit.log_event("TEST_START", {"file": "test.img"})
audit.log_event("TEST_END", {"status": "SUCCESS"})
print(f"Integrity Valid: {audit.verify_integrity()}")

