from pathlib import Path


def safety_check(file_path):

    path = Path(file_path)

    # Target file must exist
    if not path.is_file():
        return False, "Safety Check Failed: Target file does not exist."

    # Target must be inside our test_data folder
    if "test_data" not in path.parts:
        return False, "Safety Check Failed: Target must be inside test_data folder."

    # Only allow controlled disk-image files
    if path.suffix.lower() not in [".img", ".dd", ".raw", ".iso"]:
        return False, "Safety Check Failed: Unsupported file type."

    # Prevent system-drive targets
    if path.drive.upper() in ["C:", "D:"]:
        return False, "Safety Check Failed: System/local drive target blocked."

    return True, "Safety Check Passed."