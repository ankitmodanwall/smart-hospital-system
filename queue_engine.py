from datetime import datetime

def sort_queue(patients):
    return sorted(
        patients,
        key=lambda x: (x[6], datetime.fromisoformat(x[8]))
    )

def calculate_wait(index, doctor_count):
    return (index // doctor_count) * 10
