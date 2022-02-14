import os
from dotenv import load_dotenv
from json import dump

# File responsible for loading sensitive variables
if os.path.isfile("./.env"):
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    COMMANDS_SHEET_ID = os.getenv("COMMANDS_SHEET_ID")
    ELE_SHEET_ID = os.getenv("ELE_SHEET_ID")
    MEC_SHEET_ID = os.getenv("MEC_SHEET_ID")

    GOOGLE_CREDS_TYPE = os.getenv("GOOGLE_CREDS_TYPE")
    GOOGLE_CREDS_PROJECT_ID = os.getenv("GOOGLE_CREDS_PROJECT_ID")
    GOOGLE_CREDS_PRIVATE_KEY_ID = os.getenv("GOOGLE_CREDS_PRIVATE_KEY_ID")
    GOOGLE_CREDS_PRIVATE_KEY = os.getenv("GOOGLE_CREDS_PRIVATE_KEY")
    GOOGLE_CREDS_EMAIL = os.getenv("GOOGLE_CREDS_EMAIL")
    GOOGLE_CREDS_CLIENT_ID = os.getenv("GOOGLE_CREDS_CLIENT_ID")
    GOOGLE_CREDS_AUTH_URI = os.getenv("GOOGLE_CREDS_AUTH_URI")
    GOOGLE_CREDS_TOKEN_URI = os.getenv("GOOGLE_CREDS_TOKEN_URI")
    GOOGLE_CREDS_AUTH_PROVIDER = os.getenv("GOOGLE_CREDS_AUTH_PROVIDER")
    GOOGLE_CREDS_CLIENT = os.getenv("GOOGLE_CREDS_CLIENT")

else:
    TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    COMMANDS_SHEET_ID = os.environ["COMMANDS_SHEET_ID"]
    ELE_SHEET_ID = os.environ["ELE_SHEET_ID"]
    MEC_SHEET_ID = os.environ["MEC_SHEET_ID"]

    GOOGLE_CREDS_TYPE = os.environ["GOOGLE_CREDS_TYPE"]
    GOOGLE_CREDS_PROJECT_ID = os.environ["GOOGLE_CREDS_PROJECT_ID"]
    GOOGLE_CREDS_PRIVATE_KEY_ID = os.environ["GOOGLE_CREDS_PRIVATE_KEY_ID"]
    GOOGLE_CREDS_PRIVATE_KEY = os.environ["GOOGLE_CREDS_PRIVATE_KEY"]
    GOOGLE_CREDS_EMAIL = os.environ["GOOGLE_CREDS_EMAIL"]
    GOOGLE_CREDS_CLIENT_ID = os.environ["GOOGLE_CREDS_CLIENT_ID"]
    GOOGLE_CREDS_AUTH_URI = os.environ["GOOGLE_CREDS_AUTH_URI"]
    GOOGLE_CREDS_TOKEN_URI = os.environ["GOOGLE_CREDS_TOKEN_URI"]
    GOOGLE_CREDS_AUTH_PROVIDER = os.environ["GOOGLE_CREDS_AUTH_PROVIDER"]
    GOOGLE_CREDS_CLIENT = os.environ["GOOGLE_CREDS_CLIENT"]


google_credentials = {
    "type": GOOGLE_CREDS_TYPE,
    "project_id": GOOGLE_CREDS_PROJECT_ID,
    "private_key_id": GOOGLE_CREDS_PRIVATE_KEY_ID,
    "private_key": GOOGLE_CREDS_PRIVATE_KEY,
    "client_email": GOOGLE_CREDS_EMAIL,
    "client_id": GOOGLE_CREDS_CLIENT_ID,
    "auth_uri": GOOGLE_CREDS_AUTH_URI,
    "token_uri": GOOGLE_CREDS_TOKEN_URI,
    "auth_provider_x509_cert_url": GOOGLE_CREDS_AUTH_PROVIDER,
    "client_x509_cert_url": GOOGLE_CREDS_CLIENT,
}

with open("./google_client.json", "w") as f:
    dump(google_credentials, f, indent=4)
