import os
import logging
from datetime import datetime, timedelta, timezone
from kiteconnect import KiteConnect
from utils.json_utils import load_json, save_json, is_token_valid

# ================= CONFIG ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
TOKEN_FILE = os.path.join(BASE_DIR, "tokens.json")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ZerodhaSession:
    """Manage Zerodha login, tokens, and KiteConnect session."""

    def __init__(self):
        self.config = load_json(CONFIG_FILE)
        self.tokens = load_json(TOKEN_FILE)
        self.api_key = self.config.get("API_KEY")
        self.secret_key = self.config.get("SECRET_KEY")
        self.access_token = None
        self.kite = None

        if not self.api_key or not self.secret_key:
            raise ValueError("❌ API_KEY or SECRET_KEY not found in config.json")

        self._initialize_session()

    def _initialize_session(self):
        """Initialize access token and KiteConnect instance."""
        if is_token_valid(self.tokens):
            logger.info("✅ Using existing access token.")
            self.access_token = self.tokens["access_token"]
        else:
            self.access_token = self._login_and_store_token()

        # Initialize KiteConnect instance
        self.kite = KiteConnect(api_key=self.api_key)
        self.kite.set_access_token(self.access_token)

    def _login_and_store_token(self):
        """Prompt user for login and store access token."""
        kite = KiteConnect(api_key=self.api_key)
        logger.info("🔑 Generating new access token. Please login...")

        login_url = kite.login_url()
        print(f"Please login here: {login_url}")
        request_token = input("Enter the request token: ").strip()

        data = kite.generate_session(request_token, api_secret=self.secret_key)

        # Save tokens
        self.tokens = {
            "request_token": request_token,
            "access_token": data["access_token"],
            "public_token": data.get("public_token"),
            "refresh_token": data.get("refresh_token"),
            "enctoken": data.get("enctoken"),
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
        save_json(TOKEN_FILE, self.tokens)
        logger.info("✅ New access token generated and saved.")
        return data["access_token"]

    def get_access_token(self):
        """Return the current valid access token."""
        return self.access_token

    def get_kite_session(self):
        """Return the ready KiteConnect instance."""
        return self.kite


# ================= RUN DIRECTLY ==================
if __name__ == "__main__":
    session = ZerodhaSession()
    print("🎉 Kite session ready!")
    print("Access Token:", session.get_access_token())
    print("Profile:", session.get_kite_session().profile())
