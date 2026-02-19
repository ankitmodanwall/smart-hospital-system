def grok_triage(symptoms,age,location):
    text=symptoms.lower()

    if "chest" in text or "breath" in text:
        return 1,"Emergency (Priority 1)"

    if "fever" in text or "vomit" in text:
        return 2,"Urgent (Priority 2)"

    if age>65:
        return 2,"Urgent (Priority 2)"

    return 3,"Routine (Priority 3)"
