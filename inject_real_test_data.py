import os

image_path = 'evidence.img'
test_data_dir = 'test_data'

files_to_inject = [
    ("sunflower.jpg", 1000000),      # offset 1MB
    ("IMG_1794.png", 5000000),       # offset 5MB
    ("SIH_test.pdf", 45000000)       # offset 45MB
]

def inject_real_files():
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found.")
        return

    with open(image_path, "r+b") as img_file:
        for filename, offset in files_to_inject:
            src_path = os.path.join(test_data_dir, filename)
            if not os.path.exists(src_path):
                print(f"[-] Warning: {src_path} not found. Skipping.")
                continue
                
            with open(src_path, "rb") as src_file:
                data = src_file.read()
                
                # For the PDF, let's intentionally corrupt it (remove the last 10 bytes)
                # so the fragment reconstructor gets triggered, just to show off the feature!
                if filename.endswith(".pdf"):
                    data = data[:-10]
                    print(f"[*] Intentionally corrupted {filename} to demonstrate Fragment Reconstruction!")
                    
                img_file.seek(offset)
                img_file.write(data)
                print(f"[+] Injected {filename} ({len(data)} bytes) at offset {offset}")

if __name__ == "__main__":
    inject_real_files()
