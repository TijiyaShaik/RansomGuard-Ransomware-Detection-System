from flask import Flask, render_template, redirect, url_for, flash
from pathlib import Path

from database import DatabaseManager
from backup import BackupManager

app = Flask(__name__)
app.secret_key = "ransomware_dashboard_secret"

PROTECTED_FOLDER = Path("protected_files").resolve()


@app.route("/")
def dashboard():

    # Count protected files
    total_files = sum(
        1 for file in PROTECTED_FOLDER.rglob("*")
        if file.is_file()
    )

    # Fetch alerts from MySQL
    db = DatabaseManager()
    alerts = db.fetch_alerts()
    db.close()

    total_alerts = len(alerts)

    high_risk = sum(
        1 for alert in alerts
        if alert["risk_level"] in ["HIGH", "CRITICAL"]
    )

    medium_risk = sum(
        1 for alert in alerts
        if alert["risk_level"] == "MEDIUM"
    )

    # Fetch backup information
    backup_manager = BackupManager()
    backups = backup_manager.get_backup_details()

    total_backups = len(backups)

    return render_template(
        "index.html",
        total_files=total_files,
        total_alerts=total_alerts,
        high_risk=high_risk,
        medium_risk=medium_risk,
        alerts=alerts[:10],
        backups=backups,
        total_backups=total_backups
    )


@app.route("/restore/<backup_name>", methods=["POST"])
def restore_file(backup_name):

    # Prevent path traversal
    if Path(backup_name).name != backup_name:
        flash("Invalid backup selection.")
        return redirect(url_for("dashboard"))

    backup_manager = BackupManager()

    backup_path = (
        backup_manager.backup_folder / backup_name
    ).resolve()

    # Find the selected backup's original filename
    details = backup_manager.get_backup_details()

    selected = next(
        (
            item for item in details
            if item["backup_name"] == backup_name
        ),
        None
    )

    if selected is None:
        flash("Backup not found.")
        return redirect(url_for("dashboard"))

    destination = (
        PROTECTED_FOLDER / selected["original_name"]
    ).resolve()

    # Ensure restoration stays inside protected_files
    if not destination.is_relative_to(PROTECTED_FOLDER):
        flash("Invalid restoration destination.")
        return redirect(url_for("dashboard"))

    success = backup_manager.restore_backup(
        backup_path,
        destination
    )

    if success:
        flash(f"{selected['original_name']} restored successfully.", "success")
    else:
        flash("File restoration failed.", "error")

    return redirect(url_for("dashboard"))


if __name__ == "__main__":

    PROTECTED_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    app.run(debug=True)