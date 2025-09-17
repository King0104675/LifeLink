
# Sample Data Generator for LifeLink Blood/Organ Donation System
# Run this after starting the main application to populate with demo data

import random
from datetime import datetime, timedelta
import uuid

# Sample data for demonstration
SAMPLE_DONOR_NAMES = [
    "Dr. Arjun Sharma", "Priya Patel", "Rajesh Kumar", "Sneha Gupta", "Amit Singh",
    "Kavya Reddy", "Rohit Verma", "Anita Joshi", "Vikram Malhotra", "Deepika Nair",
    "Sanjay Yadav", "Meera Shah", "Akash Agarwal", "Pooja Mishra", "Ravi Tiwari",
    "Sunita Rao", "Manish Kapoor", "Asha Bhatt", "Kiran Kumar", "Neha Bansal"
]

SAMPLE_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", 
    "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Kanpur", "Nagpur"
]

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

ORGANS = ["Heart", "Kidney", "Liver", "Lungs", "Pancreas", "Cornea", "Bone Marrow", "Skin"]

HOSPITALS = [
    "Apollo Hospital", "Fortis Healthcare", "Max Hospital", "AIIMS", 
    "Manipal Hospital", "Columbia Asia", "Narayana Health", "Medanta",
    "Kokilaben Hospital", "Ruby Hall Clinic", "Global Hospital", "Care Hospital"
]

def generate_sample_donors(num_donors=50):
    """Generate sample donor data"""
    sample_donors = {}

    for i in range(num_donors):
        donor_id = str(uuid.uuid4())

        # Random donor data
        name = random.choice(SAMPLE_DONOR_NAMES)
        city = random.choice(SAMPLE_CITIES)
        blood_group = random.choice(BLOOD_GROUPS)
        age = random.randint(18, 60)
        gender = random.choice(["male", "female"])

        # Random organs (0-4 organs per donor)
        num_organs = random.randint(0, 4)
        organs = random.sample(ORGANS, num_organs)

        # Generate email and phone
        email = f"{name.lower().replace(' ', '').replace('.', '')}{random.randint(10, 99)}@email.com"
        phone = f"+91-{random.randint(70, 99)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}"

        # Last donation date (some donors, not all)
        last_donation = None
        if random.choice([True, False]):
            days_ago = random.randint(30, 365)
            last_donation = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

        donor_data = {
            'id': donor_id,
            'name': name,
            'email': email,
            'phone': phone,
            'age': age,
            'gender': gender,
            'city': city,
            'address': f"{random.randint(1, 999)} {random.choice(['MG Road', 'Park Street', 'Mall Road', 'Station Road'])}, {city}",
            'blood_group': blood_group,
            'organs': organs,
            'medical_history': random.choice([
                "", 
                "No significant medical history", 
                "Hypertension controlled with medication",
                "Diabetic, well controlled",
                "Occasional allergies"
            ]),
            'last_donation': last_donation,
            'available': random.choice([True, True, True, False]),  # 75% available
            'registered_date': (datetime.now() - timedelta(days=random.randint(1, 730))).isoformat()
        }

        sample_donors[donor_id] = donor_data

    return sample_donors

def generate_sample_requests(num_requests=20):
    """Generate sample donation requests"""
    sample_requests = {}

    for i in range(num_requests):
        request_id = str(uuid.uuid4())

        # Random request data
        request_type = random.choice(["blood", "blood", "blood", "organ"])  # More blood requests
        city = random.choice(SAMPLE_CITIES)
        hospital = random.choice(HOSPITALS)
        urgency = random.choice(["critical", "urgent", "urgent", "moderate"])  # Weight toward urgent

        # Patient names
        patient_name = random.choice([
            "Rahul Kumar", "Sunita Sharma", "Vikash Patel", "Meera Gupta", "Arjun Singh",
            "Kavya Reddy", "Rohit Verma", "Anita Joshi", "Sanjay Malhotra", "Deepika Nair"
        ])

        contact_person = random.choice([
            "Dr. " + random.choice(["Sharma", "Patel", "Kumar", "Singh", "Gupta"]),
            patient_name + "'s family member"
        ])

        phone = f"+91-{random.randint(70, 99)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
        email = f"contact{random.randint(100, 999)}@{hospital.lower().replace(' ', '').replace('.', '')}.com"

        request_data = {
            'id': request_id,
            'patient_name': patient_name,
            'contact_person': contact_person,
            'phone': phone,
            'email': email,
            'city': city,
            'hospital': hospital,
            'type': request_type,
            'urgency': urgency,
            'quantity': random.randint(1, 4) if request_type == 'blood' else 1,
            'max_distance': random.choice([25, 50, 100]),
            'additional_info': random.choice([
                "Patient needs immediate assistance due to emergency surgery",
                "Regular dialysis patient requiring weekly donation",
                "Post-accident patient in ICU, critical condition",
                "Cancer patient undergoing chemotherapy treatment",
                "Scheduled surgery next week, please arrange donation",
                "Elderly patient with complications, urgent care needed"
            ]),
            'status': random.choice(['active', 'active', 'active', 'matched']),  # Mostly active
            'created_date': (datetime.now() - timedelta(hours=random.randint(1, 48))).isoformat()
        }

        if request_type == 'blood':
            request_data['blood_group'] = random.choice(BLOOD_GROUPS)
        else:
            request_data['organ'] = random.choice(ORGANS)

        sample_requests[request_id] = request_data

    return sample_requests

def print_sample_data_summary(donors, requests):
    """Print summary of generated sample data"""
    print("\n" + "="*50)
    print("📊 SAMPLE DATA GENERATED FOR LIFELINK")
    print("="*50)

    print(f"\n👥 DONORS GENERATED: {len(donors)}")
    print(f"   • Available: {len([d for d in donors.values() if d['available']])}")
    print(f"   • Cities: {len(set(d['city'] for d in donors.values()))}")

    blood_groups = {}
    for donor in donors.values():
        bg = donor['blood_group']
        blood_groups[bg] = blood_groups.get(bg, 0) + 1

    print("   • Blood Groups:")
    for bg, count in sorted(blood_groups.items()):
        print(f"     - {bg}: {count} donors")

    print(f"\n📋 REQUESTS GENERATED: {len(requests)}")
    print(f"   • Blood Requests: {len([r for r in requests.values() if r['type'] == 'blood'])}")
    print(f"   • Organ Requests: {len([r for r in requests.values() if r['type'] == 'organ'])}")
    print(f"   • Critical: {len([r for r in requests.values() if r['urgency'] == 'critical'])}")
    print(f"   • Urgent: {len([r for r in requests.values() if r['urgency'] == 'urgent'])}")

    print("\n🎯 TO USE THIS DATA:")
    print("1. Start your Flask app: python blood_donation_app.py")
    print("2. Run this script to populate data")
    print("3. Refresh your browser to see populated data")

    print("\n💡 DEMO FEATURES TO SHOWCASE:")
    print("• Browse registered donors by blood group")
    print("• View active requests with urgency levels")
    print("• Test donor registration with new data")
    print("• Submit new requests to see matching")
    print("• Explore donor dashboard with notifications")

if __name__ == "__main__":
    # Generate sample data
    print("🔄 Generating sample data for LifeLink...")

    donors = generate_sample_donors(50)
    requests = generate_sample_requests(20)

    print_sample_data_summary(donors, requests)

    print("\n✅ Sample data generated successfully!")
    print("🚀 Your LifeLink system now has realistic demo data!")
