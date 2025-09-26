import os
import logging
from datetime import datetime, timezone
from SmartApi import SmartConnect
import pyotp
from utils.json_utils import load_json, save_json, is_token_valid

# ================= CONFIG ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
TOKEN_FILE = os.path.join(BASE_DIR, "tokens.json")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AngelSession:
    """Manage Angel login, tokens, and SmartConnect session."""

    def __init__(self):
        self.config = load_json(CONFIG_FILE)
        self.tokens = load_json(TOKEN_FILE)

        self.api_key = self.config.get("API_KEY")
        self.user_id = self.config.get("USER_ID")
        self.pin = self.config.get("PIN")
        self.totp_token = self.config.get("TOPT_TOKEN")

        if not all([self.api_key, self.user_id, self.pin, self.totp_token]):
            raise ValueError("❌ API_KEY, USER_ID, PIN, or TOPT_TOKEN missing in config.json")

        # SmartAPI object
        self.smart_api = SmartConnect(api_key=self.api_key)

        self.access_token = None
        self.feed_token = None
        self.refresh_token = None

        self._initialize_session()

    def _initialize_session(self):
        """Initialize tokens and SmartConnect instance."""
        if is_token_valid(self.tokens):
            logger.info("✅ Using existing tokens.")
            self._set_tokens(self.tokens)
        else:
            self._login_and_store_token()

    def _set_tokens(self, data: dict):
        self.access_token = data.get("jwtToken")
        self.feed_token = data.get("feedToken")
        self.refresh_token = data.get("refreshToken")

    def _login_and_store_token(self):
        """Login via SmartAPI and save fresh tokens."""
        logger.info("🔑 Generating new session tokens...")
        totp = pyotp.TOTP(self.totp_token).now()
        data = self.smart_api.generateSession(self.user_id, self.pin, totp)

        if not data.get("status"):
            raise ValueError(f"Login failed: {data.get('message')}")

        session_data = data["data"]
        self._set_tokens(session_data)

        self.tokens = {
            "jwtToken": self.access_token,
            "feedToken": self.feed_token,
            "refreshToken": self.refresh_token,
            "clientcode": session_data.get("clientcode"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        save_json(TOKEN_FILE, self.tokens)
        logger.info("✅ New tokens generated and saved.")

    # ---------- Public Getters ----------
    def get_access_token(self): return self.access_token
    def get_feed_token(self): return self.feed_token
    def get_refresh_token(self): return self.refresh_token

    def get_smart_api(self):
        """Return SmartConnect instance (ready to use)."""
        return self.smart_api

    def get_profile(self):
        """Fetch user profile using jwtToken."""
        return self.smart_api.getProfile(self.access_token)

# ================= RUN DIRECTLY ==================
if __name__ == "__main__":
    session = AngelSession()
    print("🎉 Angel SmartConnect session ready!")
    print("Profile:", session.get_profile())
