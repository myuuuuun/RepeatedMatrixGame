#-*- encoding: utf-8 -*-
'''
Simulate finite repeated symmetric matrix game.
Copyright (c) 2015 @myuuuuun

Released under the MIT license.
'''
import math
import numpy as np
import sys
sys.path.append('./user_strategies')
import play as pl
from sample import AllC, AllD, MyStrategy, GrimTrigger, Alternate, RandomStrategy
from Iida_perfect_monitoring import Iida_pm
from Iida_imperfect_public import Iida_ipm
from Iida_imperfect_private import Iida_iprm
from kato import KatoStrategy

np.set_printoptions(precision=3)



if __name__ == '__main__':
    payoff = np.array([[4, 0], [5, 2]])
    seed = 11451
    rs = np.random.RandomState(seed)
    
    # 第1期は確率1で来るものとする
    discount_v = 0.97
    ts_length = rs.geometric(p=1-discount_v, size=1000) + 1

    # プロジェクトが成功か失敗かを返す
    def public_signal(actions):
        prob = rs.uniform()
        if actions[0] == 0 and actions[1] == 0:
            return 0 if prob < 0.9 else 1

        elif (actions[0] == 0 and actions[1] == 1) or (actions[0] == 1 and actions[1] == 0):
            return 0 if prob < 0.5 else 1

        elif actions[0] == 1 and actions[1] == 1:
            return 0 if prob < 0.2 else 1

        else:
            raise ValueError

    # 「相手の」シグナルが協調か攻撃かを（ノイズ付きで）返す
    def private_signal(actions):
        pattern = [[0, 0], [0, 1], [1, 0], [1, 1]]
        # 例えば実際の行動が(0, 1)なら、シグナルは(1, 0)である可能性が最も高い
        signal_probs = [[.9, .02, .02, .06], [.02, .06, .9, .02], [.02, .9, .06, .02], [.06, .02, .02, .9]]
        prob = rs.uniform()
        if actions[0] == 0 and actions[1] == 0:
            choice = rs.choice(4, p=signal_probs[0])
            return pattern[choice]

        elif actions[0] == 0 and actions[1] == 1:
            choice = rs.choice(4, p=signal_probs[1])
            return pattern[choice]

        elif actions[0] == 1 and actions[1] == 0:
            choice = rs.choice(4, p=signal_probs[2])
            return pattern[choice]

        elif actions[0] == 1 and actions[1] == 1:
            choice = rs.choice(4, p=signal_probs[3])
            return pattern[choice]

        else:
            raise ValueError

    strategies = [AllC, AllD, MyStrategy, GrimTrigger]
    game = pl.RepeatedMatrixGame(payoff, strategies, signal=private_signal, ts_length=ts_length, repeat=1000)
    game.play(mtype="private", random_seed=seed, record=True)



   