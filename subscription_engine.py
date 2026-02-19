def check_subscription(user_data):
    free = user_data[4]
    active = user_data[5]

    if free > 0:
        return "FREE"
    elif active == 1:
        return "SUBSCRIBED"
    else:
        return "BLOCKED"
