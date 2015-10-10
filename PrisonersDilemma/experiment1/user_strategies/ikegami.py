import random

def ikegami(my_list, opponent_list):
    a = random.random()
    if a <= 0.0001:
        while len(my_list) < 100000:
            return 1

    else:
        if len(my_list) == 0:
            return 0

        else:
            return opponent_list[-1]