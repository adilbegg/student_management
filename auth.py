import csv
import hashlib

USERS_FILE = "users.csv"
USER_HEADERS = ["username", "password_hash"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    users = {}

    with open(USERS_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            username = row.get("username")
            password_hash = row.get("password_hash")

            if username and password_hash:
                users[username] = password_hash

    return users

def save_users(users):
    
    with open(USERS_FILE, "w", newline= "") as file:
        writer = csv.DictWriter(file, fieldnames = USER_HEADERS)
        writer.writeheader()

        for username, password_hash in users.items():
            writer.writerow({
                "username": username,
                "password_hash": password_hash
            })


def login(username, password):

    username = username.strip()
    users = load_users()

    if username not in users:
        return False
    
    return users[username] == hash_password(password)

def create_account(username, password):

    username = username.strip()

    if len(password) < 6:
        raise ValueError("Password must be atleast 6 characters")
    
    users = load_users()

    if username in users:
        raise ValueError("Username already exists!")
    
    users[username] = hash_password(password)
    save_users(users)

    return True