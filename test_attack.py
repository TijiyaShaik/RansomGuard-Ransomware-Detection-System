from pathlib import Path
import time

folder = Path("protected_files")

print("Starting harmless ransomware behavior simulation...")

for i in range(15):
    file_path = folder / f"attack_test_{i}.txt"

    file_path.write_text(
        f"Initial content for file {i}",
        encoding="utf-8"
    )

print("Test files created.")

time.sleep(2)

for i in range(15):
    file_path = folder / f"attack_test_{i}.txt"

    file_path.write_text(
        f"Modified content for file {i}",
        encoding="utf-8"
    )

print("15 files modified successfully.")
print("Simulation completed.")