# Attendance Manager

## Overview

Attendance Manager is a desktop application designed to manage attendance records for schools, organizations, or businesses. It provides secure authentication, attendance tracking, personnel management, reporting, and system administration through a modern, organized interface.

---

# Application Structure

```
Attendance Manager
│
├── Login
│
├── Setup Wizard (First Launch Only)
│   ├── Organization Information
│   ├── Administrator Account
│   ├── Attendance Method
│   ├── Database Configuration
│   └── Finish
│
└── Main Application
    ├── Dashboard
    ├── Attendance
    ├── People
    ├── Logs
    ├── Profile
    ├── Settings
    └── Logout
```

---

# Pages

## Login

### Purpose

Authenticate users before granting access to the application.

### Responsibilities

* Username or Email
* Password
* Remember Me
* Forgot Password (Optional)
* Login Authentication
* Display Login Errors

### Notes

* Users cannot access any application features without successful authentication.
* This page should only handle authentication.

---

## Setup Wizard

### Purpose

Configure the application during the first launch.

### Administrator Account Setup

* Administrator Username
* Password
* Email Address

### Notes

The Setup Wizard should only appear during the first launch or after a factory reset.

---

## Dashboard

### Purpose

Provide a quick overview of the entire system.

### Typical Information

* Present Today
* Absent Today
* Late Today
* Recent Check-ins
* Recent Check-outs
* System Notifications

### Quick Actions

* Start Attendance
* Add Person
* Generate Report
* Open Attendance Records

### Notes

The dashboard is intended to summarize information rather than modify records.

---

## Attendance

### Purpose

Record and manage daily attendance.

### Features

* Check In
* Check Out
* QR Code Scanning
* Manual Attendance
* Attendance Search
* Attendance History
* Edit Records (Administrator)
* Delete Incorrect Records (Administrator)
* Add classes/subjects per course or section

---

## Students

### Purpose

Manage everyone who can use the attendance system.

Examples include:

* Students

### Features

* Add Person
* Edit Information
* Delete Person
* Upload Photo (Optional)
* Assign QR Code
* Import CSV
* Export CSV

Typical information stored:

* Full Name
* Course
* Section
* Contact Information
* QR Identifier
* Status

---

## Logs

### Purpose

Generate historical attendance Logs.

### Available Logs

* Daily
* Weekly
* Monthly
* Custom Date Range

### Export Formats

* PDF
* Excel
* CSV

---

## Profile

### Purpose

Manage the currently logged-in user's account and users.

### Features

* Profile Picture (Optional)
* Name
* Username
* Email
* Change Password
* Add User
* Link Google Account (OAuth)

---

## Settings

### Purpose

Configure system-wide application behavior.

### General

* Theme
* Time Format

### Attendance

* Grace Period
* Working Hours
* Overtime Rules

### Database

* Backup
* Restore

### About

* Application Version
* License
* Developer Information

---

# Sidebar Navigation

```
Attendance Manager

🏠 Dashboard
📋 Attendance
👥 Students
📊 Logs
👤 Profile
🛠 Settings
🚪 Logout
```

---