import os
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
