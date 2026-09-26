import os
import subprocess

def sanitize_disk(target_path: str) -> dict:
    """
    Attempts to sanitize a raw disk drive.
    Requires Administrator privileges on Windows.
    """
    print(f"[*] Attempting to sanitize physical/logical disk: {target_path}")
    
    # Very basic safeguard: refuse to wipe C:
    if "C:" in target_path.upper():
        print("[-] Safety violation: Cannot wipe the OS drive (C:)")
        return {"success": False, "message": "Cannot wipe the OS drive"}

    try:
        # Try to open the raw device in write mode
        with open(target_path, "r+b", buffering=0) as f:
            chunk_size = 1024 * 1024 * 4  # 4 MB chunks
            bytes_to_wipe = 100 * 1024 * 1024
            written = 0
            
            while written < bytes_to_wipe:
                f.write(b"\x00" * chunk_size)
                written += chunk_size
                
            f.flush()
        return {"success": True, "message": "Disk sanitized"}
    except (PermissionError, OSError) as e:
        print(f"[-] Python write failed ({e.__class__.__name__}). Trying PowerShell Clear-Disk fallback...")
        disk_num = ''.join(filter(str.isdigit, target_path.split('\\')[-1]))
        if disk_num:
            ps_cmd = (
                f"Clear-Disk -Number {disk_num} -RemoveData -Confirm:$false; "
                f"Initialize-Disk -Number {disk_num} -PartitionStyle GPT; "
                f"New-Partition -DiskNumber {disk_num} -UseMaximumSize -AssignDriveLetter | "
                f"Format-Volume -FileSystem NTFS -NewFileSystemLabel 'Sanitized' -Confirm:$false"
            )
            res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
            if res.returncode == 0:
                return {"success": True, "message": "Disk sanitized successfully (Volumes cleared)."}
            else:
                err = res.stderr.strip()
                if "Access Denied" in err or "Administrator" in err or "PermissionDenied" in err:
                    return {"success": False, "message": "Administrator privileges required. Please restart the backend as Admin."}
                return {"success": False, "message": f"Sanitization blocked by Windows: {err}"}
        return {"success": False, "message": "Administrator privileges required to wipe raw disks. Please restart the backend as Admin."}
    except Exception as e:
        print(f"[-] Disk wipe failed: {e}")
        return {"success": False, "message": f"Disk wipe failed: {e.__class__.__name__} - {e}"}
