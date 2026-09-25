import os

class FileValidator:
    def __init__(self, recovered_dir: str = "recovered"):
        self.recovered_dir = recovered_dir

    def validate_file(self, filepath: str) -> str:
        if not os.path.exists(filepath):
            return "INVALID"
        
        if os.path.getsize(filepath) == 0:
            return "INVALID"

        with open(filepath, 'rb') as f:
            data = f.read()

        ext = filepath.split('.')[-1].lower()

        # Check JPEG: Must start with FF D8 and end with FF D9
        if ext == 'jpg':
            if data.startswith(b'\xFF\xD8') and data.endswith(b'\xFF\xD9'):
                return "VALID"
            elif data.startswith(b'\xFF\xD8'):
                return "PARTIAL"
            return "INVALID"
            
        # Check PNG: Must have signature and an IEND chunk near the end
        elif ext == 'png':
            if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A') and b'IEND' in data[-100:]:
                return "VALID"
            elif data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
                return "PARTIAL"
            return "INVALID"

        # Check PDF: Must have header and %%EOF near the end
        elif ext == 'pdf':
            # EOF marker might have trailing whitespace, so we check the last 1024 bytes
            if data.startswith(b'%PDF-') and b'%%EOF' in data[-1024:]:
                return "VALID"
            elif data.startswith(b'%PDF-'):
                return "PARTIAL"
            return "INVALID"
        
        return "UNKNOWN"

    def validate_all(self):
        print(f"[*] Starting validation on '{self.recovered_dir}' directory...")
        for filename in sorted(os.listdir(self.recovered_dir)):
            filepath = os.path.join(self.recovered_dir, filename)
            if os.path.isfile(filepath):
                status = self.validate_file(filepath)
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                print(f" -> {filename} ({size_mb:.2f} MB): {status}")

if __name__ == "__main__":
    validator = FileValidator()
    validator.validate_all()