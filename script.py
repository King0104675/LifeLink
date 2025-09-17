# Let's first examine the current Flask app structure to understand the data storage
with open('blood_donation_app.py', 'r') as f:
    content = f.read()

print("Current data storage structures in the app:")
print("==========================================")

# Extract the data storage variables
lines = content.split('\n')
for i, line in enumerate(lines):
    if line.strip() and ('= {}' in line or '= []' in line) and not line.strip().startswith('#'):
        print(f"Line {i+1}: {line.strip()}")
        
print("\n\nIdentifying data structures that need CSV storage:")
print("================================================")
data_structures = ['donors', 'recipients', 'blood_banks', 'active_requests', 'notifications', 'accepted_matches']
for struct in data_structures:
    if f"{struct} = {{}}" in content:
        print(f"✓ {struct} - Dictionary (needs CSV conversion)")