import requests

def add_user():
    url = "http://localhost:5000/users"
    payload = {
        "username": "John",
        "password": "123456",
        "role": "teacher",
    }

    headers = {'Content-Type': 'application/json'}
    # Use 'json' instead of 'params'
    r = requests.post(url, json=payload, headers=headers)

    if r.status_code == 201:
        print("Student added successfully")
    else:
        print(f"Failed to add student. Status code: {r.status_code}, Response: {r.text}")

def auth():
    url = "http://localhost:5000/users/authenticate"
    payload ={
        "username": "John",
        "password": "1234567"
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

update_user()
