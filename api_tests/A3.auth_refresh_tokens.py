import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import utils

# --- SETUP ---
ENDPOINT = "/auth/refresh-tokens"
OUTPUT_FILE = f"{os.path.splitext(os.path.basename(__file__))[0]}.json"

# Load Refresh Token from secrets
refresh_token = utils.load_config("refresh_token")

if not refresh_token:
    print("ERROR: No refresh token found in secrets.json. Please run auth_login.py first.")
    sys.exit(1)

payload = {
    "refreshToken": refresh_token
}

# --- EXECUTE ---
response = utils.send_and_print(
    url=f"{utils.BASE_URL}{ENDPOINT}",
    method="POST",
    body=payload,
    output_file=OUTPUT_FILE
)

# --- UPDATE SAVED TOKENS ---
if response.status_code == 200:
    data = response.json()
    # Update new access token
    new_access = data.get("access", {}).get("token")
    if new_access:
        utils.save_config("access_token", new_access)
    
    # Update new refresh token
    new_refresh = data.get("refresh", {}).get("token")
    if new_refresh:
        utils.save_config("refresh_token", new_refresh)
        
    print(">> Tokens refreshed and updated in secrets.json")