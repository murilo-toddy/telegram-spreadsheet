import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import COMMANDS_SHEET_ID, ELE_SHEET_ID, MEC_SHEET_ID
from utils import electric_subsystems, mechanics_subsystem

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
            print("\n  [!] Connected to spreadsheet")

    def add_sheet(self, sheet_name: str, worksheet_id: str) -> None:
        """
        Registers new sheet based on its ID

        Parameters
        ----------
        sheet_name - str: Identifier that will be used to access worksheet
        worksheet_id - str: Identifier of worksheet
        """
        self.sheets[sheet_name] = self.ss.get_worksheet_by_id(worksheet_id)
        if self.__debug:
            print(f"  [!!] Added sheet {sheet_name}")

    def sheet(self, sheet_name: str) -> gspread.worksheet.Worksheet:
        """
        Returns a specific worksheet

        Parameters
        ----------
        sheet_name - str: Identifier of registered sheet
        """
        return self.sheets[sheet_name]


# Commands spreadsheet
commands: Spreadsheet = Spreadsheet(COMMANDS_SHEET_ID, SHEET_SCOPE, SHEET_AUTH_FILE, True)
commands.add_sheet("cmd", 0)

# Electric Spreadsheet
electric_ss: Spreadsheet = Spreadsheet(ELE_SHEET_ID, SHEET_SCOPE, SHEET_AUTH_FILE, True)
for subsystem, info in electric_subsystems.items():
    electric_ss.add_sheet(subsystem, info["worksheet_id"])

# Mec Spreadsheet
mechanics_ss: Spreadsheet = Spreadsheet(MEC_SHEET_ID, SHEET_SCOPE, SHEET_AUTH_FILE, True)
for subsystem, info in mechanics_subsystem.items():
    mechanics_ss.add_sheet(subsystem, info["worksheet_id"])

# All systems and their relevant information
systems = {
    "ele": {"ss": electric_ss, "sub": electric_subsystems},
    "mec": {"ss": mechanics_ss, "sub": mechanics_subsystem},
}
