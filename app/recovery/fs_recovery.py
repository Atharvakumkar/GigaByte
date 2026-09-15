import subprocess
import os

class FilesystemRecovery:
    def __init__(self, image_path: str, output_dir: str = "recovered"):
        self.image_path = image_path
        self.output_dir = output_dir

    def get_image_info(self):
        print(f"[*] Extracting filesystem info from {self.image_path}...")
        try:
            result = subprocess.run(['fsstat', self.image_path], capture_output=True, text=True, check=True)
            info = {}
            for line in result.stdout.split('\n'):
                if line.startswith('File System Type:'):
                    info['Filesystem'] = line.split(':')[1].strip()
                elif line.startswith('Sector Size:'):
                    info['Sector Size'] = line.split(':')[1].strip()
            return info
        except Exception as e:
            print(f"[-] Error: {e}")
            return None

    def recover_files(self):
        print(f"\n[*] Starting Filesystem Recovery (Sleuth Kit) on: {self.image_path}")
        
        try:
            # 1. Use fls to list all files recursively (-r) with full paths (-p)
            fls_cmd = ['fls', '-r', '-p', self.image_path]
            result = subprocess.run(fls_cmd, capture_output=True, text=True, check=True)
            
            recovery_count = 0
            for line in result.stdout.split('\n'):
                if not line.strip():
                    continue
                    
                # We only want regular files (denoted by 'r/r' in Sleuth Kit)
                if line.startswith('r/r'):
                    meta_part, name_part = line.split(':', 1)
                    original_name = os.path.basename(name_part.strip())
                    inode_str = meta_part.split()[-1]
                    
                    filepath = os.path.join(self.output_dir, f"fs_{original_name}")
                    
                    with open(filepath, 'wb') as out_file:
                        subprocess.run(['icat', self.image_path, inode_str], stdout=out_file, check=True)
                        
                    print(f"[+] Recovered: fs_{original_name} (Inode: {inode_str})")
                    recovery_count += 1
                    
            print(f"[*] Filesystem Recovery complete. Total files recovered: {recovery_count}")

        except subprocess.CalledProcessError as e:
            print(f"[-] Sleuth Kit error: {e}")

if __name__ == "__main__":
    fs_rec = FilesystemRecovery("evidence.img")
    fs_rec.get_image_info()
    fs_rec.recover_files()