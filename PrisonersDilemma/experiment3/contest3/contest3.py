#-*- encoding: utf-8 -*-
'''
Simulate finite repeated symmetric matrix game.
Copyright (c) 2015 @myuuuuun

Contest - imperfect private monitoring
'''
import sys
sys.path.append('../')
sys.path.append('../user_strategies')
import numpy as np
import pandas as pd
import play as pl

from Iida_imperfect_private import Iida_iprm
from kato import KatoStrategy
from ikegami_imperfect_private import Self_Centered_private
from mhanami_Imperfect_Private_Strategy import ImPrivStrategy
from tsuyoshi import GrimTrigger
from gistfile1 import MyStrategy
from beeleb_Strategy import beeleb
from oyama import OyamaImperfectPrivateMonitoring
from ogawa import ogawa
from yamagishi_impd import yamagishi
np.set_printoptions(precision=3)


if __name__ == '__main__':
    payoff = np.array([[4, 0], [5, 2]])
    seed = 282
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

    strategies = [Iida_iprm, ImPrivStrategy, KatoStrategy, Self_Centered_private, GrimTrigger, MyStrategy, beeleb, OyamaImperfectPrivateMonitoring, ogawa, yamagishi]
    game = pl.RepeatedMatrixGame(payoff, strategies, signal=private_signal, ts_length=ts_length, repeat=1000)
    game.play(mtype="private", random_seed=seed, record=True)



   
   