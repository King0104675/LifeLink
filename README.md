# Blood Donation System with CSV Storage

## Overview
This is a Flask-based blood and organ donation management system that stores data in CSV files instead of a database.

## Features
- Donor registration and management
- Blood/organ request system
- Compatible donor matching based on location and blood type
- Notification system for donors
- Request tracking and status updates
- Dashboard for donors to view and respond to requests

## File Structure
```
project/
├── blood_donation_app_csv.py    # Main Flask application
├── requirements.txt             # Python dependencies
├── data/                       # CSV data storage directory
│   ├── donors.csv              # Donor information
│   ├── active_requests.csv     # Blood/organ requests
│   ├── notifications.csv       # Donor notifications
│   ├── accepted_matches.csv    # Successful matches
│   ├── recipients.csv          # Recipient information
│   └── blood_banks.csv         # Blood bank information
└── templates/                  # HTML templates
    ├── base.html
    ├── index.html
    ├── register.html
    ├── request.html
    ├── donor_dashboard.html
    ├── request_status.html
    ├── all_requests.html
    └── all_donors.html
```

## Installation & Setup
1. Install Python 3.7 or higher
2. Install dependencies: `pip install -r requirements.txt`
3. Ensure all HTML template files are in the `templates/` directory
4. Run the application: `python blood_donation_app_csv.py`
5. Open your browser and navigate to `http://localhost:5000`

## Data Storage
- All data is stored in CSV files in the `data/` directory
- Files are automatically created with proper headers when the app starts
- Data persists between application restarts
- CSV files can be opened and edited in Excel or other spreadsheet programs

## Key Changes from Original
- Replaced in-memory dictionaries with CSV file storage
- Added robust CSV read/write functions
- Proper handling of data types (lists, booleans, numbers)
- Error handling for file operations
- Maintained all original functionality

## Usage
1. **Register as Donor**: Fill out the registration form with your details
2. **Submit Request**: Create a blood/organ request with specific requirements
3. **View Notifications**: Donors can see matching requests in their dashboard
4. **Accept Requests**: Donors can accept compatible donation requests
5. **Track Status**: Request creators can track the status of their requests

## Data Fields

### Donors CSV
- id, name, email, phone, age, gender, city, address
- blood_group, organs (JSON array), medical_history, last_donation
- available (boolean), registered_date

### Active Requests CSV
- id, patient_name, contact_person, phone, email, city, hospital
- type, blood_group, organ, urgency, quantity, max_distance
- additional_info, status, matched_donor, created_date

### Notifications CSV
- id, donor_id, request_id, message, distance, timestamp, status

### Accepted Matches CSV
- id, donor_id, request_id, matched_date, status
