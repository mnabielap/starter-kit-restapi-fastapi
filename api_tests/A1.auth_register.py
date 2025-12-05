import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import utils

# --- SETUP ---
ENDPOINT = "/auth/register"
OUTPUT_FILE = f"{os.path.splitext(os.path.basename(__file__))[0]}.json"

payload = {
    "email": "newuser@example.com",
    "password": "password123",
    "name": "New Registered User"
}

# --- EXECUTE ---
response = utils.send_and_print(
    url=f"{utils.BASE_URL}{ENDPOINT}",
    method="POST",
    body=payload,
    output_file=OUTPUT_FILE
)

if response.status_code == 201:
    print("Registration Successful!")