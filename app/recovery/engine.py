import os
import sys

# Ensure Python can find our modules when running directly
sys.path.append(os.path.dirname(__file__))

from .carver import RawCarver
from .fs_recovery import FilesystemRecovery
from .validator import FileValidator


class RecoveryEngine:
    def __init__(self, image_path: str, output_dir: str = "recovered"):
        # Resolve image_path to an absolute path relative to project root if needed
        if not os.path.isabs(image_path):
            project_root = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..")
            )
            image_path = os.path.join(project_root, image_path)

        image_path = os.path.abspath(image_path)

        if not os.path.exists(image_path):
            raise FileNotFoundError(
                f"Forensic image '{image_path}' not found."
            )

        self.image_path = image_path
        self.output_dir = output_dir

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def run_recovery(self, method: str):
        print("\n========================================")
        print("[*] INITIALIZING RECOVERY ENGINE")
        print(f"[*] SELECTED METHOD: {method.upper()}")
        print("========================================")

        recovered_files = []

        # Clear previous recoveries for a clean run
        for f in os.listdir(self.output_dir):
            filepath = os.path.join(self.output_dir, f)

            if os.path.isfile(filepath):
                os.remove(filepath)

        # 1. Run the selected recovery method
        if method == "filesystem":
            fs_engine = FilesystemRecovery(
                self.image_path,
                self.output_dir
            )

            fs_engine.recover_files()

        elif method == "carving":
            carver_engine = RawCarver(
                self.image_path,
                self.output_dir
            )

            recovered_files = carver_engine.scan_image()

        else:
            print("[-] Error: Unknown recovery method.")
            return []

        # 2. Automatically validate the recovered files
        print("\n[*] Running Validation Engine...")

        validator = FileValidator(self.output_dir)
        validator.validate_all()

        print("========================================\n")

        # Return structured recovery metadata
        return recovered_files


if __name__ == "__main__":
    # Resolve the forensic image path relative to the project root
    image_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "evidence.img"
        )
    )

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Forensic image '{image_path}' not found."
        )

    engine = RecoveryEngine(image_path)

    # Test Route 1: Filesystem Recovery
    engine.run_recovery("filesystem")

    # Test Route 2: Raw Carving
    engine.run_recovery("carving")
