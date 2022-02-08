from spreadsheet import Spreadsheet

# A class containing all information that may be needed in a certain conversation
class Conversation:
    def __init__(self):
        # Related data
        self.ss: Spreadsheet
        self.dict: dict
        self.index: int
        self.row: int

        # Checks
        self.new_project: bool
        self.projects: str
        self.tasks: str

        # Task information
        self.system: str
        self.subsystem: str
        self.project: str
        self.task: str
        self.difficulty: str
        self.duration: str
        self.comments: str
        self.documents: str
