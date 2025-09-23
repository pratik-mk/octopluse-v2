import os
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict


def load_json(file_path: str) -> Dict[str, Any]:
    """
    Safely load a JSON file. Returns empty dict if file does not exist.
    
    Args:
        file_path (str): Path to the JSON file.
        
    Returns:
        dict: Parsed JSON data or empty dict.
    """
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Invalid JSON, return empty dict
        return {}
    except Exception as e:
        raise IOError(f"Error reading JSON file {file_path}: {e}")


def save_json(file_path: str, data: Dict[str, Any]) -> None:
    """
    Safely save a dictionary to a JSON file.
    
    Args:
        file_path (str): Path to save the JSON file.
        data (dict): Data to save.
    """
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise IOError(f"Error writing JSON file {file_path}: {e}")


def is_token_valid(tokens: Dict[str, Any]) -> bool:
    """
    Check if a Zerodha access token is still valid (before 6 AM next day).
    
    Args:
        tokens (dict): Token dictionary containing 'access_token' and 'generated_at'.
        
    Returns:
        bool: True if token is valid, False if expired or missing.
    """
    if "access_token" not in tokens or "generated_at" not in tokens:
        return False

    try:
        generated_at = datetime.fromisoformat(tokens["generated_at"])
        now = datetime.now(timezone.utc)  # Always compare in UTC

        # Zerodha tokens expire at 6 AM UTC next day
        expiry_time = generated_at.replace(hour=6, minute=0, second=0, microsecond=0) + timedelta(days=1)
        return now < expiry_time
    except Exception:
        return False
