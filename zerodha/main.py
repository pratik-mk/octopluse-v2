from kiteconnect import KiteConnect
from login import get_access_token, load_json

CONFIG_FILE = "config.json"

# Load config
config = load_json(CONFIG_FILE)
API_KEY = config.get("API_KEY")

# Get valid access token
access_token = get_access_token()

# Initialize Kite
kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(access_token)

print("✅ Trading session ready with access token:", access_token)

# Example: Get profile
print(kite.profile())