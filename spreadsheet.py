import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_AUTH_FILE = 'client_secret.json'
SHEET_NAME = "Planejamento Manufatura T-06 Prime"
SHEET_SCOPE = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
    ]

subsystems = {
    "bt": 1546038790,
    "pt": 1047261973,
    "hw": 0,
    "sw": 447316715
}

class Spreadsheet:
    def __init__(self, sheet_name: str, scope: list, auth_file: str, debug: bool):
        self.__debug = debug
        
        # Autenticação na Google API
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(auth_file, scope)
        self.client = gspread.authorize(self.creds)
        
        # Abertura da planilha
        self.ss = self.client.open(sheet_name)
        self.sheets = {}

        if self.__debug: print("[!] Connected do spreadsheet")

    # Cadastra uma nova aba da planilha com base no ID
    def add_sheet(self, sheet_name: str, sheet_id: str) -> None:
        self.sheets[sheet_name] = self.ss.get_worksheet_by_id(sheet_id)
        if self.__debug: print(f"[!!] Added sheet {sheet_name}")

    # Coleta todas as informações da planilha
    def sheet(self, sheet_name: str) -> gspread.worksheet.Worksheet:
        return self.sheets[sheet_name]


# Instancia a planilha
ss: Spreadsheet = Spreadsheet(SHEET_NAME, SHEET_SCOPE, SHEET_AUTH_FILE, True)
for subsystem, sheet_id in subsystems.items(): 
    ss.add_sheet(subsystem, sheet_id)
    




