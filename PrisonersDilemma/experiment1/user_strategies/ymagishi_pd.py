def yamagishi_pd(my_history, opponent_history):
    # TFT with a little more tolerance
    if len(opponent_history) < 2:
        return 0
    else:
        if opponent_history[-1]==1 or opponent_history[-2]==1:
            return 1
        else:
            return 0