import os
from json import dump

import psycopg2
from dotenv import load_dotenv

import database.connection as connection
from google.spreadsheet import SHEET_SCOPE, SHEET_AUTH_FILE, Spreadsheet, ElectricSpreadsheet
from utils import electric_subsystems, mechanics_subsystem

RELOAD_DATABASE = True

# File responsible for loading sensitive variables
if os.path.isfile("./.env"):
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")
    COMMANDS_SHEET_ID = os.getenv("COMMANDS_SHEET_ID")
    ELE_SHEET_ID = os.getenv("ELE_SHEET_ID")
    MEC_SHEET_ID = os.getenv("MEC_SHEET_ID")
    REPORT_CHAT_ID = os.getenv("BOT_REPORT_CHANNEL_ID")

else:
    TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    DATABASE_URL = os.environ["DATABASE_URL"]
    COMMANDS_SHEET_ID = os.environ["COMMANDS_SHEET_ID"]
    ELE_SHEET_ID = os.environ["ELE_SHEET_ID"]
    MEC_SHEET_ID = os.environ["MEC_SHEET_ID"]
    REPORT_CHAT_ID = os.environ["BOT_REPORT_CHANNEL_ID"]


if not os.path.isfile("./google_client.json"):
    if os.path.isfile("./.env"):
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
        GOOGLE_CREDS_TYPE = os.environ["GOOGLE_CREDS_TYPE"]
        GOOGLE_CREDS_PROJECT_ID = os.environ["GOOGLE_CREDS_PROJECT_ID"]
        GOOGLE_CREDS_PRIVATE_KEY_ID = os.environ["GOOGLE_CREDS_PRIVATE_KEY_ID"]
        GOOGLE_CREDS_PRIVATE_KEY = os.environ["GOOGLE_CREDS_PRIVATE_KEY"].replace("\\\\", "\\")
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
        print("\n  [!] Google config file created")


"""
Spreadsheet Connection
"""
# Commands spreadsheet
commands: Spreadsheet = Spreadsheet(COMMANDS_SHEET_ID, SHEET_SCOPE, SHEET_AUTH_FILE, True)
commands.add_sheet("cmd", 0)

# Electric Spreadsheet
electric_ss: ElectricSpreadsheet = ElectricSpreadsheet(ELE_SHEET_ID, SHEET_SCOPE, SHEET_AUTH_FILE, True)
for subsystem, info in electric_subsystems.items():
    electric_ss.add_sheet(subsystem, info["worksheet_id"])

# Mec Spreadsheet
# TODO determine how mechanics spreadsheet is going to work
mechanics_ss: Spreadsheet = Spreadsheet(MEC_SHEET_ID, SHEET_SCOPE, SHEET_AUTH_FILE, True)
# for subsystem, info in mechanics_subsystem.items():
#     mechanics_ss.add_sheet(subsystem, info["worksheet_id"])

# All systems and their relevant information
systems = {
    "ele": {"ss": electric_ss, "sub": electric_subsystems},
    "mec": {"ss": mechanics_ss, "sub": mechanics_subsystem},
}

"""
Database connection
"""
con = connection.Connection(debug=True)
database_configuration = open("database/default_configuration.sql").read()
if RELOAD_DATABASE:
    con.exec_and_commit("DROP SCHEMA public CASCADE;")
    con.exec_and_commit("CREATE SCHEMA public;")
try:
    con.exec_and_commit(database_configuration)
    print("  [!!] Default configuration loaded")
except psycopg2.Error:
    pass
