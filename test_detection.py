
from detector import RansomwareDetector

from pathlib import Path
import os
import time

detector = RansomwareDetector()

folder = Path("protected_files")

folder.mkdir(exist_ok=True)

print("Starting ransomware detection test...")

# Simulate rapid modifications
for i in range(15):

    filepath = folder / f"sample_{i}.txt"

    filepath.write_text("Harmless test content")

    detector.analyze(
        filepath,
        "MODIFIED",
        process_id=os.getpid()
    )

    time.sleep(0.2)

print("\nDetection test completed.")

