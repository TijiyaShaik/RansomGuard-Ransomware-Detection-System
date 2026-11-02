import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseManager:

    def __init__(self):
        self.connection = None

    def connect(self):

        try:
            if self.connection and self.connection.is_connected():
                return True

            self.connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

            print("[SUCCESS] Connected to MySQL database.")
            return True

        except Error as e:
            print("[DATABASE ERROR]", e)
            self.connection = None
            return False

    def insert_alert(self, alert):

        try:
            if not self.connect():
                return False

            query = """
                INSERT INTO security_alerts (
                    filename,
                    file_path,
                    event_type,
                    risk_score,
                    risk_level,
                    threat_description,
                    modified_files,
                    time_window,
                    modification_rate,
                    process_name,
                    process_id,
                    recommendation,
                    timestamp
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                alert.get("file_name", alert.get("filename")),
                alert.get("file_path", alert.get("filepath")),
                alert.get("event_type"),
                alert.get("risk_score"),
                alert.get("risk_level"),
                alert.get("threat_description"),
                alert.get("modified_files", alert.get("modified_count", 0)),
                alert.get("time_window", 10),
                alert.get("modification_rate", 0.0),
                alert.get("process_name", "Unknown"),
                alert.get("process_id"),
                alert.get("recommendation"),
                alert.get("timestamp")
            )

            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()

            cursor.close()

            print("[SUCCESS] Security alert saved to MySQL.")
            return True

        except Error as e:
            print("[DATABASE ERROR]", e)
            return False

    def fetch_alerts(self):

        try:
            if not self.connect():
                return []

            cursor = self.connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT *
                FROM security_alerts
                ORDER BY timestamp DESC
            """)

            alerts = cursor.fetchall()
            cursor.close()

            return alerts

        except Error as e:
            print("[DATABASE ERROR]", e)
            return []

    def close(self):

        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None
            print("[INFO] MySQL connection closed.")


if __name__ == "__main__":

    db = DatabaseManager()

    if db.connect():
        print("Database connection test successful.")

    db.close()