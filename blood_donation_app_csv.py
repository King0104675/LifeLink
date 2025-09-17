from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from datetime import datetime, timedelta
import uuid
import random
import csv
import os
import json
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)
app.secret_key = 'blood_organ_donation_secret_2025'

# CSV file paths
CSV_FILES = {
    'donors': 'data/donors.csv',
    'recipients': 'data/recipients.csv',
    'blood_banks': 'data/blood_banks.csv',
    'active_requests': 'data/active_requests.csv',
    'notifications': 'data/notifications.csv',
    'accepted_matches': 'data/accepted_matches.csv'
}

# Create data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

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

def init_csv_files():
    """Initialize CSV files with headers if they don't exist"""
    for file_type, filepath in CSV_FILES.items():
        if not os.path.exists(filepath):
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS[file_type])
                writer.writeheader()

def read_csv_data(file_type):
    """Read data from CSV file and return as dictionary"""
    data = {}
    filepath = CSV_FILES[file_type]
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['id']:  # Skip empty rows
                        # Handle special data types
                        if file_type == 'donors' and 'organs' in row:
                            # Convert organs string back to list
                            if row['organs']:
                                row['organs'] = json.loads(row['organs']) if row['organs'].startswith('[') else row['organs'].split(',')
                            else:
                                row['organs'] = []

                        # Convert boolean fields
                        if 'available' in row:
                            row['available'] = row['available'].lower() == 'true'

                        # Convert numeric fields
                        if 'age' in row and row['age']:
                            row['age'] = int(row['age'])
                        if 'quantity' in row and row['quantity']:
                            row['quantity'] = int(row['quantity'])
                        if 'max_distance' in row and row['max_distance']:
                            row['max_distance'] = int(row['max_distance'])
                        if 'distance' in row and row['distance']:
                            row['distance'] = float(row['distance'])

                        data[row['id']] = row
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    return data

def write_csv_data(file_type, data):
    """Write data dictionary to CSV file"""
    filepath = CSV_FILES[file_type]
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS[file_type])
            writer.writeheader()
            for record in data.values():
                # Handle special data types
                record_copy = record.copy()
                if 'organs' in record_copy and isinstance(record_copy['organs'], list):
                    record_copy['organs'] = json.dumps(record_copy['organs'])

                # Ensure all fields exist
                for field in CSV_FIELDS[file_type]:
                    if field not in record_copy:
                        record_copy[field] = ''

                writer.writerow(record_copy)
    except Exception as e:
        print(f"Error writing {filepath}: {e}")

def add_csv_record(file_type, record):
    """Add a single record to CSV file"""
    filepath = CSV_FILES[file_type]
    try:
        # Handle special data types
        record_copy = record.copy()
        if 'organs' in record_copy and isinstance(record_copy['organs'], list):
            record_copy['organs'] = json.dumps(record_copy['organs'])

        # Ensure all fields exist
        for field in CSV_FIELDS[file_type]:
            if field not in record_copy:
                record_copy[field] = ''

        with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS[file_type])
            writer.writerow(record_copy)
    except Exception as e:
        print(f"Error adding record to {filepath}: {e}")

def read_notifications_for_donor(donor_id):
    """Read notifications for a specific donor from CSV"""
    notifications = []
    filepath = CSV_FILES['notifications']
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['donor_id'] == donor_id:
                        if 'distance' in row and row['distance']:
                            row['distance'] = float(row['distance'])
                        notifications.append(row)
        except Exception as e:
            print(f"Error reading notifications: {e}")
    return notifications

# Initialize CSV files
init_csv_files()

# Blood type compatibility mapping
BLOOD_COMPATIBILITY = {
    'A+': ['A+', 'A-', 'O+', 'O-'],
    'A-': ['A-', 'O-'],
    'B+': ['B+', 'B-', 'O+', 'O-'],
    'B-': ['B-', 'O-'],
    'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
    'AB-': ['A-', 'B-', 'AB-', 'O-'],
    'O+': ['O+', 'O-'],
    'O-': ['O-']
}

# Sample organs list
ORGANS = ['Heart', 'Kidney', 'Liver', 'Lungs', 'Pancreas', 'Cornea', 'Bone Marrow', 'Skin']

