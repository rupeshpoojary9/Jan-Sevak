import requests
import json

BASE_URL = "http://localhost:8000"
USERNAME = "rupesh1"
PASSWORD = "password123$"

def test_list():
    session = requests.Session()
    
    # 1. Login
    login_url = f"{BASE_URL}/auth/login/"
    login_data = {"username": USERNAME, "password": PASSWORD}
    try:
        resp = session.post(login_url, json=login_data)
        if resp.status_code != 200:
            print("Login Failed")
            return
    except Exception as e:
        print(f"Login Error: {e}")
        return

    # 2. Get List
    url = f"{BASE_URL}/api/complaints/"
    resp = session.get(url)
    if resp.status_code == 200:
        data = resp.json()
        results = data.get('results', data) # Handle pagination or flat list
        
        if results and isinstance(results, list) and len(results) > 0:
            latest = results[0]
            print(json.dumps(latest, indent=4))
        else:
            print("No complaints found in list.")
    else:
        print(f"Error: {resp.status_code}")

if __name__ == "__main__":
    test_list()
