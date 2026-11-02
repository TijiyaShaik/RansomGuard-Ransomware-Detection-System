import json
from pathlib import Path
from datetime import datetime

from database import DatabaseManager


class SecurityAlert:

    def __init__(self):

        self.alert_file = Path("security_alerts.json")
        self.db = DatabaseManager()

    def generate_alert(
        self,
        filepath,
        risk_score,
        risk_level,
        event_type="MODIFIED",
        modified_count=0,
        time_window=10,
        process_name="Unknown",
        process_id=None
    ):

        filepath = str(Path(filepath).resolve())

        filename = Path(filepath).name
        extension = Path(filepath).suffix

        modification_rate = round(
            modified_count / time_window, 2
        ) if time_window else 0

        descriptions = {
            "LOW": "Normal file activity detected.",
            "MEDIUM": "Potentially suspicious file activity detected.",
            "HIGH": "Rapid file modifications detected.",
            "CRITICAL": "Critical ransomware-like activity detected."
        }

        recommendations = {
            "LOW": "Continue monitoring file activity.",
            "MEDIUM": "Review the suspicious file activity.",
            "HIGH": "Investigate the responsible process and protect clean backups.",
            "CRITICAL": "Immediately investigate the activity and isolate the affected environment if necessary."
        }

        alert = {

            "file_name": filename,
            "file_extension": extension,
            "file_path": filepath,
            "event_type": event_type,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "threat_description": descriptions.get(
                risk_level, "Unclassified suspicious activity."
            ),
            "modified_files": modified_count,
            "time_window": time_window,
            "modification_rate": modification_rate,
            "process_name": process_name,
            "process_id": process_id,
            "recommendation": recommendations.get(
                risk_level, "Review the security event."
            ),
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        # Save alert to JSON
        self.save_alert(alert)

        # Save alert to MySQL
        self.db.insert_alert(alert)

        # Display alert
        self.display_alert(alert)

        return alert

    def save_alert(self, alert):

        alerts = []

        if self.alert_file.exists():

            try:
                with open(self.alert_file, "r") as file:
                    alerts = json.load(file)

                if not isinstance(alerts, list):
                    alerts = []

            except (json.JSONDecodeError, OSError):
                alerts = []

        alerts.append(alert)

        with open(self.alert_file, "w") as file:
            json.dump(alerts, file, indent=4)

        print("[SUCCESS] Alert saved to JSON.")

    def display_alert(self, alert):

        print("\n===================================")
        print("         SECURITY ALERT")
        print("===================================")

        print("File Name:", alert["file_name"])
        print("Event Type:", alert["event_type"])
        print("Risk Score:", alert["risk_score"])
        print("Risk Level:", alert["risk_level"])
        print("Process:", alert["process_name"])

        print("Description:", alert["threat_description"])
        print("Recommendation:", alert["recommendation"])

        print("Timestamp:", alert["timestamp"])

        print("===================================\n")