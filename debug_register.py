import requests

url = "http://localhost:8000/auth/registration/"
data = {
    "username": "debug_user_1",
    "email": "debug@test.com",
    "password": "password123"
}

try:
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
