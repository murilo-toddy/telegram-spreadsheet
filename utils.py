from spreadsheet import ele_ss, mec_ss

# All subsystems separated by respective systems
electric_subsystems = {
    "bat": {"name": "Baterias",   "sheet_id": 447316715},
    "pt":  {"name": "Powertrain", "sheet_id": 1129194817},
    "hw":  {"name": "Hardware",   "sheet_id": 1556464449},
    "sw":  {"name": "Software",   "sheet_id": 367184788},
}
mechanics_subsystem = {
    "ch":    {"name": "Chassi",       "sheet_id": 447316715},
    "tr":    {"name": "Transmissão",  "sheet_id": 447316715},
    "aero":  {"name": "Aerodinâmica", "sheet_id": 447316715},
    "susp":  {"name": "Suspensão",    "sheet_id": 447316715},
    "freio": {"name": "Freio",        "sheet_id": 447316715},
}

# All systems and their relevant information
systems = {
    "ele": {"ss": ele_ss, "sub": electric_subsystems}, 
    "mec": {"ss": mec_ss, "sub": mechanics_subsystem},
}
