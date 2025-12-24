import requests
import json

BASE_URL = "http://localhost:8000"

def register_and_login():
    session = requests.Session()
    
    # Get CSRF token
    session.get(f"{BASE_URL}/api/auth/login/")
    csrftoken = session.cookies.get('csrftoken')
    headers = {"X-CSRFToken": csrftoken} if csrftoken else {}

    # Register
    username = "rupesh_api_test_2"
    email = "imrupesh24@gmail.com"
    password = "Password@123"
    
    print(f"Registering {username}...")
    resp = session.post(f"{BASE_URL}/api/auth/register/", json={
        "username": username,
        "email": email,
        "password": password,
        "confirm_password": password
    }, headers=headers)
    
    if resp.status_code == 201 or "already exists" in resp.text:
        print("Registration successful or user exists.")
    else:
        print(f"Registration failed: {resp.text}")
        # Continue to login anyway

    # Login
    print(f"Logging in {username}...")
    resp = session.post(f"{BASE_URL}/api/auth/login/", json={
        "username": username,
        "password": password
    }, headers=headers)
    
    if resp.status_code == 200:
        token = resp.json().get("key")
        print(f"Login successful. Token: {token}")
        return token
    else:
        print(f"Login failed: {resp.text}")
        return None

def submit_complaint(token):
    headers = {"Authorization": f"Token {token}"}
    data = {
        "title": "API Test for CC Feature",
        "description": "Testing if CC email is sent via API submission.",
        "category": "OTHERS",
        "ward": "1",
        "location_address": "Test Location",
        "is_anonymous": False,
        "cc_reporter": True
    }
    
    print("Submitting complaint...")
    resp = requests.post(f"{BASE_URL}/api/complaints/", json=data, headers=headers)
    
    if resp.status_code == 201:
        print("Complaint submitted successfully.")
        print(f"Response: {resp.json()}")
        return resp.json()['id']
    else:
        print(f"Complaint submission failed: {resp.text}")
        return None

if __name__ == "__main__":
    token = register_and_login()
    if token:
        submit_complaint(token)

