from prevention import SecurityAlert

alert_system = SecurityAlert()

alert_system.generate_alert(

    filepath="protected_files/sample_10.txt",

    risk_score=65,

    risk_level="HIGH",

    event_type="RAPID_MODIFICATION",

    modified_count=15,

    time_window=5,

    process_name="python.exe",

    process_id=4521

)