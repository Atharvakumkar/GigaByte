import os
import base64

image_path = 'evidence.img'

# Valid 1x1 JPG
jpg_b64 = "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="

# Valid 1x1 PNG
png_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

# Valid empty PDF
pdf_b64 = "JVBERi0xLjAKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFszIDAgUl0KL0NvdW50IDEKPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1BhcmVudCAyIDAgUgovTWVkaWFCb3ggWzAgMCAxMDAgMTAwXQo+PgplbmRvYmoKeHJlZgowIDQKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDEwIDAwMDAwIG4gCjAwMDAwMDAwNjAgMDAwMDAgbiAKMDAwMDAwMDExNyAwMDAwMCBuIAp0cmFpbGVyCjwwCi9TaXplIDQKL1Jvb3QgMSAwIFIKPj4Kc3RhcnR4cmVmCjE5OQolJUVPRg=="

def inject_files(image_path):
    with open(image_path, "r+b") as f:
        # 1. Inject valid JPG at offset 1000
        f.seek(1000)
        f.write(base64.b64decode(jpg_b64))
        
        # 2. Inject valid PNG at offset 5000
        f.seek(5000)
        f.write(base64.b64decode(png_b64))
        
        # 3. Inject Corrupted PDF at offset 10000
        # We decode the valid PDF and remove the "%%EOF" from the end so it's corrupted.
        pdf_data = base64.b64decode(pdf_b64)
        corrupted_pdf_data = pdf_data.replace(b"%%EOF", b"")
        
        f.seek(10000)
        f.write(corrupted_pdf_data)
        
        print("Successfully injected REAL, viewable files (including a corrupted one) into evidence.img")

if __name__ == "__main__":
    if os.path.exists(image_path):
        inject_files(image_path)
    else:
        print("evidence.img not found")
