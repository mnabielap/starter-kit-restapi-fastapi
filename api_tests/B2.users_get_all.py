import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import utils

# --- SETUP ---
ENDPOINT = "/users?limit=10&page=1"
OUTPUT_FILE = f"{os.path.splitext(os.path.basename(__file__))[0]}.json"

access_token = utils.load_config("access_token")
if not access_token:
    print("ERROR: access_token not found. Run auth_login.py first.")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {access_token}"
}

# --- EXECUTE ---
utils.send_and_print(
    url=f"{utils.BASE_URL}{ENDPOINT}",
    method="GET",
    headers=headers,
    output_file=OUTPUT_FILE
)