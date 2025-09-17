# Now let's create a requirements.txt file for the modified app
requirements_content = '''Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
'''

with open('requirements.txt', 'w') as f:
    f.write(requirements_content)

print("✓ Created requirements.txt file")

# Let's also create a README with instructions
readme_content = '''# Blood Donation System with CSV Storage

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
'''

with open('README.md', 'w') as f:
    f.write(readme_content)

print("✓ Created README.md file with detailed instructions")

# Create a sample data directory structure script
setup_script = '''import os
import csv

# Create data directory
if not os.path.exists('data'):
    os.makedirs('data')
    print("Created data directory")

# CSV field definitions
CSV_FIELDS = {
    'donors': ['id', 'name', 'email', 'phone', 'age', 'gender', 'city', 'address', 
               'blood_group', 'organs', 'medical_history', 'last_donation', 'available', 'registered_date'],
    'recipients': ['id', 'name', 'email', 'phone', 'age', 'gender', 'city', 'address', 
                   'blood_group', 'organ_needed', 'urgency', 'registered_date'],
    'blood_banks': ['id', 'name', 'city', 'address', 'phone', 'email', 'contact_person'],
    'active_requests': ['id', 'patient_name', 'contact_person', 'phone', 'email', 'city', 
                        'hospital', 'type', 'blood_group', 'organ', 'urgency', 'quantity', 
                        'max_distance', 'additional_info', 'status', 'matched_donor', 'created_date'],
    'notifications': ['id', 'donor_id', 'request_id', 'message', 'distance', 'timestamp', 'status'],
    'accepted_matches': ['id', 'donor_id', 'request_id', 'matched_date', 'status']
}

CSV_FILES = {
    'donors': 'data/donors.csv',
    'recipients': 'data/recipients.csv',
    'blood_banks': 'data/blood_banks.csv',
    'active_requests': 'data/active_requests.csv',
    'notifications': 'data/notifications.csv',
    'accepted_matches': 'data/accepted_matches.csv'
}

# Initialize CSV files with headers
for file_type, filepath in CSV_FILES.items():
    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS[file_type])
            writer.writeheader()
        print(f"Created {filepath} with headers")

print("Setup complete! All CSV files are ready.")
'''

with open('setup_data_files.py', 'w') as f:
    f.write(setup_script)

print("✓ Created setup_data_files.py for initializing CSV files")
print("\nAll files have been created successfully!")