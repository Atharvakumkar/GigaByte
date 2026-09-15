import os
import hashlib


class FileValidator:

    def __init__(self, recovered_dir: str = "recovered"):
        self.recovered_dir = recovered_dir


    def validate_file(self, filepath: str) -> dict:

        if not os.path.exists(filepath):
            return {
                "status": "INVALID",
                "score": 0,
                "hash": "N/A"
            }


        if os.path.getsize(filepath) == 0:
            return {
                "status": "INVALID",
                "score": 0,
                "hash": "N/A"
            }


        with open(filepath, "rb") as f:
            data = f.read()
            
        file_hash = hashlib.sha256(data).hexdigest()


        ext = filepath.split(".")[-1].lower()


        # ====================================================
        # JPEG VALIDATION
        # ====================================================

        if ext == "jpg":

            if (
                data.startswith(b"\xFF\xD8")
                and data.endswith(b"\xFF\xD9")
            ):
                return {
                    "status": "VALID",
                    "score": 100,
                    "hash": file_hash
                }


            elif data.startswith(b"\xFF\xD8"):

                score = 50 if len(data) > 1024 else 20

                return {
                    "status": "PARTIAL",
                    "score": score,
                    "hash": file_hash
                }


            return {
                "status": "INVALID",
                "score": 0,
                "hash": file_hash
            }


        # ====================================================
        # PNG VALIDATION
        # ====================================================

        elif ext == "png":

            png_signature = (
                b"\x89\x50\x4E\x47"
                b"\x0D\x0A\x1A\x0A"
            )


            if (
                data.startswith(png_signature)
                and b"IEND" in data[-100:]
            ):
                return {
                    "status": "VALID",
                    "score": 100,
                    "hash": file_hash
                }


            elif data.startswith(png_signature):

                score = 50 if len(data) > 1024 else 20

                return {
                    "status": "PARTIAL",
                    "score": score,
                    "hash": file_hash
                }


            return {
                "status": "INVALID",
                "score": 0,
                "hash": file_hash
            }


        # ====================================================
        # PDF VALIDATION
        # ====================================================

        elif ext == "pdf":

            if (
                data.startswith(b"%PDF-")
                and b"%%EOF" in data[-1024:]
            ):
                return {
                    "status": "VALID",
                    "score": 100,
                    "hash": file_hash
                }


            elif data.startswith(b"%PDF-"):

                score = 50 if len(data) > 1024 else 20

                return {
                    "status": "PARTIAL",
                    "score": score,
                    "hash": file_hash
                }


            return {
                "status": "INVALID",
                "score": 0,
                "hash": file_hash
            }


        # ====================================================
        # UNKNOWN FILE TYPE
        # ====================================================

        return {
            "status": "UNKNOWN",
            "score": 10,
            "hash": file_hash
        }


    def validate_all(self):

        print(
            f"[*] Starting validation on "
            f"'{self.recovered_dir}' directory..."
        )


        results = []


        if not os.path.exists(self.recovered_dir):
            return results


        for filename in sorted(
            os.listdir(self.recovered_dir)
        ):

            filepath = os.path.join(
                self.recovered_dir,
                filename
            )


            if not os.path.isfile(filepath):
                continue


            result = self.validate_file(
                filepath
            )


            size_mb = (
                os.path.getsize(filepath)
                / (1024 * 1024)
            )


            print(
                f" -> {filename} "
                f"({size_mb:.2f} MB): "
                f"{result['status']} "
                f"(Score: {result['score']})"
            )


            # IMPORTANT:
            # Return the filename together with
            # the validation result so the API
            # can match it with recovered files.

            results.append({
                "filename": filename,
                "status": result["status"],
                "score": result["score"],
                "hash": result["hash"]
            })


        return results


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    validator = FileValidator()

    results = validator.validate_all()

    print("\n[*] Validation Results:")

    for result in results:
        print(result)
