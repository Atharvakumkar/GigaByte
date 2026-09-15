import os
import subprocess

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.recovery.engine import RecoveryEngine
from app.recovery.validator import FileValidator


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Secure Data Sanitization and File Recovery System",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
RECOVERED_DIR = os.path.join(BASE_DIR, "recovered")


os.makedirs(RECOVERED_DIR, exist_ok=True)


# ============================================================
# SERVE FRONTEND
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


@app.get("/")
def serve_frontend():
    return FileResponse(
        os.path.join(FRONTEND_DIR, "index.html")
    )


# ============================================================
# REQUEST MODELS
# ============================================================

class RecoveryRequest(BaseModel):
    method: str
    drive: str


# ============================================================
# CONTROLLED EVIDENCE IMAGES
# ============================================================

EVIDENCE_IMAGES = {
    "sihtest": {
        "id": "sihtest",
        "name": "SIH Test Evidence Image (test.img)",
        "filename": "test.img"
    }
}


# ============================================================
# ROOT / HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "service": "Secure File Recovery Engine"
    }


# ============================================================
# LIST AVAILABLE EVIDENCE IMAGES
# ============================================================

@app.get("/api/drives")
def get_drives():
    return list(EVIDENCE_IMAGES.values())


# ============================================================
# DISK IMAGE INFORMATION
# ============================================================

@app.get("/api/image-info/{drive_id}")
def get_image_info(drive_id: str):

    if drive_id not in EVIDENCE_IMAGES:
        raise HTTPException(
            status_code=404,
            detail="Evidence image not found."
        )

    image_name = EVIDENCE_IMAGES[drive_id]["filename"]
    image_path = os.path.join(BASE_DIR, image_name)

    if not os.path.exists(image_path):
        raise HTTPException(
            status_code=404,
            detail=f"Evidence image '{image_name}' does not exist."
        )

    try:

        result = subprocess.run(
            ["fsstat", image_path],
            capture_output=True,
            text=True,
            timeout=30,
            check=False
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Sleuth Kit 'fsstat' command was not found."
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=500,
            detail="Filesystem analysis timed out."
        )

    if result.returncode != 0:

        error_message = (
            result.stderr.strip()
            or "Unable to determine filesystem information."
        )

        raise HTTPException(
            status_code=400,
            detail=error_message
        )

    output = result.stdout

    # --------------------------------------------------------
    # Helper function
    # --------------------------------------------------------

    def get_value(label):

        for line in output.splitlines():

            if line.startswith(label):

                value = line[len(label):].strip()

                if value:
                    return value

        return "N/A"

    # --------------------------------------------------------
    # Basic information
    # --------------------------------------------------------

    filesystem = get_value("File System Type:")
    volume_id = get_value("Volume ID:")

    last_written = get_value("Last Written at:")
    last_checked = get_value("Last Checked at:")
    last_mounted = get_value("Last Mounted at:")

    mounted_on = get_value("Last mounted on:")
    source_os = get_value("Source OS:")

    # --------------------------------------------------------
    # Mount status
    # --------------------------------------------------------

    mount_status = "Unknown"

    if "Unmounted properly" in output:
        mount_status = "Unmounted properly"

    elif "Unmounted improperly" in output:
        mount_status = "Unmounted improperly"

    # --------------------------------------------------------
    # Filesystem features
    # --------------------------------------------------------

    compat_features = get_value("Compat Features:")
    incompat_features = get_value("InCompat Features:")
    readonly_features = get_value(
        "Read Only Compat Features:"
    )

    filesystem_features = []

    if compat_features != "N/A":
        filesystem_features.append(compat_features)

    if incompat_features != "N/A":
        filesystem_features.append(incompat_features)

    if readonly_features != "N/A":
        filesystem_features.append(readonly_features)

    # --------------------------------------------------------
    # Technical information
    # --------------------------------------------------------

    journal_id = get_value("Journal ID:")
    journal_inode = get_value("Journal Inode:")

    inode_range = get_value("Inode Range:")
    inode_size = get_value("Inode Size:")

    block_range = get_value("Block Range:")
    block_size = get_value("Block Size:")

    free_inodes = get_value("Free Inodes:")
    free_blocks = get_value("Free Blocks:")

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "status": "success",

        "image": {
            "id": drive_id,
            "name": EVIDENCE_IMAGES[drive_id]["name"],
            "filename": image_name
        },

        "filesystem": filesystem,

        "volume_id": volume_id,

        "source_os": source_os,

        "mount_status": mount_status,

        "last_written": last_written,

        "last_checked": last_checked,

        "last_mounted": last_mounted,

        "mounted_on": mounted_on,

        "filesystem_features": filesystem_features,

        "technical_details": {
            "journal_id": journal_id,
            "journal_inode": journal_inode,
            "inode_range": inode_range,
            "inode_size": inode_size,
            "block_range": block_range,
            "block_size": block_size,
            "free_inodes": free_inodes,
            "free_blocks": free_blocks
        }
    }