# Cities in India for location selection
CITIES = [
    'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad',
    'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur',
    'Indore', 'Thane', 'Bhopal', 'Visakhapatnam', 'Pimpri', 'Patna'
]

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates using Haversine formula"""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def get_city_coordinates(city):
    """Get approximate coordinates for Indian cities"""
    coordinates = {
        'Mumbai': (19.0760, 72.8777),
        'Delhi': (28.7041, 77.1025),
        'Bangalore': (12.9716, 77.5946),
        'Chennai': (13.0827, 80.2707),
        'Kolkata': (22.5726, 88.3639),
        'Hyderabad': (17.3850, 78.4867),
        'Pune': (18.5204, 73.8567),
        'Ahmedabad': (23.0225, 72.5714),
        'Jaipur': (26.9124, 75.7873),
        'Lucknow': (26.8467, 80.9462),
        'Kanpur': (26.4499, 80.3319),
        'Nagpur': (21.1458, 79.0882),
        'Indore': (22.7196, 75.8577),
        'Thane': (19.2183, 72.9781),
        'Bhopal': (23.2599, 77.4126),
        'Visakhapatnam': (17.6868, 83.2185),
        'Pimpri': (18.6298, 73.8131),
        'Patna': (25.5941, 85.1376)
    }
    return coordinates.get(city, (28.7041, 77.1025))  # Default to Delhi

def find_compatible_donors(recipient_request):
    """Find donors compatible with recipient request"""
    donors = read_csv_data('donors')
    compatible_donors = []
    request_type = recipient_request['type']

    for donor_id, donor in donors.items():
        if not donor.get('available', True):
            continue

        # Check if donor can provide what's needed
        if request_type == 'blood' and 'blood_group' in donor:
            # Check blood compatibility
            recipient_blood = recipient_request['blood_group']
            if donor['blood_group'] in BLOOD_COMPATIBILITY.get(recipient_blood, []):
                # Calculate distance
                donor_coords = get_city_coordinates(donor['city'])
                recipient_coords = get_city_coordinates(recipient_request['city'])
                distance = calculate_distance(donor_coords[0], donor_coords[1],
                                           recipient_coords[0], recipient_coords[1])

                if distance <= recipient_request.get('max_distance', 50):  # 50km default
                    compatible_donors.append({
                        'donor_id': donor_id,
                        'donor': donor,
                        'distance': round(distance, 2)
                    })

        elif request_type == 'organ' and 'organs' in donor:
            # Check organ availability
            required_organ = recipient_request['organ']
            donor_organs = donor['organs'] if isinstance(donor['organs'], list) else []
            if required_organ in donor_organs:
                # Calculate distance
                donor_coords = get_city_coordinates(donor['city'])
                recipient_coords = get_city_coordinates(recipient_request['city'])
                distance = calculate_distance(donor_coords[0], donor_coords[1],
                                           recipient_coords[0], recipient_coords[1])

                if distance <= recipient_request.get('max_distance', 100):  # 100km for organs
                    compatible_donors.append({
                        'donor_id': donor_id,
                        'donor': donor,
                        'distance': round(distance, 2)
                    })

    # Sort by distance
    compatible_donors.sort(key=lambda x: x['distance'])
    return compatible_donors

def send_notifications_to_donors(request_id, compatible_donors):
    """Send notifications to compatible donors"""
    active_requests = read_csv_data('active_requests')

    for donor_info in compatible_donors:
        donor_id = donor_info['donor_id']

        notification = {
            'id': str(uuid.uuid4()),
            'donor_id': donor_id,
            'request_id': request_id,
            'message': f"Urgent request for {active_requests[request_id]['type']} donation",
            'distance': donor_info['distance'],
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        }

        add_csv_record('notifications', notification)

# Routes
@app.route('/')
def home():
    donors = read_csv_data('donors')
    active_requests = read_csv_data('active_requests')
    accepted_matches = read_csv_data('accepted_matches')
    blood_banks = read_csv_data('blood_banks')

    stats = {
        'total_donors': len(donors),
        'total_requests': len(active_requests),
        'successful_matches': len(accepted_matches),
        'blood_banks': len(blood_banks)
    }
    return render_template('index.html', stats=stats)

@app.route('/register')
def register():
    return render_template('register.html', cities=CITIES, organs=ORGANS)

@app.route('/submit_donor', methods=['POST'])
def submit_donor():
    donor_data = {
        'id': str(uuid.uuid4()),
        'name': request.form['name'],
        'email': request.form['email'],
        'phone': request.form['phone'],
        'age': int(request.form['age']),
        'gender': request.form['gender'],
        'city': request.form['city'],
        'address': request.form['address'],
        'blood_group': request.form.get('blood_group', ''),
        'organs': request.form.getlist('organs'),
        'medical_history': request.form.get('medical_history', ''),
        'last_donation': request.form.get('last_donation', ''),
        'available': True,
        'registered_date': datetime.now().isoformat()
    }

    add_csv_record('donors', donor_data)
    session['donor_id'] = donor_data['id']
    flash('Registration successful! You are now registered as a donor.', 'success')
    return redirect(url_for('donor_dashboard'))

@app.route('/request')
def request_donation():
    return render_template('request.html', cities=CITIES, organs=ORGANS)

@app.route('/submit_request', methods=['POST'])
def submit_request():
    request_data = {
        'id': str(uuid.uuid4()),
        'patient_name': request.form['patient_name'],
        'contact_person': request.form['contact_person'],
        'phone': request.form['phone'],
        'email': request.form['email'],
        'city': request.form['city'],
        'hospital': request.form['hospital'],
        'type': request.form['type'],
        'urgency': request.form['urgency'],
        'quantity': int(request.form.get('quantity', 1)),
        'max_distance': int(request.form.get('max_distance', 50)),
        'additional_info': request.form.get('additional_info', ''),
        'status': 'active',
        'matched_donor': '',
        'created_date': datetime.now().isoformat(),
        'blood_group': '',
        'organ': ''
    }

    if request_data['type'] == 'blood':
        request_data['blood_group'] = request.form['blood_group']
    else:
        request_data['organ'] = request.form['organ']

    add_csv_record('active_requests', request_data)

    # Find compatible donors and send notifications
    compatible_donors = find_compatible_donors(request_data)
    if compatible_donors:
        send_notifications_to_donors(request_data['id'], compatible_donors)
        flash(f'Request submitted successfully! {len(compatible_donors)} compatible donors have been notified.', 'success')
    else:
        flash('Request submitted, but no compatible donors found nearby. We will continue looking.', 'warning')

    session['request_id'] = request_data['id']
    return redirect(url_for('request_status', request_id=request_data['id']))

@app.route('/donor_dashboard')
def donor_dashboard():
    donor_id = session.get('donor_id')
    if not donor_id:
        return redirect(url_for('register'))

    donors = read_csv_data('donors')
    if donor_id not in donors:
        return redirect(url_for('register'))

    donor = donors[donor_id]
    donor_notifications = read_notifications_for_donor(donor_id)
    active_requests = read_csv_data('active_requests')

    return render_template('donor_dashboard.html', 
                         donor=donor, 
                         notifications=donor_notifications, 
                         active_requests=active_requests)

@app.route('/accept_request', methods=['POST'])
def accept_request():
    donor_id = session.get('donor_id')
    request_id = request.form['request_id']
    notification_id = request.form['notification_id']

    active_requests = read_csv_data('active_requests')

    if donor_id and request_id in active_requests:
        # Update notification status
        notifications = read_csv_data('notifications')
        for notif_id, notification in notifications.items():
            if notification['id'] == notification_id and notification['donor_id'] == donor_id:
                notification['status'] = 'accepted'
                write_csv_data('notifications', notifications)
                break

        # Create match
        match_id = str(uuid.uuid4())
        match_data = {
            'id': match_id,
            'donor_id': donor_id,
            'request_id': request_id,
            'matched_date': datetime.now().isoformat(),
            'status': 'matched'
        }
        add_csv_record('accepted_matches', match_data)

        # Update request status
        active_requests[request_id]['status'] = 'matched'
        active_requests[request_id]['matched_donor'] = donor_id
        write_csv_data('active_requests', active_requests)

        flash('You have successfully accepted the donation request! The recipient has been notified.', 'success')

    return redirect(url_for('donor_dashboard'))

@app.route('/request_status/<request_id>')
def request_status(request_id):
    active_requests = read_csv_data('active_requests')
    if request_id not in active_requests:
        return redirect(url_for('home'))

    request_data = active_requests[request_id]
    matched_donor = None

    if request_data.get('matched_donor'):
        donors = read_csv_data('donors')
        matched_donor = donors.get(request_data['matched_donor'])

    return render_template('request_status.html', request=request_data, matched_donor=matched_donor)

@app.route('/all_requests')
def all_requests():
    active_requests = read_csv_data('active_requests')
    return render_template('all_requests.html', requests=active_requests)

@app.route('/all_donors')
def all_donors():
    donors = read_csv_data('donors')
    return render_template('all_donors.html', donors=donors)

@app.route('/api/stats')
def api_stats():
    donors = read_csv_data('donors')
    active_requests = read_csv_data('active_requests')
    accepted_matches = read_csv_data('accepted_matches')
    blood_banks = read_csv_data('blood_banks')

    active_count = sum(1 for r in active_requests.values() if r.get('status') == 'active')

    return jsonify({
        'donors': len(donors),
        'active_requests': active_count,
        'matches': len(accepted_matches),
        'blood_banks': len(blood_banks)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
