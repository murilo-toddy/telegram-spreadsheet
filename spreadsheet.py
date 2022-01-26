import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils import ele_subsystems, mec_subsystems
from config import COMMANDS_SHEET_ID, ELE_SHEET_ID, MEC_SHEET_ID

SHEET_AUTH_FILE = "client_secret.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1kHx2-Q3H_m3pqm7YHDmMD8SzOJMxPIIw5cwB7vVlMi0/edit#gid=1546038790"
SHEET_SCOPE = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
]


class Spreadsheet:
    """
    Class used to comunicate with google spreadsheets

    Parameters
    ----------
    sheet_id - str: Identifier of google spreadsheet
    scope - list: Google drive authorization scope
    auth_file - str: Name of authentication file
    debug - bool: Enables debug mode

    Attributes
    ----------
    ss - gspread.Spreadsheet: Google spreadsheet
    sheets - {str: gspread.Worksheet}: Dictionary containing
    """

    def __init__(self, sheet_id: str, scope: list, auth_file: str, debug: bool):
        self.__debug = debug

        # Authenticates in GoogleAPI
        creds = ServiceAccountCredentials.from_json_keyfile_name(auth_file, scope)
        self.client = gspread.authorize(creds)

        # Opens spreadsheet
        self.ss = self.client.open_by_key(sheet_id)
        self.sheets = {}

        if self.__debug:
            print("[!] Connected to spreadsheet")

    """
    Registers new sheet based on its ID

    Parameters
    ----------
    sheet_name - str: Identifier that will be used to access worksheet
    worksheet_id - str: Identifier of worksheet
    """

    def add_sheet(self, sheet_name: str, worksheet_id: str) -> None:
        self.sheets[sheet_name] = self.ss.get_worksheet_by_id(worksheet_id)
        if self.__debug:
            print(f"[!!] Added sheet {sheet_name}")

    """
    Returns a specific worksheet
    
    Parameters
    ----------
    sheet_name - str: Identifier of registered sheet
    """

    def sheet(self, sheet_name: str) -> gspread.worksheet.Worksheet:
        return self.sheets[sheet_name]


# Commands spreadsheet
commands: Spreadsheet = Spreadsheet(COMMANDS_SHEET_ID, SHEET_SCOPE, SHEET_AUTH_FILE, True)
commands.add_sheet("cmd", 0)

# Ele Spreadsheet
ele_ss: Spreadsheet = Spreadsheet(ELE_SHEET_ID, SHEET_SCOPE, SHEET_AUTH_FILE, True)
for subsystem, info in ele_subsystems.items():
    ele_ss.add_sheet(subsystem, info["sheet_id"])

# Mec Spreadsheet
mec_ss: Spreadsheet = Spreadsheet(MEC_SHEET_ID, SHEET_SCOPE, SHEET_AUTH_FILE, True)
for subsystem, info in mec_subsystems.items():
    mec_ss.add_sheet(subsystem, info["sheet_id"])
