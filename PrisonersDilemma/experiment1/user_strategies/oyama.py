def oyama(my_history, opponent_history):
    try:
        my_prev_action = my_history[-1]
        opponent_prev_action = opponent_history[-1]
    except IndexError:  # Empty history
        return 0
    if my_prev_action == 1 or opponent_history == 1:
        return 1
    return 0
