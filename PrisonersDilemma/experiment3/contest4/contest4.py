#-*- encoding: utf-8 -*-
'''
Simulate finite repeated symmetric matrix game.
Copyright (c) 2015 @myuuuuun

Contest - imperfect private monitoring2
'''
import sys
sys.path.append('../')
sys.path.append('../user_strategies')
import numpy as np
import pandas as pd
import play as pl

from kandori import *
np.set_printoptions(precision=3)


if __name__ == '__main__':
    payoff = np.array([[4, 0], [5, 2]])
    seed = 2822
    rs = np.random.RandomState(seed)
    
    # 第1期は確率1で来るものとする
    discount_v = 0.97
    ts_length = rs.geometric(p=1-discount_v, size=1000)

    # 「相手の」シグナルが協調か攻撃かを（ノイズ付きで）返す
    def private_signal(actions, random_state):
        pattern = [[0, 0], [0, 1], [1, 0], [1, 1]]
        # 例えば実際の行動が(0, 1)なら、シグナルは(1, 0)である可能性が最も高い
        signal_probs = [[.9, .02, .02, .06], [.02, .06, .9, .02], [.02, .9, .06, .02], [.06, .02, .02, .9]]
        p = random_state.uniform()
        if actions[0] == 0 and actions[1] == 0:
            return [0, 0] if p < 0.9 else [0, 1] if p < 0.92 else [1, 0] if p < 0.94 else [1, 1]
        elif actions[0] == 0 and actions[1] == 1:
            return [1, 0] if p < 0.9 else [0, 0] if p < 0.92 else [1, 1] if p < 0.94 else [0, 1]
        elif actions[0] == 1 and actions[1] == 0:
            return [0, 1] if p < 0.9 else [1, 1] if p < 0.92 else [0, 0] if p < 0.94 else [1, 0]
        elif actions[0] == 1 and actions[1] == 1:
            return [1, 1] if p < 0.9 else [1, 0] if p < 0.92 else [0, 1] if p < 0.94 else [0, 0]
        else:
            raise ValueError

    strategies = [Strategy1, Strategy2, Strategy3, Strategy4, Strategy5,
                    Strategy6, Strategy7, Strategy8, Strategy9, Strategy10,
                    Strategy11, Strategy12, Strategy13, Strategy14, Strategy15,
                    Strategy16, Strategy17, Strategy18, Strategy19, Strategy20, 
                    Strategy21, Strategy22, Strategy23, Strategy24]
    
    game = pl.RepeatedMatrixGame(payoff, strategies, signal=private_signal, ts_length=ts_length, repeat=1000)
    game.play(mtype="private", random_seed=seed, record=True)



   
   