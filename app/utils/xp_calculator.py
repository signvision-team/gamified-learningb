def calculate_xp(is_correct, confidence):

    if not is_correct:
        return 0

    # base XP
    xp = 10

    # confidence bonus
    xp += int(confidence * 10)

    return xp