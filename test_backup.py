
from pathlib import Path

from backup import BackupManager


# Initialize backup manager
manager = BackupManager()

folder = Path("protected_files")

folder.mkdir(exist_ok=True)

filepath = folder / "important.txt"

# Create original file
filepath.write_text(
    "This is my original important file."
)

print("\nOriginal content:")

print(filepath.read_text())


# Step 1: Create backup
print("\nCreating backup...")

backup_path = manager.create_backup(filepath)


if backup_path:

    # Step 2: Modify original file
    print("\nModifying original file...")

    filepath.write_text(
        "This content has been modified."
    )

    print("Modified content:")

    print(filepath.read_text())


    # Step 3: Display available backups
    print("\nAvailable backups:")

    backups = manager.list_backups("important.txt")

    for backup in backups:

        print(backup)


    # Step 4: Restore original file
    print("\nRestoring original file...")

    manager.restore_backup(
        backup_path,
        filepath
    )


    # Step 5: Verify restored content
    print("\nFinal restored content:")

    print(filepath.read_text())

