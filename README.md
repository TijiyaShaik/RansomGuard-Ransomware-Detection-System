# 🛡️ RansomGuard – Ransomware Detection and Prevention System

A Python-based cybersecurity project that detects suspicious file activities associated with potential ransomware attacks through real-time monitoring, behavioral analysis, and file integrity verification. It also provides backup management and file recovery through an interactive Flask dashboard.

---

## 📌 Project Overview

RansomGuard is designed to identify potential ransomware behavior by continuously monitoring files and analyzing suspicious activities such as rapid file modifications, mass renaming, and suspicious file extensions.

The system uses behavioral detection techniques and SHA-256 hashing to monitor file integrity, assign risk scores, and generate security alerts. It also maintains versioned backups to support file recovery.

A Flask-based dashboard provides a centralized interface to monitor file activities, review security alerts, manage backups, and restore files.

---

## ✨ Key Features

* **Real-Time File Monitoring:** Monitors file creation, modification, deletion, and renaming activities using Watchdog.
* **Behavioral Threat Detection:** Identifies suspicious patterns through rapid file modifications, mass renaming, and suspicious extensions.
* **Risk Assessment:** Assigns risk scores and classifies detected activities into LOW, MEDIUM, HIGH, and CRITICAL severity levels.
* **File Integrity Monitoring:** Uses SHA-256 hashing to identify unauthorized or unexpected file changes.
* **Security Alert Management:** Generates alerts containing file information, event details, risk scores, and recommendations.
* **Database Integration:** Stores security alerts in a MySQL database.
* **Automated Backup Management:** Creates versioned backups and verifies backup integrity.
* **File Recovery:** Supports restoration of previous file versions with SHA-256 verification.
* **Interactive Dashboard:** Provides a Flask-based interface for monitoring alerts, viewing backups, and managing recovery.

---

## 🛠️ Technologies Used

| Category                | Technologies |
| ----------------------- | ------------ |
| Programming Language    | Python       |
| Backend Framework       | Flask        |
| Database                | MySQL        |
| File Monitoring         | Watchdog     |
| Process Monitoring      | Psutil       |
| File Integrity          | SHA-256      |
| Frontend                | HTML, CSS    |
| Development Environment | VS Code      |
| Version Control         | Git, GitHub  |

---

## 📂 Project Structure

```text
RansomGuard-Ransomware-Detection-System/
│
├── app.py
├── monitor.py
├── detector.py
├── integrity.py
├── backup.py
├── database.py
├── prevention.py
├── containment.py
├── process_monitor.py
│
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── screenshots/
│   ├── dashboard.png
│   ├── security_alerts.png
│   ├── backup_management.png
│   ├── file_recovery_check.png
│   └── file_recovery_success.png
│
├── protected_files/
│
├── backups/
│   └── versions/
│
└── venv/
```

---

## 📸 Project Screenshots

### 1. RansomGuard Dashboard

Displays an overview of protected files, security alerts, risk levels, and available backups.

<img width="1920" height="1020" alt="dashboard png" src="https://github.com/user-attachments/assets/1aea6061-bc14-40b2-9e8c-17367e28f459" />


### 2. Security Alerts

Displays detected suspicious file activities, associated risk scores, severity levels, and alert information.

<img width="1920" height="1020" alt="security_alerts png" src="https://github.com/user-attachments/assets/2df79eff-233a-42af-b5c4-cd3954a5f566" />


### 3. Backup Management

Displays available backup versions, original filenames, backup timestamps, file sizes, and recovery options.

<img width="1920" height="1020" alt="backup_management png" src="https://github.com/user-attachments/assets/0e6af732-5a51-4c20-b70e-fd034766852a" />


### 4. File Recovery – Integrity Verification

Demonstrates the file recovery verification process using SHA-256 hashing to check file integrity.

<img width="1920" height="1020" alt="file_recovery_check png" src="https://github.com/user-attachments/assets/1ac1f1d9-e33b-4325-8cef-9aeb9e7c07d6" />


### 5. File Recovery – Successful Restoration

Shows the successful restoration of a previous file version through the recovery functionality.

<img width="1920" height="1020" alt="file_recovery_success png" src="https://github.com/user-attachments/assets/601c085a-6ea8-41b8-b426-d78b6d722fa2" />


---

## ⚙️ Installation and Setup

### Prerequisites

* Python 3.10 or above
* MySQL Server
* MySQL Workbench (optional)
* Visual Studio Code
* Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/RansomGuard-Ransomware-Detection-System.git
```

Navigate into the project directory:

```bash
cd RansomGuard-Ransomware-Detection-System
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure MySQL Database

1. Start your MySQL server.
2. Open MySQL Workbench.
3. Create a database named:

```sql
CREATE DATABASE ransomware_db;
```

4. Configure your database credentials in a `.env` file in the project root.

Example:

```env
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=ransomware_db
```

Replace the placeholder with your MySQL password.

**Note:** The `.env` file is excluded from version control. Never upload database credentials to GitHub.

5. Ensure the `security_alerts` table is created with the columns required by the application.

---

## ▶️ Running the Application

The application requires two separate terminal sessions.

### Terminal 1: Start File Monitoring

Activate the virtual environment and run:

```bash
python monitor.py
```

This starts monitoring activities in the protected files directory.

### Terminal 2: Start Flask Dashboard

Open another terminal, activate the virtual environment, and run:

```bash
python app.py
```

Open your browser and navigate to:

```text
http://127.0.0.1:5000/
```

The RansomGuard dashboard will be displayed.

---

## 🔍 Detection Methodology

RansomGuard uses rule-based behavioral analysis to identify suspicious file activities.

| Suspicious Activity      | Detection Approach                                                |
| ------------------------ | ----------------------------------------------------------------- |
| Rapid File Modifications | Tracks multiple unique file modifications within a time window.   |
| Mass File Renaming       | Identifies repeated file renaming activities.                     |
| Suspicious Extensions    | Detects extensions such as `.locked`, `.encrypted`, and `.crypt`. |
| File Integrity Changes   | Compares SHA-256 hashes to identify file modifications.           |

The detection engine calculates a risk score based on observed activity and classifies alerts into four severity levels:

| Risk Score | Severity |
| ---------- | -------- |
| 0–29       | LOW      |
| 30–49      | MEDIUM   |
| 50–74      | HIGH     |
| 75–100     | CRITICAL |

---

## 🔐 Backup and Recovery Mechanism

The backup and recovery module supports file restoration through the following process:

1. Creates backups of monitored files.
2. Maintains different backup versions when file content changes.
3. Calculates SHA-256 hashes for integrity verification.
4. Allows users to select a previous backup version.
5. Restores the selected version to the protected files directory.
6. Verifies the restored file using SHA-256 hash comparison.

---

## ⚠️ Project Limitations

* This project is an academic prototype based on rule-based behavioral detection.
* Detection depends on configured thresholds and monitored file activities.
* Process attribution may be unavailable for certain file events.
* File restoration is performed through the dashboard and requires user action.
* It does not provide guaranteed ransomware prevention or replace professional endpoint detection and response solutions.

---

## 🚀 Future Enhancements

* Machine learning-based ransomware behavior classification.
* Advanced process attribution and suspicious process monitoring.
* Real-time notification and alert integration.
* Improved threat scoring using additional behavioral indicators.
* Enhanced backup automation and recovery management.

---

## 👩‍💻 Author

**YOUR NAME**

B.Tech – Artificial Intelligence and Data Science

---

## 📄 Disclaimer

This project is developed for academic and educational purposes. Testing is performed using harmless file activity simulations and does not require executing actual ransomware.
