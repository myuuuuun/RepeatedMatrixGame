#-*- encoding: utf-8 -*-
'''
Simulate finite repeated symmetric matrix game.
Copyright (c) 2015 @myuuuuun

Released under the MIT license.
'''

from __future__ import division, print_function
import math
import functools #for python3
import numpy as np
import pandas as pd
from numpy.random import geometric
from sample import AllC, AllD, MyStrategy, GrimTrigger, Alternate, RandomStrategy
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
from datetime import datetime
import numba
np.set_printoptions(precision=3)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 200)


# type and size checking of payoff
def is_valid_payoff(payoff):
    msg1 = "payoff must be square matrix(array_like, ndim=2)."
    msg2 = ("payoff must be square matrix(array_like, ndim=2)"
            " and each element of it must be integer or float.")
    
    if isinstance(payoff, list):
        row = len(payoff)
        for x in payoff:
            if not isinstance(x, list):
                raise TypeError(msg1)

            if len(x) != row:
                raise TypeError(msg1)
                
            for y in x:
                if not isinstance(y, (float, int)):
                    raise TypeError(msg2)
        
    elif isinstance(payoff, np.ndarray):
        if payoff.ndim != 2:
            raise TypeError(msg1)

        row, col = payoff.shape
        if row != col:
            raise TypeError(msg1)

        if not np.issubdtype(payoff.dtype, (int, float)):
            raise TypeError(msg2)

    return payoff, row


# type checking of strategies
def is_valid_strategies(strategies):
    msg = ("Argument \"strategies\" must be function or "
           "list(ndim=1) of functions.")

    if hasattr(strategies, '__call__'):
        strategies = [strategies]

    elif isinstance(strategies, list) and len(strategies) >= 1:
        for s in strategies:
            if not hasattr(s, '__call__'):
                raise TypeError(msg)

    else:
        raise TypeError(msg)

    return strategies


# type checking of ts_length
def is_valid_ts_length(ts_length, random_state=None):
    msg = ("ts_length must be None, or int or list of ints"
            "that satisfy 0 <= ts_length or ts_length = -1")

    if random_state is None:
        random_state = np.random.RandomState()

    if ts_length is None:
        ts_length = np.random.RandomState().randint(1000, 10001)

    elif np.isscalar(ts_length):
        ts_length = np.array([ts_length], dtype=np.int64)

    else:
        try:
            ts_length = np.asarray(ts_length, dtype=np.int64)

        except:
            raise TypeError(msg)
    
    if np.any(ts_length < -1):
        raise ValueError(msg)

    index = np.where(ts_length == -1)
    ts_length[index] = random_state.randint(1000, 10001, size=len(index[0]))
    
    return ts_length



