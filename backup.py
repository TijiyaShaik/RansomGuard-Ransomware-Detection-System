import hashlib
import shutil
import re

from pathlib import Path
from datetime import datetime


class BackupManager:

    def __init__(self):

        self.backup_folder = Path("backups/versions")

        self.backup_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    # Calculate SHA-256 hash
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

    # Create backup
    def create_backup(self, filepath):

        source = Path(filepath)

        if not source.is_file():
            print("File does not exist!")
            return None

        original_hash = self.calculate_hash(source)

        if original_hash is None:
            return None

        # Check whether an identical backup already exists
        existing_backups = self.list_backups(source.name)

        for existing_backup in existing_backups:

            existing_hash = self.calculate_hash(existing_backup)

            if existing_hash == original_hash:

                print("\n[INFO] Identical backup already exists.")
                print("Existing Backup:", existing_backup)

                return existing_backup

        # Create a new backup if content has changed
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        backup_name = (
            source.stem + "_" + timestamp + source.suffix
        )

        backup_path = self.backup_folder / backup_name

        shutil.copy2(source, backup_path)

        backup_hash = self.calculate_hash(backup_path)

        if original_hash == backup_hash:

            print("\n[BACKUP SUCCESSFUL]")
            print("Backup File:", backup_path)

            return backup_path

        backup_path.unlink(missing_ok=True)

        print("Backup verification failed!")

        return None

    # List backups for a particular file
    def list_backups(self, filename):

        backups = list(
            self.backup_folder.glob(
                f"{Path(filename).stem}_*{Path(filename).suffix}"
            )
        )

        backups.sort(
            key=lambda item: item.stat().st_mtime,
            reverse=True
        )

        return backups

    # List all backups
    def list_all_backups(self):

        backups = [
            file for file in self.backup_folder.iterdir()
            if file.is_file()
        ]

        backups.sort(
            key=lambda item: item.stat().st_mtime,
            reverse=True
        )

        return backups

    # Get backup information
    def get_backup_details(self):

        backup_details = []

        for backup in self.list_all_backups():

            backup_hash = self.calculate_hash(backup)

            # Extract original filename
            match = re.match(
                r"^(.+)_\d{8}_\d{6}_\d{6}(\..+)?$",
                backup.name
            )

            original_name = (
                match.group(1) + (match.group(2) or "")
                if match else backup.name
            )

            backup_details.append({

                "backup_name": backup.name,
                "original_name": original_name,
                "backup_path": str(backup),
                "backup_date": datetime.strptime(
    re.search(
        r"_(\d{8}_\d{6}_\d{6})(?=\.)",
        backup.name
    ).group(1),
    "%Y%m%d_%H%M%S_%f"
).strftime("%Y-%m-%d %H:%M:%S"),
                "size": round(backup.stat().st_size / 1024, 2),
                "status": (
                    "Available" if backup_hash is not None
                    else "Unreadable"
                )

            })

        return backup_details

    # Restore backup
    def restore_backup(self, backup_path, destination):

        backup_path = Path(backup_path).resolve()
        destination = Path(destination).resolve()

        # Ensure the selected backup belongs to backup folder
        try:
            backup_path.relative_to(self.backup_folder.resolve())
        except ValueError:
            print("Invalid backup location!")
            return False

        if not backup_path.is_file():

            print("Backup file not found!")
            return False

        backup_hash = self.calculate_hash(backup_path)

        if backup_hash is None:
            return False

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(
            backup_path,
            destination
        )

        restored_hash = self.calculate_hash(destination)

        if restored_hash == backup_hash:

            print("\n[FILE RESTORED SUCCESSFULLY]")
            print("Restored File:", destination)

            return True

        print("Restoration verification failed!")

        return False