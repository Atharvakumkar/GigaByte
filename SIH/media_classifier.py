from pathlib import Path


DISK_IMAGE_EXTENSIONS = [".img", ".dd", ".raw"]
ISO_EXTENSIONS = [".iso"]


def classify_media(file_path):
    path = Path(file_path)

    extension = path.suffix.lower()

    if extension in DISK_IMAGE_EXTENSIONS:
        return "Disk Image"

    elif extension in ISO_EXTENSIONS:
        return "ISO Image"

    else:
        return "Unknown"