class RepeatedMatrixGame(object):
    '''
    Class for simulating finite repeated symmetric matrix game.

    Arguments
    ---------
    payoff: array_like(int or float, ndim=2)
        Payoff matrix(2 dim array) of row player. The matrix must be square.

    strategies: list(function, ndim=1)
        List of strategy functions. List length must be more than 1.
        Each function needs to follow the format below.

        Arguments
            my_history: array(int, ndim=1)
                History of my actions before the period. "my_history[i]" refers
                to my past action of the i-th period. If it is 3rd period now,
                given ["my action of 1st period(int)", "of 2nd period(int)"].
                When 1st period, given empty list.

            opponent_history: array(int, ndim=1)
                History of opponent actions before the period.
                The format is same as of "my_history".

        Returns
            action: int
                My action of this period. It must be "0<=action<len(payoff)".

        To check whether each function is valid, use the method ".check()".

    ts_length: int(optional) or array_like(int, ndim=1), default=None
        Number of repetition of games.
        If None or -1, pick random number from 1000 to 10000.
    '''
    def __init__(self, payoff, strategies, signal_dist, ts_length=None, repeat=1, **kwargs):
        # kwargs: discount factor, is_play_with_myself...

        # type and size checking of payoff
        self.payoff, self.actlen = is_valid_payoff(payoff)

        # type checking of strategies
        self.strategies =  is_valid_strategies(strategies)

        # type checking of ts_length
        self.ts_length = is_valid_ts_length(ts_length)

        self.repeat = repeat

        self.signal = signal_dist
            
    def set_payoff(self, payoff):
        self.payoff, self.actlen = is_valid_payoff(payoff)

    def set_strategies(self, strategies):
        self.strategies = is_valid_strategies(strategies)

    def add_strategies(self, strategies):
        self.strategies = self.strategies + is_valid_strategies(strategies)

    def show_strategies(self):
        print("The object has {0} strategy functions below".format(len(self.strategies)))
        print("*"*40)
        for f in self.strategies:
            print(f.__name__)

        print("*"*40)

    def remove_strategies(self, str_name):
        for f in self.strategies:
            if f.__name__ == str_name:
                self.strategies.remove(f)

    def set_ts_length(self, ts_length):
        self.ts_length = is_valid_ts_length(ts_length)

    def set_signal(self, signal_dist):
        self.signal = signal_dist


    @numba.jit
    def __play__(self, strategy1, strategy2, mtype, round_ts_length, random_state, record):
        # インスタンス化
        Strategy1 = strategy1(random_state)
        Strategy2 = strategy2(random_state)
        score1 = 0
        score2 = 0
        
        for i in range(round_ts_length):
            # Stage gameをプレイ
            action1 = Strategy1.play()
            action2 = Strategy2.play()

            # 利得を追加
            stage_score1 = self.payoff[action1][action2]
            stage_score2 = self.payoff[action2][action1]

            score1 += stage_score1
            score2 += stage_score2

            # シグナルを作成
            if mtype == "perfect":
                signal1 = action2
                signal2 = action1

            elif mtype == "public":
                signal = self.signal([action1, action2])
                signal1 = signal
                signal2 = signal

            elif mtype == "private":
                signals = self.signal([action1, action2])
                signal1 = signals[0]
                signal2 = signals[1]

            else:
                raise ValueError

            # シグナルを渡す
            Strategy1.get_signal(signal1)
            Strategy2.get_signal(signal2)

            if record:
                self.match_result[self.stage_count][0] = i
                self.match_result[self.stage_count][1] = action1
                self.match_result[self.stage_count][2] = action2
                self.match_result[self.stage_count][3] = signal1
                self.match_result[self.stage_count][4] = signal2
                self.match_result[self.stage_count][5] = stage_score1
                self.match_result[self.stage_count][6] = stage_score2

            self.stage_count += 1

        return score1, score2

    
    def play(self, mtype="perfect", random_seed=None, record=False, plot=False):
        if random_seed is None:
            random_state = np.random.RandomState()
            random_seed = np.nan

        else:
            random_state = np.random.RandomState(random_seed)

        # Monitoring type
        if not mtype in ["perfect", "public", "private"]:
            msg = "mtype must be \'perfect\', \'public\' or \'private\'"
            raise ValueError(msg)

        # Number of strategy classes
        strlen = len(self.strategies)
        if strlen < 2:
            msg = "To play, need at least 2 strategies."
            raise TypeError(msg)

        # Number of matches
        matches = strlen * (strlen-1) // 2

        # Score table
        result = np.zeros((strlen, strlen))

        # List of time series for all rounds
        ts_list = np.empty(self.repeat, dtype=np.int64)
        for r in range(self.repeat):
            ts_list[r] = self.ts_length[r % len(self.ts_length)]

        # Total time series of all rounds (of 1 match)
        total_ts = np.sum(ts_list)

        if record:
            self.match_result = np.empty((total_ts, 7), dtype=int)
            # Number of rows in record DataFrame (=total stages)
            row = total_ts * matches
            str_names = [s.__name__ for s in self.strategies]
            round_list = np.empty(total_ts, dtype=int)
            count_row = 0
            for r, ts in enumerate(ts_list):
                round_list[count_row:count_row+ts] = r
                count_row += ts

            self.record_df = pd.DataFrame({
                'Mtype'  : pd.Categorical([mtype] * row, categories=["perfect", "public", "private"]),
                'RandomSeed': np.array([random_seed] * row),
                'Strategy1': pd.Categorical(np.empty(row), categories=str_names),
                'Strategy2': pd.Categorical(np.empty(row), categories=str_names),
                'Round'  : np.empty(row, dtype=int),
                'Period' : np.empty(row, dtype=int),
                'Action1': np.empty(row),
                'Action2': np.empty(row),
                'Signal1': np.empty(row),
                'Signal2': np.empty(row),
                'Payoff1': np.empty(row),
                'Payoff2': np.empty(row),
                }, columns=['Mtype', 'RandomSeed', 'Strategy1', 'Strategy2', 'Round',
                'Period', 'Action1', 'Action2', 'Signal1', 'Signal2', 'Payoff1', 'Payoff2'])

            for i in range(matches):
                self.record_df.loc[i*total_ts : (i+1)*total_ts-1, "Round"] = round_list

        # 現在何組目の対戦か
        match_count = 1

        start = time.time()
        print("Start")
        self.show_strategies()
        print("Time series length: {0}".format(self.ts_length))
        print("Repeats: {0}".format(self.repeat))
        print("Total time series length: {0}".format(total_ts))
        
        for i, str1 in enumerate(self.strategies):
            for j, str2 in enumerate(self.strategies[i+1:]):
                if record:
                    count_ts = 0
                    self.record_df['Strategy1'][(match_count-1) * total_ts : match_count * total_ts] = str1.__name__
                    self.record_df['Strategy2'][(match_count-1) * total_ts : match_count * total_ts] = str2.__name__

                score1, score2 = 0, 0
                self.stage_count = 0

                for r in range(self.repeat):
                    round_ts_length = ts_list[r]

                    s1, s2 = self.__play__(str1, str2, mtype, round_ts_length, random_state, record)
                    score1 += s1
                    score2 += s2
                    count_ts += round_ts_length

                if record:
                    self.record_df.loc[(match_count-1)*total_ts : match_count*total_ts-1, 'Period':'Payoff2'] = self.match_result[0:total_ts, 0:7]
                
                print("-"*60)
                print("Game {0}: \"{1}\" vs \"{2}\"".format(match_count, str1.__name__, str2.__name__))
                print("total score of {0}: {1:.3f}, per stage: {2:.3f}".format(str1.__name__, score1, score1/total_ts))
                print("total score of {0}: {1:.3f}, per stage: {2:.3f}".format(str2.__name__, score2, score2/total_ts))
                result[i][i+j+1] = score1
                result[i+j+1][i] = score2
                match_count += 1
        

        print("-"*60)
        elapsed_time = time.time() - start
        print ("elapsed_time:{0}".format(elapsed_time))


        print("Score table:")
        print(result)

        print("\nRanking:")

        total = np.zeros(strlen, dtype=float)
        for i in range(strlen):
            total[i] = np.sum(result[i])
        
        ranking = np.argsort(total)[::-1]
        for i in range(strlen):
            s = ranking[i]
            print("{0}. \"{1}\"".format(i+1, self.strategies[s].__name__))
            print("total points: {0:.3f}, average points per opponent: {1:.3f}, average points per stage: {2:.3f}"
                .format( total[s], total[s]/(strlen-1), total[s]/((strlen-1)*total_ts) ))

        current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.record_df.to_csv("record_" + str(current_time) + ".csv")
        print(self.record_df)


    def plot(self, history1=None, history2=None, signals=None):
        ts_length = len(history1)

        ax1 = plt.subplot(2, 1, 1)
        plt.plot(history1, range(ts_length), 'o', color='c')

        plt.subplot(2, 1, 2, sharex=ax1, sharey=ax1)
        plt.plot(history2, range(ts_length), 'o', color='c')

        plt.xlim(-1, 2)
        plt.ylim(-1, 101)
        plt.show()
 

if __name__ == '__main__':
    payoff = np.array([[4, 0], [5, 2]])
    seed = 11451
    rs = np.random.RandomState(seed)
    discount_v = 0.97
    repeat = 1000
    # 第1期は確率1で来るものとする
    ts_length = rs.geometric(p=1-discount_v, size=1000) + 1


    # プロジェクトが成功か失敗かを返す
    def public_signal_dist(actions):
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
    def private_signal_dist(actions):
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

    strategies = [AllC, AllD, MyStrategy, GrimTrigger, Alternate, RandomStrategy]
    game = RepeatedMatrixGame(payoff, strategies, private_signal_dist, ts_length, repeat)
    game.play("private", seed, True)
    #game.plot()


