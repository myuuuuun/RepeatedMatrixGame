def tit_for_tat(my_history, opponent_history):
    if len(opponent_history) < 1:
        return 0
    else:
        return opponent_history[-1]