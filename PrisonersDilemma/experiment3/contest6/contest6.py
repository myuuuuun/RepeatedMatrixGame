#-*- encoding: utf-8 -*-
'''
Simulate finite repeated symmetric matrix game.
Copyright (c) 2015 @myuuuuun

Contest - imperfect private monitoring3
'''
import sys
sys.path.append('../')
import numpy as np
import pandas as pd
import play as pl
np.set_printoptions(precision=3)


class TFT(object):
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.signal = 0

    def play(self):
        return self.signal

    def get_signal(self, signal):
        self.signal = signal


class WSLS(object):
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.my_action = 0
        self.signal = 0

    def play(self):
        if self.signal == 1:
            self.my_action = 1 - self.my_action
            return self.my_action
        else:
            return self.my_action

    def get_signal(self, signal):
        self.signal = signal


class ALLD(object):
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state

    def play(self):
        return 1

    def get_signal(self, signal):
        pass

class Prob:
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.my_history = []
        self.signals = []
        self.count = 0
        self.count_rate = 0
        
    def play(self):
        if self.count_rate >= 0.1:
            return 1
        else:
            return 0
    
    def countf(self):
        if self.signals[-1] == 1:
            self.count += 1
        self.count_rate = self.count / len(self.signals)
        
    def get_signal(self, signal):
        self.signals.append(signal)
        self.countf()


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

    strategies = [TFT, TFT, TFT, TFT, TFT, TFT, TFT, TFT, TFT, TFT, TFT, WSLS, WSLS, WSLS, WSLS, WSLS, WSLS, WSLS, WSLS, WSLS, ALLD, ALLD, ALLD, ALLD, ALLD]

    game = pl.RepeatedMatrixGame(payoff, strategies, signal=private_signal, ts_length=ts_length, repeat=1000)
    game.play(mtype="private", random_seed=seed, record=False)



   
   