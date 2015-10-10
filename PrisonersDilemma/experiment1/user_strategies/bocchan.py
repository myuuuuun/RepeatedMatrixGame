def Iida_tit(my_history, opponent_history):
    if len(opponent_history) < 1:
        return 0

    return opponent_history[-1]