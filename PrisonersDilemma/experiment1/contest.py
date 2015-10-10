#-*- encoding: utf-8 -*-
'''
Simulate finite repeated symmetric matrix game.
Copyright (c) 2015 @myuuuuun

Released under the MIT license.
'''

from __future__ import division, print_function
import sys
import math
import functools #for python3
import numpy as np
import sys
from sample import *
import play as pl

sys.path.append('./user_strategies')
import ikegami
import tsuyoshi
import bocchan
import oyama
import ymagishi_pd
import ogawa_prison
import beelab
import kato
import oyataku

np.set_printoptions(precision=3)


if __name__ == '__main__':
    payoff = np.array([[2, 0], [3, 1]])
    seed = 1005
    discount_v = 0.9999
    playtimes = np.random.RandomState(seed).geometric(p=1-discount_v)

    strategies = [ikegami.ikegami, tsuyoshi.allD, bocchan.Iida_tit, oyama.oyama, ymagishi_pd.yamagishi_pd, ogawa_prison.ogaway, beelab.ohno, kato.tit_for_tat, oyataku.random_strategy]
    game = pl.RepeatedMatrixGame(payoff, strategies, playtimes)
    game.play()




   