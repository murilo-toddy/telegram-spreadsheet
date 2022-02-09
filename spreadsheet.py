import gspread
from datetime import date
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
    Class used to communicate with Google spreadsheets

    Parameters
    ----------
    sheet_id - str: Identifier of google spreadsheet
    scope - list: Google Drive authorization scope
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

    def add_sheet(self, sheet_name: str, worksheet_id: int) -> None:
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


class SystemSpreadsheet(Spreadsheet):
    """
    Interface to handle spreadsheet manipulation related
    to a generic system

    Methods
    -------
    conclude_task: Updates task state to Concluído
    register_task: Adds new task to spreadsheet
    start_task: Updates task state to Fazendo
    """
    def __init__(self, sheet_id: str, scope: list, auth_file: str, debug: bool):
        super().__init__(sheet_id, scope, auth_file, debug)

    @staticmethod
    def conclude_task(user_data) -> None:
        pass

    @staticmethod
    def register_task(user_data) -> None:
        pass

    @staticmethod
    def start_task(user_data) -> None:
        pass


class ElectricSpreadsheet(SystemSpreadsheet):
    def __init__(self, sheet_id: str, scope: list, auth_file: str, debug: bool):
        super().__init__(sheet_id, scope, auth_file, debug)

    @staticmethod
    def conclude_task(user_data) -> None:
        sheet = user_data.ss.sheet(user_data.subsystem)
        index = user_data.index + 1

        sheet.update_acell(f"C{index}", "Concluído")
        sheet.update_acell(f"H{index}", user_data.difficulty)
        sheet.update_acell(f"I{index}", f"{user_data.row[8]}\n{user_data.comments}")

    # Returns project index in spreadsheet
    @staticmethod
    def __find_project_index(proj, data) -> int:
        for index, p in enumerate(data):
            if p[0] == proj:
                return index + 1
        return -1

    @staticmethod
    def register_task(user_data) -> None:
        ss: gspread.Worksheet = user_data.ss.sheet(user_data.subsystem)
        data = ss.get_all_values()

        if user_data.new_project:
            # Selects last spreadsheet row
            index = len(data) + 1
            ss.update_acell(f"A{index}", user_data.project)
        else:
            project_index = index = ElectricSpreadsheet.__find_project_index(user_data.project, data)
            # Finds last row related to project
            while not data[index][0]:
                index += 1
            index += 1
            ss.insert_row([], index=index)
            ss.merge_cells(f"A{project_index}:A{index}")

        # Adds related data to spreadsheet
        ss.update_acell(f"B{index}", user_data.task)
        ss.update_acell(f"C{index}", "A fazer")
        ss.update_acell(f"D{index}", date.today().strftime("%d/%m/%Y"))
        ss.update_acell(f"E{index}", user_data.duration)
        ss.update_acell(f"F{index}", user_data.difficulty)
        ss.update_acell(f"J{index}", user_data.documents)

    @staticmethod
    def start_task(user_data) -> None:
        ss: gspread.Worksheet = user_data.ss.sheet(user_data.subsystem)
        data = ss.get_all_values()
        for index, row in enumerate(data):
            if row[1] == user_data.task:
                break

        # Updates status and returns
        ss.update_acell(f"C{index+1}", "Fazendo")


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
