import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import utils

# --- SETUP ---
ENDPOINT = "/auth/reset-password"
OUTPUT_FILE = f"{os.path.splitext(os.path.basename(__file__))[0]}.json"

# SIMULASI: Ganti string ini dengan token yang muncul di log server
# setelah menjalankan auth_forgot_password.py
RESET_TOKEN = "paste-token-from-server-log-here" 

url_with_query = f"{utils.BASE_URL}{ENDPOINT}?token={RESET_TOKEN}"

payload = {
    "password": "newPassword123"
}

# --- EXECUTE ---
utils.send_and_print(
    url=url_with_query,
    method="POST",
    body=payload,
    output_file=OUTPUT_FILE
)