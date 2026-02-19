from datetime import datetime

def sort_queue(patients):
    return sorted(patients,key=lambda x:(x[6],datetime.fromisoformat(x[9])))

def calculate_wait(patients,available_doctors):
    consultation_time=10
    result=[]
    for i,p in enumerate(patients):
        batch=i//available_doctors
        wait=batch*consultation_time
        result.append({
            "UID":p[1],
            "Name":p[2],
            "Priority":p[6],
            "Wait (mins)":wait,
            "Location":p[4]
        })
    return result
