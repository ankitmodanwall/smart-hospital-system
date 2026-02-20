def sort_queue(patients):
    return sorted(patients, key=lambda x: x[6])


def calculate_wait(position, total_doctors):
    if total_doctors == 0:
        return "No doctors available"
    return (position // total_doctors) * 15