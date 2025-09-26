import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

config = load_json(CONFIG_FILE)
API_KEY = config.get("API_KEY")
user_id = config.get("USER_ID")
pin = config.get("PIN")
totp_token = config.get("TOPT_TOKEN")

smart_api = SmartConnect(API_KEY)
totp_code = pyotp.TOTP(totp_token).now()
data = smart_api.generateSession(user_id, pin, totp_code)

session_data = data.get("data", {})
AUTH_TOKEN = session_data.get("jwtToken")
FEED_TOKEN = session_data.get("feedToken")
REFRESH_TOKEN = session_data.get("refreshToken")

res = smart_api.getProfile(REFRESH_TOKEN)

print("Profile:", res)



# https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json
############## WEB SOCKET ####################
from SmartApi.smartWebSocketV2 import SmartWebSocketV2

CLIENT_CODE = user_id
correlation_id = "abc123"
action = 1
mode = 1

token_list = [
    {
        "exchangeType": 1,
        "tokens": ["26009", "2885"]
    }
]
token_list1 = [
    {
        "action": 0,
        "exchangeType": 1,
        "tokens": ["26009"]
    }
]

sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN)

def on_data(wsapp, message):
    logger.info("Ticks: {}".format(message))
    # close_connection()

def on_open(wsapp):
    logger.info("on open")
    sws.subscribe(correlation_id, mode, token_list)
    # sws.unsubscribe(correlation_id, mode, token_list1)


def on_error(wsapp, error):
    logger.error(error)


def on_close(wsapp):
    logger.info("Close")



def close_connection():
    sws.close_connection()


# Assign the callbacks.
sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error
sws.on_close = on_close

sws.connect()
