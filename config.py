"""
Configuration module for DSS SkyNet Scraper.
Loads credentials from .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

DSS_USERNAME = os.getenv("DSS_USERNAME")
DSS_PASSWORD = os.getenv("DSS_PASSWORD")
DSS_LINK = os.getenv("DSS_LINK")
DSS_PIN = os.getenv("DSS_PIN", "demodss")

API_BASE_URL = "https://api.x-find.live/api/v3"
LOGIN_ENDPOINT = f"{API_BASE_URL}/user/login"

HEADERS = {
    "Content-Type": "application/json",
    "x-api-name": "user login",
    "x-api-vers": "v3",
    "Access-Control-Allow-Origin": "*"
}
