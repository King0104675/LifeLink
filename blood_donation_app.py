
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from datetime import datetime, timedelta
import uuid
import random
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)
app.secret_key = 'blood_organ_donation_secret_2025'

# Temporary data storage (in-memory)
donors = {}
recipients = {}
blood_banks = {}
active_requests = {}
notifications = {}
accepted_matches = {}

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
            if required_organ in donor['organs']:
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
    for donor_info in compatible_donors:
        donor_id = donor_info['donor_id']
        if donor_id not in notifications:
            notifications[donor_id] = []

        notification = {
            'id': str(uuid.uuid4()),
            'request_id': request_id,
            'message': f"Urgent request for {active_requests[request_id]['type']} donation",
            'distance': donor_info['distance'],
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        }
        notifications[donor_id].append(notification)

# Routes
@app.route('/')
def home():
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
        'blood_group': request.form.get('blood_group'),
        'organs': request.form.getlist('organs'),
        'medical_history': request.form.get('medical_history', ''),
        'last_donation': request.form.get('last_donation'),
        'available': True,
        'registered_date': datetime.now().isoformat()
    }

    donors[donor_data['id']] = donor_data
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
        'quantity': request.form.get('quantity', 1),
        'max_distance': int(request.form.get('max_distance', 50)),
        'additional_info': request.form.get('additional_info', ''),
        'status': 'active',
        'created_date': datetime.now().isoformat()
    }

    if request_data['type'] == 'blood':
        request_data['blood_group'] = request.form['blood_group']
    else:
        request_data['organ'] = request.form['organ']

    active_requests[request_data['id']] = request_data

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
    if not donor_id or donor_id not in donors:
        return redirect(url_for('register'))

    donor = donors[donor_id]
    donor_notifications = notifications.get(donor_id, [])

    return render_template('donor_dashboard.html', donor=donor, notifications=donor_notifications, active_requests=active_requests)

@app.route('/accept_request', methods=['POST'])
def accept_request():
    donor_id = session.get('donor_id')
    request_id = request.form['request_id']
    notification_id = request.form['notification_id']

    if donor_id and request_id in active_requests:
        # Mark notification as accepted
        for notification in notifications.get(donor_id, []):
            if notification['id'] == notification_id:
                notification['status'] = 'accepted'
                break

        # Create match
        match_id = str(uuid.uuid4())
        accepted_matches[match_id] = {
            'donor_id': donor_id,
            'request_id': request_id,
            'matched_date': datetime.now().isoformat(),
            'status': 'matched'
        }

        # Update request status
        active_requests[request_id]['status'] = 'matched'
        active_requests[request_id]['matched_donor'] = donor_id

        flash('You have successfully accepted the donation request! The recipient has been notified.', 'success')

    return redirect(url_for('donor_dashboard'))

@app.route('/request_status/<request_id>')
def request_status(request_id):
    if request_id not in active_requests:
        return redirect(url_for('home'))

    request_data = active_requests[request_id]
    matched_donor = None

    if request_data.get('matched_donor'):
        matched_donor = donors.get(request_data['matched_donor'])

    return render_template('request_status.html', request=request_data, matched_donor=matched_donor)

@app.route('/all_requests')
def all_requests():
    return render_template('all_requests.html', requests=active_requests)

@app.route('/all_donors')
def all_donors():
    return render_template('all_donors.html', donors=donors)

@app.route('/api/stats')
def api_stats():
    return jsonify({
        'donors': len(donors),
        'active_requests': len([r for r in active_requests.values() if r['status'] == 'active']),
        'matches': len(accepted_matches),
        'blood_banks': len(blood_banks)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
