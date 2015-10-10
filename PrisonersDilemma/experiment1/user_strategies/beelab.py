def ohno(my_history, opponent_history):
    if len(my_history) < 100:
        return 0
    else:
        my_latest = sum(my_history[-10:])
        opponent_latest = sum(opponent_history[-10:])

        if opponent_latest >= 9:
            return 1
        elif my_latest >= 4 or opponent_latest <= 3:
            return 0
        else:
            return 1