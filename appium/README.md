# ZyntraPass – Appium Mobile Test Suite

End-to-end mobile automation test suite for the **ZyntraPass** Android application using **Appium**.
All test cases, scripts, reports, and configurations are contained exclusively within this folder.

---

## 📁 Folder Structure

```
appium/
├── README.md
├── requirements.txt
├── appium.config.json
├── conftest.py
├── generate_report.py         ← generates appium_test_report.xlsx
├── reports/
│   └── appium_test_report.xlsx
└── tests/
    ├── test_login.py
    ├── test_role_selection.py
    ├── test_organizer.py
    ├── test_create_event.py
    ├── test_live_attendance.py
    ├── test_participants.py
    ├── test_certificates.py
    ├── test_volunteers.py
    ├── test_attendee.py
    ├── test_settings.py
    └── test_navigation.py
```

---

## ⚙️ Prerequisites

| Tool | Version |
|------|---------|
| Python | ≥ 3.9 |
| Appium Server | ≥ 2.x |
| Appium UIAutomator2 Driver | latest |
| Android SDK / ADB | API 24+ |
| Android Emulator / Real Device | connected |

---

## 🚀 Setup

```bash
# 1. Install Appium server globally
npm install -g appium
appium driver install uiautomator2

# 2. Install Python dependencies
pip install -r appium/requirements.txt

# 3. Set environment variables
export APP_PATH=/path/to/ZyntraPass.apk
export APPIUM_HOST=127.0.0.1
export APPIUM_PORT=4723

# 4. Start Appium server
appium

# 5. Run all tests
cd appium
pytest tests/ -v --html=reports/appium_test_report.html

# 6. Generate Excel report
python generate_report.py
```

---

## 🧪 Test Modules

| Module | File | Test Cases |
|--------|------|------------|
| Login | test_login.py | TC001–TC020 |
| Role Selection | test_role_selection.py | TC021–TC030 |
| Organizer | test_organizer.py | TC031–TC075 |
| Create Event | test_create_event.py | TC076–TC105 |
| Live Attendance | test_live_attendance.py | TC106–TC130 |
| Participants | test_participants.py | TC131–TC160 |
| Certificates | test_certificates.py | TC161–TC185 |
| Volunteers | test_volunteers.py | TC186–TC225 |
| Attendee | test_attendee.py | TC226–TC320 |
| Settings | test_settings.py | TC321–TC360 |
| Navigation | test_navigation.py | TC361–TC410 |

**Total: 410 unique test cases**

---

## 📊 Report

Run `python generate_report.py` to produce `reports/appium_test_report.xlsx`  
The report includes: Test ID, Module, Screen, Test Name, Steps, Expected Result, Status, Priority.

---

## 🔄 CI/CD

Tests are automated via GitHub Actions — see `.github/workflows/appium_tests.yml`.
