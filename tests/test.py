import requests
import json

def add_student():
    url = "http://localhost:5000/students"
    payload = {
        "student_id": 1,
        "username": "John",
        "password": "123456",
        "age": 18,
        "disorder_category": "ADHD",
        "created_at": "2021-01-01 00:00:00"
    }

    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data = json.dumps(payload), headers = headers)

    if r.status_code == 201:
        print("Student added successfully")


add_student()