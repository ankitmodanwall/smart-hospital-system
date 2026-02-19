def check_ambulance(patient):
    if patient[4] == "Rural" and patient[6] == 1:
        return True
    return False