# ============================================================
# FILE RECOVERY
# ============================================================

@app.post("/api/recover")
def recover_files(request: RecoveryRequest):

    # --------------------------------------------------------
    # Validate recovery method
    # --------------------------------------------------------

    allowed_methods = {
        "filesystem",
        "carving"
    }

    method = request.method.lower().strip()

    if method not in allowed_methods:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid recovery method. "
                "Choose 'filesystem' or 'carving'."
            )
        )

    # --------------------------------------------------------
    # Validate evidence image
    # --------------------------------------------------------

    if request.drive not in EVIDENCE_IMAGES:

        raise HTTPException(
            status_code=404,
            detail="Evidence image not found."
        )

    image_name = EVIDENCE_IMAGES[
        request.drive
    ]["filename"]

    image_path = os.path.join(
        BASE_DIR,
        image_name
    )

    if not os.path.exists(image_path):

        raise HTTPException(
            status_code=404,
            detail=f"Evidence image '{image_name}' not found."
        )

    # --------------------------------------------------------
    # Create recovery engine
    # --------------------------------------------------------

    try:

        engine = RecoveryEngine(
            image_path=image_path,
            output_dir=RECOVERED_DIR
        )

        # IMPORTANT:
        # The user explicitly selects the recovery method.
        # There is NO automatic filesystem -> carving fallback.

        recovered_metadata = engine.run_recovery(
            method
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    validator = FileValidator(
        RECOVERED_DIR
    )

    validation_results = validator.validate_all()

    # --------------------------------------------------------
    # Build lookup table for validation results
    # --------------------------------------------------------

    validation_lookup = {}

    if validation_results:

        for result in validation_results:

            if isinstance(result, dict):

                filename = result.get("filename")

                if filename:
                    validation_lookup[
                        filename
                    ] = result

    # --------------------------------------------------------
    # Build final response
    # --------------------------------------------------------

    files = []

    for metadata in recovered_metadata:

        filename = metadata.get(
            "filename",
            "unknown"
        )

        validation = validation_lookup.get(
            filename,
            {}
        )

        status = validation.get(
            "status",
            metadata.get(
                "status",
                "RECOVERED"
            )
        )

        score = validation.get(
            "score",
            0
        )

        size = metadata.get(
            "size",
            0
        )

        hash_val = validation.get("hash", "N/A")

        files.append({

            "filename": filename,

            "type": metadata.get(
                "type",
                "unknown"
            ),

            "method": metadata.get(
                "method",
                method
            ),

            "offset": metadata.get(
                "offset",
                0
            ),

            "size": size,

            "size_mb": round(
                size / (1024 * 1024),
                2
            ),

            "status": status,

            "score": score,
            
            "hash": hash_val
        })

    # --------------------------------------------------------
    # Return API response
    # --------------------------------------------------------

    return {

        "status": "success",

        "method_used": method,

        "total_recovered": len(files),

        "files": files
    }


# ============================================================
# RECOVERY REPORT
# ============================================================

@app.get("/api/report")
def generate_report():

    recovered_files = []

    if os.path.exists(RECOVERED_DIR):

        for filename in os.listdir(
            RECOVERED_DIR
        ):

            filepath = os.path.join(
                RECOVERED_DIR,
                filename
            )

            if os.path.isfile(filepath):

                recovered_files.append({

                    "filename": filename,

                    "size": os.path.getsize(
                        filepath
                    )
                })

    return {

        "status": "success",

        "total_files": len(
            recovered_files
        ),

        "files": recovered_files
    }
