from detector import RansomwareDetector

detector = RansomwareDetector()

filepath = "protected_files/sample.locked"

result = detector.analyze(filepath, "MODIFIED")

print("\nFinal Classification:", result)