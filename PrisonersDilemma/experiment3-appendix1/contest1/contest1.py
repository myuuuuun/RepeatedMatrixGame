#-*- encoding: utf-8 -*-
'''
Simulate finite repeated symmetric matrix game.
Copyright (c) 2015 @myuuuuun

Contest - perfect monitoring
'''
import sys
sys.path.append('../')
sys.path.append('../user_strategies')
import numpy as np
import pandas as pd
import play as pl

from Iida_perfect_monitoring import Iida_pm
from kato import KatoStrategy
from ikegami_perfect import Self_Centered_perfect
from mhanami_Public_Strategy import PubStrategy
from tsuyoshi import GrimTrigger
from gistfile1 import MyStrategy
from beeleb_Strategy import beeleb
from oyama import OyamaPerfectMonitoring
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

    strategies = [Iida_pm, PubStrategy, KatoStrategy, Self_Centered_perfect, GrimTrigger, MyStrategy, beeleb, OyamaPerfectMonitoring, ogawa, yamagishi]
    game = pl.RepeatedMatrixGame(payoff, strategies, ts_length=ts_length, repeat=1000)
    game.play(mtype="perfect", random_seed=seed, record=True)



   