import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import utils

# --- SETUP ---
ENDPOINT = "/auth/logout"
OUTPUT_FILE = f"{os.path.splitext(os.path.basename(__file__))[0]}.json"

refresh_token = utils.load_config("refresh_token")

if not refresh_token:
    print("ERROR: No refresh token found. Run auth_login.py first.")
    sys.exit(1)

payload = {
    "refreshToken": refresh_token
}

# --- EXECUTE ---
utils.send_and_print(
    url=f"{utils.BASE_URL}{ENDPOINT}",
    method="POST",
    body=payload,
    output_file=OUTPUT_FILE
)