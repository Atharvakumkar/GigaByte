import os
import base64

drives = [
    {"id": "drive_c", "name": "Local Disk (C:)", "filename": "drive_c.img"},
    {"id": "drive_d", "name": "Data (D:)", "filename": "drive_d.img"},
    {"id": "drive_e", "name": "USB Drive (E:)", "filename": "drive_e.img"}
]

# Base64 for the dummy files (from inject_dummy_files.py)
jpg_b64 = "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="
png_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
pdf_b64 = "JVBERi0xLjAKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFszIDAgUl0KL0NvdW50IDEKPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1BhcmVudCAyIDAgUgovTWVkaWFCb3ggWzAgMCAxMDAgMTAwXQo+PgplbmRvYmoKeHJlZgowIDQKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDEwIDAwMDAwIG4gCjAwMDAwMDAwNjAgMDAwMDAgbiAKMDAwMDAwMDExNyAwMDAwMCBuIAp0cmFpbGVyCjwwCi9TaXplIDQKL1Jvb3QgMSAwIFIKPj4Kc3RhcnR4cmVmCjE5OQolJUVPRg=="

def inject_dummy_files(filepath):
    # 50MB of zeroes
    size = 50 * 1024 * 1024
    print(f"Creating {filepath} ({size} bytes)...")
    
    with open(filepath, "wb") as f:
        # Write mostly zeros, but inject the files at specific offsets
        f.seek(size - 1)
        f.write(b"\0")
    
    # Now inject
    with open(filepath, "r+b") as f:
        f.seek(1000)
        f.write(base64.b64decode(jpg_b64))
        
        f.seek(5000)
        f.write(base64.b64decode(png_b64))
        
        pdf_data = base64.b64decode(pdf_b64)
        corrupted_pdf_data = pdf_data.replace(b"%%EOF", b"")
        
        f.seek(10000)
        f.write(corrupted_pdf_data)
        
    print(f"Successfully injected dummy files into {filepath}")

if __name__ == "__main__":
    for drive in drives:
        inject_dummy_files(drive["filename"])
    print("All simulated drives created successfully.")
