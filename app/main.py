from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import subprocess
import json
from pydantic import BaseModel
import os

# Import our unified engine and validator
from recovery.engine import RecoveryEngine
from recovery.validator import FileValidator

app = FastAPI(title="SIH 2026 Data Recovery API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the expected JSON payload from the frontend
class RecoveryRequest(BaseModel):
    method: str  # Expecting "filesystem" or "carving"
    target: str = "evidence.img"  # Optional target drive path

@app.get("/api/drives")
def list_drives():
    drives = {"physical": [], "logical": []}
    try:
        # Get Physical Drives
        ps_cmd = "Get-Disk | Select-Object Number, FriendlyName, Size | ConvertTo-Json"
        result = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
        if result.stdout.strip():
            disks = json.loads(result.stdout)
            if isinstance(disks, dict):
                disks = [disks]
            for d in disks:
                if d.get("Number") is not None:
                    size_gb = round(d.get("Size", 0) / (1024**3), 2) if d.get("Size") else 0
                    drives["physical"].append({
                        "id": f"\\\\.\\PhysicalDrive{d['Number']}",
                        "name": d.get("FriendlyName", f"Physical Drive {d['Number']}"),
                        "size_gb": size_gb
                    })
                    
        # Get Logical Drives
        ps_cmd_logical = "Get-Volume | Where-Object DriveLetter -ne $null | Select-Object DriveLetter, FileSystemLabel, Size | ConvertTo-Json"
        res_logical = subprocess.run(["powershell", "-Command", ps_cmd_logical], capture_output=True, text=True)
        if res_logical.stdout.strip():
            vols = json.loads(res_logical.stdout)
            if isinstance(vols, dict):
                vols = [vols]
            for v in vols:
                if v.get("DriveLetter"):
                    size_gb = round(v.get("Size", 0) / (1024**3), 2) if v.get("Size") else 0
                    label = v.get("FileSystemLabel") or "Local Disk"
                    drives["logical"].append({
                        "id": f"\\\\.\\{v['DriveLetter']}:",
                        "name": f"{label} ({v['DriveLetter']}:)",
                        "size_gb": size_gb
                    })
    except Exception as e:
        print(f"Error getting drives: {e}")
        # fallback mock data
        drives = {
            "physical": [{"id": "\\\\.\\PhysicalDrive0", "name": "Fallback Generic HDD", "size_gb": 500}],
            "logical": [{"id": "\\\\.\\C:", "name": "Fallback OS (C:)", "size_gb": 500}]
        }
    return drives

@app.post("/api/upload")
def upload_disk_image(file: UploadFile = File(...)):
    try:
        os.makedirs("data", exist_ok=True)
        file_location = os.path.join("data", file.filename)
        import shutil
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return {"success": True, "target": file_location}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/recover")
def run_recovery_endpoint(request: RecoveryRequest):
    method = request.method.lower()
    target = request.target

    
    if method not in ["filesystem", "carving"]:
        raise HTTPException(status_code=400, detail="Invalid recovery method selected.")
    
    # 1. Initialize and run the engine on our target
    # NOTE: Using the raw drive path requires Admin privileges
    engine = RecoveryEngine(image_path=target, output_dir="recovered")
    engine.run_recovery(method)
    
    # 2. Gather the validation results to send back to the frontend
    validator = FileValidator("recovered")
    recovered_files_data = []
    
    if os.path.exists("recovered"):
        for filename in sorted(os.listdir("recovered")):
            filepath = os.path.join("recovered", filename)
            if os.path.isfile(filepath):
                status = validator.validate_file(filepath)
                size_mb = round(os.path.getsize(filepath) / (1024 * 1024), 2)
                
                recovered_files_data.append({
                    "filename": filename,
                    "size_mb": size_mb,
                    "status": status
                })
                
    return {
        "status": "success",
        "method_used": method,
        "total_recovered": len(recovered_files_data),
        "files": recovered_files_data
    }