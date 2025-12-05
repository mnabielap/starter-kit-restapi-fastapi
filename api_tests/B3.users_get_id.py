import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import utils

# --- SETUP ---
target_id = utils.load_config("target_user_id")

if not target_id:
    print("ERROR: target_user_id not found. Run users_create.py first.")
    sys.exit(1)

ENDPOINT = f"/users/{target_id}"
OUTPUT_FILE = f"{os.path.splitext(os.path.basename(__file__))[0]}.json"

access_token = utils.load_config("access_token")
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