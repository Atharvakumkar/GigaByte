import os
from datetime import datetime

class CertificateGenerator:
    def __init__(self, output_dir: str = "data/reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_certificate(self, target: str, pre_count: int, post_count: int, status: str, statement: str) -> str:
        timestamp = datetime.utcnow().isoformat().replace(":", "-")
        
        cert_content = f"""==================================================
          SANITIZATION CERTIFICATE
==================================================

Date/Time           : {timestamp}
Target              : {target}

Pre-Sanitization
Artifacts Recovered : {pre_count}

Post-Sanitization
Artifacts Recovered : {post_count}

Verification        : {status}

Statement:
{statement}

==================================================
"""
        filename = f"certificate_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(cert_content)
            
        return filepath
