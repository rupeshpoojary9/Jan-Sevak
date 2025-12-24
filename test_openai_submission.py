import requests
import os

BASE_URL = "http://localhost:8000"
USERNAME = "rupesh1"
PASSWORD = "password123$"

def test_submission():
    session = requests.Session()
    
    # 1. Login
    print(f"Logging in as {USERNAME}...")
    login_url = f"{BASE_URL}/auth/login/"
    login_data = {"username": USERNAME, "password": PASSWORD}
    
    try:
        resp = session.post(login_url, json=login_data)
        if resp.status_code != 200:
            print(f"Login Failed: {resp.status_code} - {resp.text}")
            return
        print("Login Successful.")
        token = resp.json().get('key')
        # If using Token auth, add header. If Session, cookie is handled by session.
        # dj-rest-auth usually returns a token.
        if token:
            session.headers.update({'Authorization': f'Token {token}'})
            
    except Exception as e:
        print(f"Login Error: {e}")
        return

    # 2. Submit Complaint
    print("Submitting Complaint...")
    complaint_url = f"{BASE_URL}/api/complaints/"
    data = {
        "title": "Overflowing Garbage Bin",
        "description": "There is a huge pile of garbage on the street that has not been collected for days. It smells bad.",
        "category": "GARBAGE",
        "ward": "1", # Assuming Ward ID 1 exists
        "location_address": "Test Location",
        "latitude": "19.0760",
        "longitude": "72.8777",
        "is_anonymous": "false"
    }
    
    try:
        # Open image file
        with open("/app/test_image.jpg", "rb") as img:
            files = {'images': img}
            resp = session.post(complaint_url, data=data, files=files) 
            print(f"Submission Status: {resp.status_code}")
            print(f"Response: {resp.text}")
        
    except Exception as e:
        print(f"Submission Error: {e}")

if __name__ == "__main__":
    test_submission()
