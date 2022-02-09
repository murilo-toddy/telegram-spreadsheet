from spreadsheet import SystemSpreadsheet


# A class containing all information that may be needed in a certain conversation
class Conversation:
    def __init__(self):
        # Related data
        self.ss: SystemSpreadsheet
        self.dict: dict = {}
        self.index: int = -1
        self.row: list = []

        # Checks
        self.new_project: bool = True
        self.projects: str = ""
        self.tasks: str = ""

        # Task information
        self.system: str = ""
        self.subsystem: str = ""
        self.project: str = ""
        self.task: str = ""
        self.difficulty: str = ""
        self.duration: str = ""
        self.comments: str = ""
        self.documents: str = ""
