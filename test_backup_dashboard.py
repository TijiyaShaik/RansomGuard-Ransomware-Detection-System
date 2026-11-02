from backup import BackupManager

backup = BackupManager()

print("\n========== BACKUP DASHBOARD TEST ==========")

details = backup.get_backup_details()

print("Total Backups:", len(details))

for item in details:

    print("\nBackup Name:", item["backup_name"])
    print("Original File:", item["original_name"])
    print("Backup Date:", item["backup_date"])
    print("Size:", item["size"], "KB")
    print("Status:", item["status"])

print("\nBackup dashboard test completed.")