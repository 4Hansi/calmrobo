# backend/tests/flow_test.py
import requests

BASE = "http://127.0.0.1:8000"

# Signup
r = requests.post(f"{BASE}/auth/signup", json={"email":"hackdemo@example.com","password":"pass1234"})
print("signup:", r.status_code, r.text)

# Login
r = requests.post(f"{BASE}/auth/login", json={"email":"hackdemo@example.com","password":"pass1234"})
print("login:", r.status_code, r.text)
token = r.json().get("access_token")

# Chat
headers = {"Authorization": f"Bearer {token}"} if token else {}
msg = "I'm 30, want moderate growth and can tolerate some volatility."
r = requests.post(f"{BASE}/chat", json={"message": msg}, headers=headers)
print("chat:", r.status_code, r.text)
