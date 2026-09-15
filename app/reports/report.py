import os
import hashlib
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

class ForensicReportGenerator:
    def __init__(self, output_pdf: str = "forensic_report.pdf", recovered_dir: str = "recovered"):
        self.output_pdf = output_pdf
        self.recovered_dir = recovered_dir

    def hash_file(self, filepath: str) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            return f"ERROR: {str(e)}"

    def generate_report(self, recovery_data: list, method_used: str):
        """
        recovery_data format:
        [{"filename": "carved_001.jpg", "size_mb": 1.2, "status": "VALID", "score": 100}, ...]
        """
        c = canvas.Canvas(self.output_pdf, pagesize=letter)
        width, height = letter
        
        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "SIH 2026 - Digital Forensics & Data Sanitization")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 70, "Consolidated Forensic Recovery Report")
        c.drawString(50, height - 90, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(50, height - 110, f"Extraction Method: {method_used.upper()}")
        
        c.line(50, height - 120, width - 50, height - 120)
        
        y = height - 140
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Recovered Evidence & Tamper-Evident Hash Log")
        y -= 20
        
        c.setFont("Helvetica", 9)
        
        for item in recovery_data:
            if y < 100:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 9)
                
            filename = item.get("filename", "Unknown")
            status = item.get("status", "UNKNOWN")
            score = item.get("score", 0)
            size = item.get("size_mb", 0)
            
            filepath = os.path.join(self.recovered_dir, filename)
            file_hash = self.hash_file(filepath) if os.path.exists(filepath) else "FILE_MISSING"
            
            # Format entry
            if status == "VALID":
                c.setFillColor(colors.darkgreen)
            elif status == "PARTIAL":
                c.setFillColor(colors.darkorange)
            else:
                c.setFillColor(colors.darkred)
                
            c.drawString(50, y, f"File: {filename} | Size: {size} MB | Status: {status} (Score: {score}/100)")
            c.setFillColor(colors.black)
            y -= 15
            c.drawString(70, y, f"SHA-256: {file_hash}")
            y -= 25

        c.save()
        print(f"[*] Forensic Report generated at: {self.output_pdf}")

if __name__ == "__main__":
    # Test
    gen = ForensicReportGenerator()
    dummy_data = [{"filename": "test.jpg", "size_mb": 0.5, "status": "VALID", "score": 100}]
    gen.generate_report(dummy_data, "test_method")
