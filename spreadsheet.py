import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

    def add_sheet(self, sheet_name: str, sheet_id: str) -> None:
        self.sheets[sheet_name] = self.ss.get_worksheet_by_id(sheet_id)
        if self.__debug: print(f"[!!] Added sheet {sheet_name}")

    def sheet(self, sheet_name: str) -> gspread.worksheet.Worksheet:
        return self.sheets[sheet_name]



    




