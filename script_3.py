# Let's also create an example of how the CSV files will look with sample data
import csv
import json
from datetime import datetime
import uuid

# Sample data for demonstration
sample_donors = [
    {
        'id': str(uuid.uuid4()),
        'name': 'John Doe',
        'email': 'john.doe@email.com',
        'phone': '+91-9876543210',
        'age': '28',
        'gender': 'Male',
        'city': 'Mumbai',
        'address': '123 Main Street, Andheri',
        'blood_group': 'O+',
        'organs': json.dumps(['Kidney', 'Cornea']),
        'medical_history': 'No major health issues',
        'last_donation': '2024-06-15',
        'available': 'True',
        'registered_date': datetime.now().isoformat()
    },
    {
        'id': str(uuid.uuid4()),
        'name': 'Priya Sharma',
        'email': 'priya.sharma@email.com',
        'phone': '+91-9876543211',
        'age': '25',
        'gender': 'Female',
        'city': 'Delhi',
        'address': '456 Park Road, Connaught Place',
        'blood_group': 'A+',
        'organs': json.dumps(['Liver']),
        'medical_history': 'Healthy',
        'last_donation': '',
        'available': 'True',
        'registered_date': datetime.now().isoformat()
    }
]

sample_requests = [
    {
        'id': str(uuid.uuid4()),
        'patient_name': 'Raj Patel',
        'contact_person': 'Meera Patel',
        'phone': '+91-9876543212',
        'email': 'meera.patel@email.com',
        'city': 'Mumbai',
        'hospital': 'City Hospital',
        'type': 'blood',
        'blood_group': 'O+',
        'organ': '',
        'urgency': 'High',
        'quantity': '2',
        'max_distance': '25',
        'additional_info': 'Patient needs blood for emergency surgery',
        'status': 'active',
        'matched_donor': '',
        'created_date': datetime.now().isoformat()
    }
]

# Create sample CSV files to show the structure
print("Creating sample CSV files to demonstrate structure:")
print("=" * 50)

# Create donors sample
with open('sample_donors.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'name', 'email', 'phone', 'age', 'gender', 'city', 'address', 
                  'blood_group', 'organs', 'medical_history', 'last_donation', 'available', 'registered_date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for donor in sample_donors:
        writer.writerow(donor)

print("✓ Created sample_donors.csv")

# Create requests sample
with open('sample_requests.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'patient_name', 'contact_person', 'phone', 'email', 'city', 
                  'hospital', 'type', 'blood_group', 'organ', 'urgency', 'quantity', 
                  'max_distance', 'additional_info', 'status', 'matched_donor', 'created_date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for request in sample_requests:
        writer.writerow(request)

print("✓ Created sample_requests.csv")

# Show the contents of sample files
print("\nSample Donors CSV structure:")
print("-" * 30)
with open('sample_donors.csv', 'r') as f:
    content = f.read()
    lines = content.split('\n')[:3]  # Show header + 2 data rows
    for line in lines:
        if line:
            print(line[:100] + "..." if len(line) > 100 else line)

print("\nSample Requests CSV structure:")
print("-" * 30)
with open('sample_requests.csv', 'r') as f:
    content = f.read()
    lines = content.split('\n')[:2]  # Show header + 1 data row
    for line in lines:
        if line:
            print(line[:100] + "..." if len(line) > 100 else line)