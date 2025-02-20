import requests

def add_user(i):
    url = "http://localhost:5000/users"
    payload = {
        "username": f"teacher{i:03}",
        "password": f"password{i:03}",
        "role": "teacher",
        "student_id": "null"
    }

    headers = {'Content-Type': 'application/json'}
    # Use 'json' instead of 'params'
    r = requests.post(url, json=payload, headers=headers)

    if r.status_code == 201:
        print(f"{i} User added successfully")
    else:
        print(f"Failed to add student. Status code: {r.status_code}, Response: {r.text}")

def auth():
    url = "http://localhost:5000/users/authenticate"
    payload ={
        "username": "xiaming",
        "password": "test002"
    }

    headers = {'Content-Type': 'application/json'}
    # Use 'json' instead of 'params'
    r = requests.post(url, json=payload, headers=headers)

    print(r.text)

def delete_user():
    url = "http://localhost:5000/users/user_9f2a4b6d7e"
    r = requests.delete(url)

def update_user():
    url = "http://localhost:5000/users/user_94b6755e"
    payload = { 
        "username": "teacher001",
        "old_password": "123456",
        "new_password": "test001",
        "role": "teacher"
    }

    headers = {'Content-Type': 'application/json'}

    r = requests.put(url, json=payload, headers=headers)
    print(r.text)

def addStudent():
    url = "http://localhost:5000/tc_students"

    payload = {
        "name": "John",
        "age": 12,
        "disorder_category": "ADHD"
    }

    headers = {'Content-Type': 'application/json'}
    # Use 'json' instead of 'params'
    r = requests.post(url, json=payload, headers=headers)
    print(r.text)
    

for i in range(1, 21):
    add_user(i)





