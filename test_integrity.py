# from integrity import FileIntegrityMonitor

# monitor = FileIntegrityMonitor()

# folder = "protected_files"

# # Step 1: Create baseline
# monitor.create_baseline(folder)

# # Step 2: Select a file
# filepath = "protected_files/sample.txt"

# # Step 3: Check integrity
# result = monitor.check_integrity(filepath)

# print("Integrity Status:", result)

from integrity import FileIntegrityMonitor

monitor = FileIntegrityMonitor()

folder = "protected_files"
filepath = "protected_files/sample.txt"

# Establish original hash
monitor.create_baseline(folder)

# Modify the file
with open(filepath, "w") as file:
    file.write("Hello Cybersecurity students")

# Check integrity
result = monitor.check_integrity(filepath)

print("Integrity Status:", result)