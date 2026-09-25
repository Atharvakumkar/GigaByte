import os
import mmap

class RawCarver:
    def __init__(self, image_path: str, output_dir: str = "recovered"):
        self.image_path = image_path
        self.output_dir = output_dir
        self.carved_count = 0
        
        # 15 MB limit to prevent runaway files from swallowing the disk
        self.max_file_size = 40 * 1024 * 1024 
        
        self.signatures = {
            "jpg": (b'\xFF\xD8\xFF', b'\xFF\xD9', 2),
            "png": (b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', b'IEND', 8),
            "pdf": (b'%PDF-', b'%%EOF', 5) 
        }

    def scan_image(self):
        print(f"[*] Starting size-limited raw carving on: {self.image_path}")
        
        try:
            with open(self.image_path, 'rb') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    offset = 0
                    file_size = len(mm)
                    
                    while offset < file_size:
                        earliest_idx = -1
                        matched_ext = None
                        matched_header = None
                        matched_footer = None
                        matched_footer_len = 0
                        
                        # Find the absolute closest header of any type
                        for ext, (header, footer, footer_len) in self.signatures.items():
                            idx = mm.find(header, offset)
                            if idx != -1:
                                if earliest_idx == -1 or idx < earliest_idx:
                                    earliest_idx = idx
                                    matched_ext = ext
                                    matched_header = header
                                    matched_footer = footer
                                    matched_footer_len = footer_len
                        
                        if earliest_idx == -1:
                            break # No more files found
                            
                        # Search for the footer ONLY within the max_file_size limit
                        search_limit = min(earliest_idx + self.max_file_size, file_size)
                        end_idx = mm.find(matched_footer, earliest_idx, search_limit)
                        
                        if end_idx != -1:
                            end_idx += matched_footer_len
                            file_data = mm[earliest_idx:end_idx]
                            
                            self.carved_count += 1
                            filename = f"carved_{self.carved_count:03d}.{matched_ext}"
                            filepath = os.path.join(self.output_dir, filename)
                            
                            with open(filepath, 'wb') as out_file:
                                out_file.write(file_data)
                                
                            print(f"[+] Recovered: {filename} (Size: {len(file_data)} bytes) at offset {earliest_idx}")
                            
                            # Jump offset past this recovered file
                            offset = earliest_idx + len(matched_header)
                        else:
                            # Footer not found within limit. 
                            # Move just past the header to keep searching so we don't miss embedded files.
                            offset = earliest_idx + len(matched_header)

            print(f"[*] Scan complete. Total files recovered: {self.carved_count}")

        except FileNotFoundError:
            print(f"[-] Error: Disk image '{self.image_path}' not found.")

if __name__ == "__main__":
    carver = RawCarver("evidence.img")
    carver.scan_image() 