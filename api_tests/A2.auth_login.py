import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import utils

# --- SETUP ---
ENDPOINT = "/auth/login"
OUTPUT_FILE = f"{os.path.splitext(os.path.basename(__file__))[0]}.json"

# Menggunakan kredensial Admin default dari init_db.py
payload = {
    "email": "admin@example.com",
    "password": "password123"
}

# --- EXECUTE ---
response = utils.send_and_print(
    url=f"{utils.BASE_URL}{ENDPOINT}",
    method="POST",
    body=payload,
    output_file=OUTPUT_FILE
)

# --- SAVE TOKENS AUTOMATICALLY ---
if response.status_code == 200:
    data = response.json()
    if data:
        # Save Access Token
        access_token = data.get("tokens", {}).get("access", {}).get("token")
        if access_token:
            utils.save_config("access_token", access_token)
            print(">> Access Token saved to secrets.json")
        
        # Save Refresh Token
        refresh_token = data.get("tokens", {}).get("refresh", {}).get("token")
        if refresh_token:
            utils.save_config("refresh_token", refresh_token)
            print(">> Refresh Token saved to secrets.json")

        # Save User ID (Admin ID)
        user_id = data.get("user", {}).get("id")
        if user_id:
            utils.save_config("current_user_id", user_id)