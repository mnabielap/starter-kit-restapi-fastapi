import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import utils

# --- SETUP ---
ENDPOINT = "/users"
OUTPUT_FILE = f"{os.path.splitext(os.path.basename(__file__))[0]}.json"

access_token = utils.load_config("access_token")
if not access_token:
    print("ERROR: access_token not found. Run auth_login.py first.")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {access_token}"
}

payload = {
    "email": "createdbyadmin@example.com",
    "password": "password123",
    "name": "User Created By Admin",
    "role": "user"
}

# --- EXECUTE ---
response = utils.send_and_print(
    url=f"{utils.BASE_URL}{ENDPOINT}",
    method="POST",
    headers=headers,
    body=payload,
    output_file=OUTPUT_FILE
)

# --- SAVE TARGET ID ---
if response.status_code == 201:
    data = response.json()
    new_id = data.get("id")
    if new_id:
        utils.save_config("target_user_id", new_id)
        print(f">> Target User ID {new_id} saved to secrets.json for CRUD tests")