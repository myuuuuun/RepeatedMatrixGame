#-*- encoding: utf-8 -*-
'''
Simulate finite repeated symmetric matrix game.
Copyright (c) 2015 @myuuuuun

Contest - imperfect public monitoring
'''
import sys
sys.path.append('../')
sys.path.append('../user_strategies')
import numpy as np
import pandas as pd
import play as pl

from Iida_imperfect_public import Iida_ipm
from kato import KatoStrategy
from ikegami_imperfect_public import Self_Centered_public
from mhanami_Imperfect_Public_Strategy import ImPubStrategy
from tsuyoshi import GrimTrigger
from gistfile1 import MyStrategy
from beeleb_Strategy import beeleb
from oyama import OyamaImperfectPublicMonitoring
from ogawa import ogawa
from yamagishi_impd import yamagishi
np.set_printoptions(precision=3)


if __name__ == '__main__':
    payoff = np.array([[4, 0], [5, 2]])
    seed = 282
    
    # 第1期は確率1で来るものとする
    discount_v = 0.97
    ts_length = np.random.RandomState(seed).geometric(p=1-discount_v, size=1000)

    # プロジェクトが成功か失敗かを返す
    def public_signal(actions, random_state):
        prob = random_state.uniform()
        if actions[0] == 0 and actions[1] == 0:
            return 0 if prob < 0.9 else 1
        elif (actions[0] == 0 and actions[1] == 1) or (actions[0] == 1 and actions[1] == 0):
            return 0 if prob < 0.5 else 1
        elif actions[0] == 1 and actions[1] == 1:
            return 0 if prob < 0.2 else 1
        else:
            raise ValueError

    strategies = [Iida_ipm, ImPubStrategy, KatoStrategy, Self_Centered_public, GrimTrigger, MyStrategy, beeleb, OyamaImperfectPublicMonitoring, ogawa, yamagishi]
    game = pl.RepeatedMatrixGame(payoff, strategies, signal=public_signal, ts_length=ts_length, repeat=1000)
    game.play(mtype="public", random_seed=seed, record=True)



   