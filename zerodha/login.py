import os
import json
import logging
from datetime import datetime, timedelta
from kiteconnect import KiteConnect

# ================= CONFIG ==================
CONFIG_FILE = "config.json"   # contains API_KEY and SECRET_KEY
TOKEN_FILE = "tokens.json"    # stores access/refresh tokens

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ================= UTILS ==================
def load_json(file):
    """Load JSON file safely."""
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)


def save_json(file, data):
    """Save data into JSON file."""
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


def is_token_valid(tokens):
    """Check if access token is still valid (before next 6 AM)."""
    if "access_token" not in tokens or "generated_at" not in tokens:
        return False

    generated_at = datetime.fromisoformat(tokens["generated_at"])
    now = datetime.now()

    # Zerodha tokens expire at 6 AM every day
    expiry_time = generated_at.replace(hour=6, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return now < expiry_time


# ================= MAIN ==================
def login_and_store_token():
    """Handle login and store access token in tokens.json."""
    config = load_json(CONFIG_FILE)
    tokens = load_json(TOKEN_FILE)

    API_KEY = config.get("API_KEY")
    SECRET_KEY = config.get("SECRET_KEY")

     # If valid token exists, reuse it
    if is_token_valid(tokens):
        logger.info("✅ Access token is still valid. No need to re-login.")
        return tokens["access_token"]

    # Otherwise, regenerate
    if not API_KEY or not SECRET_KEY:
        raise ValueError("❌ API_KEY or SECRET_KEY not found in config.json")

    kite = KiteConnect(api_key=API_KEY)


    logger.info("🔑 Generating new access token. Please login...")

    login_url = kite.login_url()
    print(f"Please login here: {login_url}")
    request_token = input("Enter the request token: ").strip()

    data = kite.generate_session(request_token, api_secret=SECRET_KEY)

    # Save updated tokens
    tokens = {
        "request_token": request_token,
        "access_token": data["access_token"],
        "public_token": data.get("public_token"),
        "refresh_token": data.get("refresh_token"),
        "enctoken": data.get("enctoken"),
        "generated_at": datetime.now().isoformat()
    }
    save_json(TOKEN_FILE, tokens)

    logger.info("✅ New access token generated and saved.")
    return tokens["access_token"]


def get_access_token():
    """Return valid access token (re-login if needed)."""
    tokens = load_json(TOKEN_FILE)

    if is_token_valid(tokens):
        return tokens["access_token"]

    # If invalid, regenerate by login
    return login_and_store_token()


if __name__ == "__main__":
    # Running this file directly will refresh/login and save tokens
    token = get_access_token()
    print(f"🎉 Your access token: {token}")
