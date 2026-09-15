import os
import mmap


class RawCarver:
    def __init__(self, image_path: str, output_dir: str = "recovered"):
        self.image_path = image_path
        self.output_dir = output_dir
        self.carved_count = 0

        # 40 MB limit to prevent runaway files from swallowing the disk
        self.max_file_size = 40 * 1024 * 1024

        self.signatures = {
            "jpg": (b'\xFF\xD8\xFF', b'\xFF\xD9', 2),
            "png": (b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', b'\x00\x00\x00\x00IEND\xae\x42\x60\x82', 12),
            "pdf": (b'%PDF-', b'%%EOF', 5)
        }

    def scan_image(self):
        print(f"[*] Starting size-limited raw carving on: {self.image_path}")

        recovered_files = []

        try:
            with open(self.image_path, 'rb') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    offset = 0
                    file_size = len(mm)

                    while offset < file_size:
                        earliest_idx = -1
                        matched_ext = None
                        matched_header = None
                        matched_footer = None
                        matched_footer_len = 0

                        # Find the closest header of any supported file type
                        for ext, (header, footer, footer_len) in self.signatures.items():
                            idx = mm.find(header, offset)

                            if idx != -1:
                                if earliest_idx == -1 or idx < earliest_idx:
                                    earliest_idx = idx
                                    matched_ext = ext
                                    matched_header = header
                                    matched_footer = footer
                                    matched_footer_len = footer_len

                        # No more supported file signatures found
                        if earliest_idx == -1:
                            break

                        # Search for the footer only within the maximum
                        # allowed file size
                        search_limit = min(
                            earliest_idx + self.max_file_size,
                            file_size
                        )

                        end_idx = mm.find(
                            matched_footer,
                            earliest_idx,
                            search_limit
                        )

                        # -------------------------------------------------
                        # COMPLETE FILE RECOVERY
                        # -------------------------------------------------
                        if end_idx != -1:
                            end_idx += matched_footer_len

                            file_data = mm[earliest_idx:end_idx]

                            self.carved_count += 1

                            filename = (
                                f"carved_{self.carved_count:03d}."
                                f"{matched_ext}"
                            )

                            filepath = os.path.join(
                                self.output_dir,
                                filename
                            )

                            with open(filepath, 'wb') as out_file:
                                out_file.write(file_data)

                            print(
                                f"[+] Recovered: {filename} "
                                f"(Size: {len(file_data)} bytes) "
                                f"at offset {earliest_idx}"
                            )

                            recovered_files.append({
                                "filename": filename,
                                "type": matched_ext,
                                "method": "carving",
                                "offset": earliest_idx,
                                "size": len(file_data),
                                "status": "RECOVERED"
                            })

                            # Jump past the recovered file.
                            # This prevents signatures embedded inside
                            # the recovered file from being carved again.
                            offset = end_idx

                        # -------------------------------------------------
                        # PARTIAL FILE RECOVERY
                        # -------------------------------------------------
                        else:
                            # Footer was not found within the maximum
                            # allowed size.
                            #
                            # We currently extract a fixed 1 MB block
                            # and mark it as partial.
                            fallback_size = min(
                                1024 * 1024,
                                file_size - earliest_idx
                            )

                            file_data = mm[
                                earliest_idx:
                                earliest_idx + fallback_size
                            ]

                            self.carved_count += 1

                            filename = (
                                f"carved_partial_"
                                f"{self.carved_count:03d}."
                                f"{matched_ext}"
                            )

                            filepath = os.path.join(
                                self.output_dir,
                                filename
                            )

                            with open(filepath, 'wb') as out_file:
                                out_file.write(file_data)

                            print(
                                f"[!] Recovered (Partial): {filename} "
                                f"(Size: {len(file_data)} bytes) "
                                f"at offset {earliest_idx}"
                            )

                            recovered_files.append({
                                "filename": filename,
                                "type": matched_ext,
                                "method": "carving",
                                "offset": earliest_idx,
                                "size": len(file_data),
                                "status": "PARTIAL"
                            })

                            # Move past the header so the scan can
                            # continue looking for other files.
                            offset = earliest_idx + len(matched_header)

            print(
                f"[*] Scan complete. "
                f"Total files recovered: {self.carved_count}"
            )

            return recovered_files

        except FileNotFoundError:
            print(
                f"[-] Error: Disk image '{self.image_path}' not found."
            )

            return []

        except Exception as e:
            print(f"[-] Carving error: {e}")

            return []


if __name__ == "__main__":
    carver = RawCarver("evidence.img")
    results = carver.scan_image()

    print("\n[*] Recovery Metadata:")

    for result in results:
        print(result)
