import os
import sys

from app.main import run_recovery_endpoint
from pydantic import BaseModel

class MockRequest(BaseModel):
    method: str

def test():
    req = MockRequest(method="carving")
    print("[*] Running API Endpoint locally for testing...")
    response = run_recovery_endpoint(req)
    print("Response Status:", response.get('status'))
    print(f"Total Recovered: {response.get('total_recovered')}")
    for f in response.get('files', []):
        print(f"  - {f['filename']} (Status: {f['status']}, Score: {f['score']})")

if __name__ == "__main__":
    test()
