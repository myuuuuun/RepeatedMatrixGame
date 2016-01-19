#-*- encoding: utf-8 -*-
'''
Play Function for Experiment3-Appendix1.
Copyright (c) 2015 @myuuuuun

Released under the MIT license.
'''

# for python2
from __future__ import division, print_function
import sys
sys.path.append('./user_strategies')
import os
from datetime import datetime
import numpy as np
import pandas as pd
import itertools
import matplotlib.pyplot as plt
from Iida_imperfect_private import Iida_iprm
from kato import KatoStrategy
from sample import AllC
np.set_printoptions(precision=3)
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 400)


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

    return payoff


# type checking of strategies
def is_valid_strategies(strategies):
    msg = ("Argument \"strategies\" must be class or "
           "list(ndim=1) of classes that has 2 methods"
           "play() and get_signal()")

    if hasattr(strategies, 'play') and hasattr(strategies, 'get_signal'):
        strategies = [strategies]

    elif isinstance(strategies, list) and len(strategies) >= 1:
        for s in strategies:
            if not hasattr(strategies, 'play') and hasattr(strategies, 'get_signal'):
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
    def __init__(self, payoff, strategies, **kwargs):
        # type and size checking of payoff
        self.payoff = is_valid_payoff(payoff)

        # type checking of strategies
        self.strategies =  is_valid_strategies(strategies)

        # type checking of ts_length
        ts_length = kwargs.get('ts_length', None)
        self.ts_length = is_valid_ts_length(ts_length)

        self.repeat = kwargs.get('repeat', 1)
        self.signal = kwargs.get('signal', None)
            
    def set_payoff(self, payoff):
        self.payoff = is_valid_payoff(payoff)

    def set_strategies(self, strategies):
        self.strategies = is_valid_strategies(strategies)

    def add_strategies(self, strategies):
        self.strategies = self.strategies + is_valid_strategies(strategies)

    def show_strategies(self):
        print("The object has {0} strategy functions below".format(len(self.strategies)))
        print("-"*50)
        for i, s in enumerate(self.strategies):
            print("{0}.".format(i+1), self.str_name(s))
        print("-"*50)

    def remove_strategies(self, str_name):
        for s in self.strategies:
            if self.str_name(s) == str_name:
                self.strategies.remove(s)

    def set_ts_length(self, ts_length):
        self.ts_length = is_valid_ts_length(ts_length)

    def set_signal(self, signal):
        self.signal = signal

    def str_name(self, strategy):
        return strategy.__module__ + "." + strategy.__name__

    def __play__(self, strategy1, strategy2, mtype, round_ts_length, random_state, record, stage_record):
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
            if mtype == 1: # perfect monitoring
                signal1 = action2
                signal2 = action1

            elif mtype == 2: # imperfect public monitoring
                signal = self.signal([action1, action2], random_state)
                signal1 = signal
                signal2 = signal

            elif mtype == 3: # imperfect private monitoring
                signals = self.signal([action1, action2], random_state)
                signal1 = signals[0]
                signal2 = signals[1]

            else:
                raise ValueError

            # シグナルを渡す
            Strategy1.get_signal(signal1)
            Strategy2.get_signal(signal2)

            if stage_record:
                self.match_result[self.stage_count][0] = i
                self.match_result[self.stage_count][1] = action1
                self.match_result[self.stage_count][2] = action2
                self.match_result[self.stage_count][3] = signal1
                self.match_result[self.stage_count][4] = signal2
                self.match_result[self.stage_count][5] = stage_score1
                self.match_result[self.stage_count][6] = stage_score2

            self.stage_count += 1

        return score1, score2
    

    def play(self, **kwargs):
        Mtype = kwargs.get('mtype', "perfect")
        random_seed = kwargs.get('random_seed', None)
        record = kwargs.get('record', False)
        stage_record = kwargs.get('stage_record', False)

        if random_seed is None:
            random_seed = np.random.seed()
        
        # Monitoring type
        if Mtype == "perfect":
            mtype = 1

        elif Mtype == "public":
            mtype = 2

        elif Mtype == "private":
            mtype = 3

        else:
            msg = "mtype must be \'perfect\', \'public\' or \'private\'"
            raise ValueError(msg)
        
        # Number of strategy classes
        strlen = len(self.strategies)
        if strlen < 2:
            msg = "To play, need at least 2 strategies."
            raise TypeError(msg)
        
        # Number of matches
        matches = strlen**2
        
        # Score table
        total_average = np.zeros((strlen, strlen))
        session_average = np.zeros((strlen, strlen))
        
        # List of time series for all rounds
        ts_list = np.empty(self.repeat, dtype=np.int64)
        for r in range(self.repeat):
            ts_list[r] = self.ts_length[r % len(self.ts_length)]
        
        # Total time series of all rounds (of 1 match)
        total_ts = np.sum(ts_list)

        if record:
            # record table for each match
            self.match_result = np.empty((total_ts, 7), dtype=int)

            # Number of rows in record DataFrame (=total stages)
            row = total_ts * matches

            # Name list of strategic classes
            str_names = [self.str_name(s) for s in self.strategies]

            # rounds(repeats) list of each game in a match
            round_list = np.empty(total_ts, dtype=int)
            count_row = 0
            for r, ts in enumerate(ts_list):
                round_list[count_row:count_row+ts] = r
                count_row += ts

            # 各セットの長さと平均利潤を記録
            set_result = np.zeros((2*self.repeat, matches), dtype=float)

            if stage_record:
                # 各ステージゲームの全記録
                Match = np.zeros(row, dtype=int)
                Round = np.zeros(row, dtype=int)
                for i in range(matches):
                    Match[i*total_ts : (i+1)*total_ts] = i
                    Round[i*total_ts : (i+1)*total_ts] = round_list

                Strategy1 = np.zeros(row, dtype=int)
                Strategy2 = np.zeros(row, dtype=int)
                match_count = 1
                for i in range(strlen):
                    for j in range(strlen):
                        Strategy1[(match_count-1) * total_ts : match_count * total_ts] = i+1
                        Strategy2[(match_count-1) * total_ts : match_count * total_ts] = j+1
                        match_count += 1

                self.record_df = pd.DataFrame({
                    'Mtype'  : np.array([mtype] * row),
                    'RandomSeed': np.array([random_seed] * row),
                    'Strategy1': Strategy1,
                    'Strategy2': Strategy2,
                    'Match'  : Match,
                    'Round'  : Round,
                    'Period' : np.empty(row, dtype=int),
                    'Action1': np.empty(row, dtype=int),
                    'Action2': np.empty(row, dtype=int),
                    'Signal1': np.empty(row, dtype=int),
                    'Signal2': np.empty(row, dtype=int),
                    'Payoff1': np.empty(row, dtype=int),
                    'Payoff2': np.empty(row, dtype=int),
                    }, columns=['Mtype', 'RandomSeed', 'Strategy1', 'Strategy2', 'Match', 'Round',
                    'Period', 'Action1', 'Action2', 'Signal1', 'Signal2', 'Payoff1', 'Payoff2'])

        # current match count
        match_count = 1

        print("Start")
        self.show_strategies()
        print("Repeats: {0}".format(self.repeat))
        print("Total time series length: {0}".format(total_ts))
        
        # play match
        for i, str1 in enumerate(self.strategies):
            for j, str2 in enumerate(self.strategies):
                score1, score2 = 0, 0
                average_score1, average_score2 = 0, 0
                self.stage_count = 0
                random_state = np.random.RandomState(random_seed)

                # play game
                for r in range(self.repeat):
                    round_ts_length = ts_list[r]
                    s1, s2 = self.__play__(str1, str2, mtype, round_ts_length, random_state, record, stage_record)
                    score1 += s1
                    score2 += s2
                    average_score1 += s1 / round_ts_length
                    average_score2 += s2 / round_ts_length
                    if record:
                        if i == j:
                            set_result[r, i*strlen+i] += s1 / round_ts_length
                            set_result[self.repeat+r, i*strlen+i] += s2 / round_ts_length
                        elif i < j:
                            set_result[r, i*strlen+j] += s1 / round_ts_length
                            set_result[r, j*strlen+i] += s2 / round_ts_length
                        else:
                            set_result[self.repeat+r, i*strlen+j] += s1 / round_ts_length
                            set_result[self.repeat+r, j*strlen+i] += s2 / round_ts_length

                if stage_record:
                    self.record_df.loc[(match_count-1)*total_ts : match_count*total_ts-1, 'Period':'Payoff2'] \
                     = self.match_result[0:total_ts, 0:7]
                
                total_average[i][j] += score1 / total_ts / 2
                total_average[j][i] += score2 / total_ts / 2
                session_average[i][j] += average_score1 / self.repeat / 2
                session_average[j][i] += average_score2 / self.repeat / 2
                match_count += 1


        # ランキング作成
        sum_session_ave = np.zeros(strlen, dtype=float)
        sum_total_ave = np.zeros(strlen, dtype=float)
        for i in range(strlen):
            sum_session_ave[i] = np.sum(session_average[i]) / strlen
            sum_total_ave[i] = np.sum(total_average[i]) / strlen
        
        ranking_session = np.argsort(sum_session_ave)[::-1]
        ranking_total = np.argsort(sum_total_ave)[::-1]

        for i in range(strlen):
            s = ranking_session[i]

        print("\nScore table:")
        print("各セッションを重率1で平均した得点")
        print(session_average)
        print("")
        print("各ステージゲームを重率1で平均した得点")
        print(total_average)


        if record:
            current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            os.mkdir("experiment_{0}".format(current_time))

            # 実験概要を記録
            summary = [["Datetime", current_time],
                      ["Monitoring type", Mtype],
                      ["RandomSeed", random_seed],
                      ["Repeats", self.repeat],
                      ["Average ts_length", np.average(ts_list)],
                      ["Number of strategies", strlen],
                      ["Str No.", "Strategy name", "Average(session based)", "Rank(session based)", "Average(stage based)", "Rank(stage based)"]]

            cor = [[i+1,
                    self.str_name(strategy),
                    sum_session_ave[i],
                    np.where(ranking_session == i)[0][0]+1,
                    sum_total_ave[i],
                    np.where(ranking_total == i)[0][0]+1] for i, strategy in enumerate(self.strategies)]
            
            summary_df = pd.DataFrame(summary + cor)
            summary_df.to_csv("./experiment_" + str(current_time) + "/summary.csv", index=False, header=False)

            # ステージゲームの全記録
            if stage_record:
                self.record_df.to_csv("./experiment_" + str(current_time) + "/record.csv")

            # 各セットの記録
            array1 = np.arange(1, strlen+1)
            tuples1 = list(itertools.product(array1, repeat=2))
            array2 = np.zeros((2, 2*self.repeat), dtype=int)
            array2[0] = np.arange(2*self.repeat)
            array2[1, 0:1000] = ts_list
            array2[1, 1000:2000] = ts_list
            tuples2 = list(zip(*array2))
            row_index = pd.MultiIndex.from_tuples(tuples1, names=['player', 'opponent'])
            col_index = pd.MultiIndex.from_tuples(tuples2, names=['round', 'ts_length'])
            set_result_df = pd.DataFrame(set_result, index=col_index, columns=row_index)
            set_result_df.to_csv("./experiment_" + str(current_time) + "/set_result.csv")

            # 平均利得表を記録
            session_average_df = pd.DataFrame(session_average, index=list(range(1, strlen+1)), columns=list(range(1, strlen+1)))
            session_average_df.to_csv("./experiment_" + str(current_time) + "/session_average.csv")
            total_average_df = pd.DataFrame(total_average, index=list(range(1, strlen+1)), columns=list(range(1, strlen+1)))
            total_average_df.to_csv("./experiment_" + str(current_time) + "/total_average.csv")

 
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


    # 「相手の」シグナルが協調か攻撃かを（ノイズ付きで）返す
    def private_signal(actions, random_state):
        pattern = [[0, 0], [0, 1], [1, 0], [1, 1]]
        # 例えば実際の行動が(0, 1)なら、シグナルは(1, 0)である可能性が最も高い
        signal_probs = [[.9, .02, .02, .06], [.02, .06, .9, .02], [.02, .9, .06, .02], [.06, .02, .02, .9]]
        prob = random_state.uniform()
        if actions[0] == 0 and actions[1] == 0:
            choice = random_state.choice(4, p=signal_probs[0])
            return pattern[choice]
        elif actions[0] == 0 and actions[1] == 1:
            choice = random_state.choice(4, p=signal_probs[1])
            return pattern[choice]
        elif actions[0] == 1 and actions[1] == 0:
            choice = random_state.choice(4, p=signal_probs[2])
            return pattern[choice]
        elif actions[0] == 1 and actions[1] == 1:
            choice = random_state.choice(4, p=signal_probs[3])
            return pattern[choice]
        else:
            raise ValueError

    strategies = [Iida_iprm, KatoStrategy]
    game = RepeatedMatrixGame(payoff, strategies, signal=private_signal, ts_length=ts_length, repeat=1)
    game.play(mtype="private", random_seed=seed, record=True)



