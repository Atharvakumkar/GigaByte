from pathlib import Path


def sanitize_file(file_path):
    path = Path(file_path)

    file_size = path.stat().st_size
    chunk_size = 1024 * 1024

    with open(path, "r+b") as file:
        remaining = file_size

        while remaining > 0:
            size = min(chunk_size, remaining)
            file.write(b"\x00" * size)
            remaining -= size

        file.flush()

    return True