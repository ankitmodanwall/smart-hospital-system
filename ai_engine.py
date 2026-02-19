def sort_queue(patients):
    """
    Safe sorting:
    Sort by priority only.
    Lower number = higher priority.
    """
    try:
        return sorted(patients, key=lambda x: x[6])
    except:
        return patients


def calculate_wait(position, total_doctors):
    if total_doctors == 0:
        return "No doctors available"

    return (position // total_doctors) * 15
