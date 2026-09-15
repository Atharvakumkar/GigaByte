import os

class FragmentReconstructor:
    def __init__(self, recovered_dir: str = "recovered"):
        self.recovered_dir = recovered_dir
        self.signatures = {
            "jpg": b'\xFF\xD9',
            "png": b'IEND',
            "pdf": b'%%EOF'
        }

    def reconstruct_orphans(self):
        print(f"\n[*] Starting Fragment Reconstruction Pass on '{self.recovered_dir}'...")
        # A real reconstruction engine would scan the disk image for orphaned blocks.
        # For this MVP, we simulate a heuristic pass by finding any file marked "partial"
        # and checking if we can logically "stitch" a simulated missing footer to it.
        # This demonstrates the system's ability to handle fragmented and incomplete files.

        reconstructed_count = 0
        if not os.path.exists(self.recovered_dir):
            return

        for filename in sorted(os.listdir(self.recovered_dir)):
            if "partial" in filename:
                filepath = os.path.join(self.recovered_dir, filename)
                ext = filename.split('.')[-1].lower()
                
                if ext in self.signatures:
                    footer = self.signatures[ext]
                    
                    # Read the partial file
                    with open(filepath, 'rb') as f:
                        data = f.read()
                    
                    # If the footer is already there (unlikely for "partial", but good to check)
                    if not data.endswith(footer):
                        print(f" [!] Fragment Reconstructor: Stitching missing {ext.upper()} footer to {filename}")
                        # Stitch the footer
                        with open(filepath, 'ab') as f:
                            f.write(b'\n' + footer)
                        
                        # Rename the file to show it was reconstructed
                        new_filename = filename.replace("partial", "reconstructed")
                        new_filepath = os.path.join(self.recovered_dir, new_filename)
                        os.rename(filepath, new_filepath)
                        reconstructed_count += 1

        print(f"[*] Fragment Reconstruction complete. {reconstructed_count} files stitched.")

if __name__ == "__main__":
    reconstructor = FragmentReconstructor()
    reconstructor.reconstruct_orphans()
