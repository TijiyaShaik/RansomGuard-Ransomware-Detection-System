import hashlib
from pathlib import Path


class FileIntegrityMonitor:

    def __init__(self):
        self.file_hashes = {}

    # Calculate SHA-256
    def calculate_hash(self, filepath):

        sha256 = hashlib.sha256()

        try:
            with open(filepath, "rb") as file:

                for chunk in iter(
                    lambda: file.read(4096), b""
                ):
                    sha256.update(chunk)

            return sha256.hexdigest()

        except OSError:
            return None

    # Create initial baseline
    def create_baseline(self, folder):

        count = 0

        for filepath in Path(folder).rglob("*"):

            if filepath.is_file():

                self.register_file(filepath)
                count += 1

        print("Integrity baseline created.")
        print("Files monitored:", count)

    # Register a new file
    def register_file(self, filepath):

        filepath = str(Path(filepath).resolve())

        file_hash = self.calculate_hash(filepath)

        if file_hash:
            self.file_hashes[filepath] = file_hash

    # Check file integrity
    def check_integrity(self, filepath):

        filepath = str(Path(filepath).resolve())

        current_hash = self.calculate_hash(filepath)

        if current_hash is None:
            return "UNAVAILABLE"

        original_hash = self.file_hashes.get(filepath)

        if original_hash is None:

            self.file_hashes[filepath] = current_hash

            return "NEW FILE"

        if original_hash != current_hash:

            print("\n[WARNING] FILE MODIFIED!")
            print("File:", filepath)

            # Update baseline
            self.file_hashes[filepath] = current_hash

            return "MODIFIED"

        return "UNCHANGED"

    # Remove deleted files
    def remove_file(self, filepath):

        filepath = str(Path(filepath).resolve())

        self.file_hashes.pop(filepath, None)

    # Update baseline after rename
    def rename_file(self, old_path, new_path):

        old_path = str(Path(old_path).resolve())
        new_path = str(Path(new_path).resolve())

        old_hash = self.file_hashes.pop(old_path, None)

        if old_hash:
            self.file_hashes[new_path] = old_hash