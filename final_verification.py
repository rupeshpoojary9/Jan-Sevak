import requests
import time
import os
import random
import string

# Configuration
BASE_URL = "http://localhost:8000"
USERNAME = "final_tester_" + ''.join(random.choices(string.ascii_lowercase, k=5))
PASSWORD = "StrongPass123!@#"

def create_user_and_login():
    print(f"👤 Creating user: {USERNAME}...")
    # Register
    reg_url = f"{BASE_URL}/auth/registration/"
    reg_data = {"username": USERNAME, "password": PASSWORD, "password1": PASSWORD, "password2": PASSWORD, "email": f"{USERNAME}@example.com"}
    res = requests.post(reg_url, json=reg_data)
    
    if res.status_code == 201:
        print("   -> Registration successful! Getting token...")
        # dj_rest_auth returns token on registration usually
        if 'access' in res.json():
            return res.json()['access']
        elif 'key' in res.json():
             return res.json()['key']
    else:
        print(f"   -> Registration note: {res.text}")

    # Login (fallback if user already exists or token not returned)
    print("🔑 Logging in...")
    login_url = f"{BASE_URL}/auth/login/"
    login_data = {"username": USERNAME, "password": PASSWORD}
    res = requests.post(login_url, json=login_data)
    
    if res.status_code != 200:
        print(f"❌ Login failed: {res.text}")
        exit(1)
        
    return res.json()['access']

def test_valid_complaint(token):
    print("\n✅ Testing VALID Complaint (Pothole)...")
    url = f"{BASE_URL}/api/complaints/"
    headers = {'Authorization': f'Bearer {token}'}
    
    data = {
        'title': 'Deep Pothole on Main Street',
        'description': 'There is a very deep pothole here that is causing accidents. It is about 2 feet wide and needs immediate repair.',
        'category': 'POTHOLE',
        'ward': 1, # Assuming Ward 1 exists
        'latitude': 19.0760,
        'longitude': 72.8777,
        'location_address': 'Dadar West'
    }
    
    # We won't send an image to keep it simple (AI analyzes text too)
    res = requests.post(url, data=data, headers=headers)
    
    if res.status_code == 201:
        print("   -> Submitted successfully!")
        c_id = res.json()['id']
        score = res.json().get('urgency_score', 0)
        print(f"   -> Urgency Score: {score}")
        if score > 0:
            print("   -> 🟢 AI Analysis: PASSED (Score assigned)")
        else:
            print("   -> 🟡 AI Analysis: PENDING or FAILED (Score is 0)")
    else:
        print(f"   -> ❌ Failed: {res.status_code} - {res.text}")

def test_invalid_complaint(token):
    print("\n🚫 Testing INVALID Complaint (Spam/Testing)...")
    url = f"{BASE_URL}/api/complaints/"
    headers = {'Authorization': f'Bearer {token}'}
    
    data = {
        'title': 'Just testing the app',
        'description': 'This is just a test description for testing purposes only. ignore this.',
        'category': 'OTHERS',
        'ward': 1,
        'latitude': 19.0760,
        'longitude': 72.8777,
        'location_address': 'Test Loc'
    }
    
    res = requests.post(url, data=data, headers=headers)
    
    if res.status_code == 400:
        print("   -> 🟢 AI Rejection: PASSED (Correctly rejected)")
        print(f"   -> Error Message: {res.text}")
    elif res.status_code == 201:
        print("   -> ❌ AI Rejection: FAILED (Complaint was accepted but should have been rejected)")
    else:
        print(f"   -> ❓ Unexpected Status: {res.status_code} - {res.text}")

if __name__ == "__main__":
    print("🚀 Starting Final System Verification...")
    token = create_user_and_login()
    test_valid_complaint(token)
    test_invalid_complaint(token)
    print("\n🏁 Verification Complete.")
