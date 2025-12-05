import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import utils

# --- SETUP ---
ENDPOINT = "/auth/forgot-password"
OUTPUT_FILE = f"{os.path.splitext(os.path.basename(__file__))[0]}.json"

payload = {
    "email": "admin@example.com"
}

# --- EXECUTE ---
utils.send_and_print(
    url=f"{utils.BASE_URL}{ENDPOINT}",
    method="POST",
    body=payload,
    output_file=OUTPUT_FILE
)
print("Check your server logs for the Reset Token.")