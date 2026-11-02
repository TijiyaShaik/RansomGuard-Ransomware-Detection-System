import time
import threading

from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from detector import RansomwareDetector
from integrity import FileIntegrityMonitor
from backup import BackupManager


PROTECTED_FOLDER = Path("protected_files")


class FileMonitor(FileSystemEventHandler):

    def __init__(self, detector, integrity, backup):

        self.detector = detector
        self.integrity = integrity
        self.backup = backup

        self.pending_backups = set()
        self.backup_timers = {}
        self.backup_tokens = {}

        self.backup_lock = threading.Lock()

        self.check_interval = 1
        self.required_stable_checks = 2

    # Schedule stability checking
    def schedule_backup(self, filepath):

        filepath = Path(filepath).resolve()

        with self.backup_lock:

            old_timer = self.backup_timers.get(filepath)

            if old_timer:
                old_timer.cancel()

            token = object()

            self.backup_tokens[filepath] = token
            self.pending_backups.add(filepath)

            timer = threading.Timer(
                self.check_interval,
                self.check_file_stability,
                args=(filepath, token, None, 0)
            )

            timer.daemon = True

            self.backup_timers[filepath] = timer

            timer.start()

        print(
            "[INFO] Waiting for file content to become stable:",
            filepath.name
        )

    # Check whether file content has stabilized
    def check_file_stability(
        self,
        filepath,
        token,
        previous_signature,
        stable_checks
    ):

        with self.backup_lock:

            if self.backup_tokens.get(filepath) is not token:
                return

        if not filepath.exists() or not filepath.is_file():

            with self.backup_lock:
                self.pending_backups.discard(filepath)
                self.backup_tokens.pop(filepath, None)
                self.backup_timers.pop(filepath, None)

            return

        try:

            stat = filepath.stat()

            # Do not back up an empty file
            if stat.st_size == 0:

                self.schedule_next_check(
                    filepath,
                    token,
                    None,
                    0
                )

                return

            current_signature = (
                stat.st_size,
                stat.st_mtime_ns
            )

            if current_signature == previous_signature:

                stable_checks += 1

            else:

                stable_checks = 0

            if stable_checks >= self.required_stable_checks:

                print(
                    "\n[INFO] File content is stable:",
                    filepath.name
                )

                backup_path = self.backup.create_backup(filepath)

                with self.backup_lock:

                    if self.backup_tokens.get(filepath) is token:

                        self.pending_backups.discard(filepath)
                        self.backup_tokens.pop(filepath, None)
                        self.backup_timers.pop(filepath, None)

                if backup_path:

                    print(
                        "[BACKUP COMPLETED]",
                        backup_path
                    )

                return

            self.schedule_next_check(
                filepath,
                token,
                current_signature,
                stable_checks
            )

        except OSError as error:

            print("[BACKUP CHECK ERROR]", error)

            self.schedule_next_check(
                filepath,
                token,
                previous_signature,
                stable_checks
            )

    # Schedule the next stability check
    def schedule_next_check(
        self,
        filepath,
        token,
        signature,
        stable_checks
    ):

        with self.backup_lock:

            if self.backup_tokens.get(filepath) is not token:
                return

            timer = threading.Timer(
                self.check_interval,
                self.check_file_stability,
                args=(
                    filepath,
                    token,
                    signature,
                    stable_checks
                )
            )

            timer.daemon = True

            self.backup_timers[filepath] = timer

            timer.start()

    # File created
    def on_created(self, event):

        if event.is_directory:
            return

        filepath = Path(event.src_path).resolve()

        print("\n[FILE CREATED]", filepath)

        self.integrity.register_file(str(filepath))

        self.schedule_backup(filepath)

        self.detector.analyze(
            str(filepath),
            "CREATED"
        )

    # File modified
    def on_modified(self, event):

        if event.is_directory:
            return

        filepath = Path(event.src_path).resolve()

        print("\n[FILE MODIFIED]", filepath)

        result = self.integrity.check_integrity(
            str(filepath)
        )

        print("Integrity Status:", result)

        # Continue waiting if the initial backup is pending
        with self.backup_lock:
            backup_pending = filepath in self.pending_backups

        if backup_pending:
            self.schedule_backup(filepath)

        self.detector.analyze(
            str(filepath),
            "MODIFIED"
        )

    # File deleted
    def on_deleted(self, event):

        if event.is_directory:
            return

        filepath = Path(event.src_path).resolve()

        print("\n[FILE DELETED]", filepath)

        with self.backup_lock:

            timer = self.backup_timers.pop(filepath, None)

            if timer:
                timer.cancel()

            self.backup_tokens.pop(filepath, None)
            self.pending_backups.discard(filepath)

        self.integrity.remove_file(str(filepath))

        self.detector.analyze(
            str(filepath),
            "DELETED"
        )

    # File renamed
    def on_moved(self, event):

        if event.is_directory:
            return

        old_path = Path(event.src_path).resolve()
        new_path = Path(event.dest_path).resolve()

        print("\n[FILE RENAMED]")
        print("Old:", old_path)
        print("New:", new_path)

        self.integrity.rename_file(
            str(old_path),
            str(new_path)
        )

        self.detector.analyze(
            str(new_path),
            "RENAMED"
        )


class MonitoringService:

    def __init__(self):

        PROTECTED_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )

        self.detector = RansomwareDetector()

        self.integrity = FileIntegrityMonitor()

        self.backup = BackupManager()

        self.handler = FileMonitor(
            self.detector,
            self.integrity,
            self.backup
        )

        self.observer = Observer()

    def start(self):

        print("\n===================================")
        print(" RANSOMWARE DETECTION SYSTEM")
        print("===================================")

        # Create initial integrity baseline
        self.integrity.create_baseline(
            PROTECTED_FOLDER
        )

        # Back up existing files
        print("\nCreating initial backups...")

        for filepath in PROTECTED_FOLDER.rglob("*"):

            if filepath.is_file():

                self.backup.create_backup(filepath)

        # Start monitoring
        self.observer.schedule(
            self.handler,
            str(PROTECTED_FOLDER),
            recursive=True
        )

        self.observer.start()

        print("\nProtection monitoring started!")

        print(
            "Protected folder:",
            PROTECTED_FOLDER.resolve()
        )

        print("Press CTRL+C to stop.")

        try:

            while True:
                time.sleep(1)

        except KeyboardInterrupt:

            self.stop()

    def stop(self):

        print("\nStopping monitoring...")

        self.observer.stop()
        self.observer.join()

        # Cancel pending timers without backing up incomplete files
        with self.handler.backup_lock:

            for timer in self.handler.backup_timers.values():
                timer.cancel()

            self.handler.backup_timers.clear()
            self.handler.backup_tokens.clear()
            self.handler.pending_backups.clear()

        print("Monitoring stopped successfully.")


if __name__ == "__main__":

    service = MonitoringService()

    service.start()