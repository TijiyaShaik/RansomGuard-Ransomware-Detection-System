
import time
import psutil

from pathlib import Path
from collections import deque

from prevention import SecurityAlert


class RansomwareDetector:

    def __init__(self):

        self.window = 10
        self.threshold = 10

        self.events = deque()

        self.alerts = []

        # Security alert system
        self.alert_system = SecurityAlert()

        # Alert deduplication
        self.alert_cooldown = 30
        self.last_alerts = {}

        # Suspicious file extensions
        self.suspicious_extensions = {
            ".locked",
            ".encrypted",
            ".crypt"
        }

    # Identify process information
    def get_process_details(self, pid):

        if pid is None:
            return "Unknown", None

        try:

            process = psutil.Process(pid)

            return process.name(), process.pid

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):

            return "Unknown", None

    # Analyze file activities
    def analyze(self, filepath, event_type, process_id=None):

        current_time = time.time()

        filepath = str(Path(filepath).resolve())

        # Store file activity
        self.events.append({
            "time": current_time,
            "file": filepath,
            "event": event_type
        })

        # Remove old events
        while (
            self.events
            and current_time - self.events[0]["time"] > self.window
        ):
            self.events.popleft()

        # Count unique modified files
        recent_modified = {
            event["file"]
            for event in self.events
            if event["event"] == "MODIFIED"
        }

        # Count unique renamed files
        recent_renamed = {
            event["file"]
            for event in self.events
            if event["event"] == "RENAMED"
        }

        # Initialize risk score
        risk_score = 0

        signals = []

        # Rule 1: Rapid file modifications
        if len(recent_modified) >= self.threshold:

            risk_score += 50
            signals.append("RAPID_MODIFICATION")

        # Rule 2: Mass file renaming
        if len(recent_renamed) >= 5:

            risk_score += 30
            signals.append("MASS_RENAMING")

        # Rule 3: Suspicious file extensions
        extension = Path(filepath).suffix.lower()

        if extension in self.suspicious_extensions:

            risk_score += 30
            signals.append("SUSPICIOUS_EXTENSION")

        # Limit risk score
        risk_score = min(risk_score, 100)

        # Threat severity classification
        if risk_score >= 75:

            severity = "CRITICAL"

        elif risk_score >= 50:

            severity = "HIGH"

        elif risk_score >= 30:

            severity = "MEDIUM"

        else:

            severity = "LOW"

        # Display security analysis
        print("\n========== SECURITY ANALYSIS ==========")

        print("File:", filepath)

        print("Event:", event_type)

        print("Modified Files:", len(recent_modified))

        print("Renamed Files:", len(recent_renamed))

        print("Risk Score:", risk_score)

        print("Threat Severity:", severity)

        # Process identification
        process_name, detected_pid = self.get_process_details(
            process_id
        )

        # Generate security alert
        if severity != "LOW":

            fingerprint = tuple(sorted(signals))

            previous_alert = self.last_alerts.get(fingerprint)

            should_alert = (
                previous_alert is None
                or current_time - previous_alert >= self.alert_cooldown
            )

            if should_alert:

                alert = self.alert_system.generate_alert(

                    filepath=filepath,

                    risk_score=risk_score,

                    risk_level=severity,

                    event_type=event_type,

                    modified_count=len(recent_modified),

                    time_window=self.window,

                    process_name=process_name,

                    process_id=detected_pid
                )

                self.alerts.append(alert)

                self.last_alerts[fingerprint] = current_time

                print("\n[SECURITY ALERT GENERATED]")

            else:

                print("\n[INFO] Duplicate alert suppressed.")

        return severity

