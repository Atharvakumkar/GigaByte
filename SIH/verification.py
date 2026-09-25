from pathlib import Path


def verify_sanitization(file_path):

    path = Path(file_path)

    file_size = path.stat().st_size

    if file_size == 0:
        return False

    chunk_size = 1024 * 1024

    with open(path, "rb") as file:
        remaining = file_size

        while remaining > 0:
            size = min(chunk_size, remaining)
            data = file.read(size)

            if data != b"\x00" * size:
                return False

            remaining -= size

    return True