import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import utils

# --- SETUP ---
ENDPOINT = "/auth/verify-email"
OUTPUT_FILE = f"{os.path.splitext(os.path.basename(__file__))[0]}.json"

# SIMULASI: Ganti string ini dengan token dari log server
VERIFY_TOKEN = "paste-token-from-server-log-here" 

url_with_query = f"{utils.BASE_URL}{ENDPOINT}?token={VERIFY_TOKEN}"

# --- EXECUTE ---
utils.send_and_print(
    url=url_with_query,
    method="POST",
    output_file=OUTPUT_FILE
)