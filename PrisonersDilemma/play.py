#-*- encoding: utf-8 -*-
'''
Simulate finite repeated symmetric matrix game.
Copyright (c) 2015 @myuuuuun

Released under the MIT license.
'''

from __future__ import division, print_function
import math
import functools #for python3
from random import randint, random
import numpy as np
from numpy.random import geometric
import sys
from sample import *
np.set_printoptions(precision=3)


class UnsupportedArgumentError(Exception):
    def __init__(self, msg):
        pass


# type and size checking of payoff
def is_valid_payoff(payoff):
    msg1 = "Argument \"payoff\" must be square matrix(array_like, ndim=2)."
    msg2 = ("Argument \"payoff\" must be square matrix(array_like, ndim=2)"
            " and each element of it must be integer or float.")
    
    if isinstance(payoff, list):
        row = len(payoff)
        for x in payoff:
            if not isinstance(x, list):
                raise UnsupportedArgumentError(msg1)

            if len(x) != row:
                raise UnsupportedArgumentError(msg1)
                
            for y in x:
                if not isinstance(y, (float, int)):
                    raise UnsupportedArgumentError(msg2)
        
    elif isinstance(payoff, np.ndarray):
        if payoff.ndim != 2:
            raise UnsupportedArgumentError(msg1)

        row, col = payoff.shape
        if row != col:
            raise UnsupportedArgumentError(msg1)

        if not np.issubdtype(payoff.dtype, (int, float)):
            raise UnsupportedArgumentError(msg2)

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
                raise UnsupportedArgumentError(msg)

    else:
        raise UnsupportedArgumentError(msg)

    return strategies


# type checking of ts_length
def is_valid_ts_length(ts_length):
    if not isinstance(ts_length, int) or ts_length < -1:
        raise UnsupportedArgumentError(
            ("Argument \"ts_length\" must be integer that"
             " satisfies 0<=ts_length or ts_length=-1, None.")
            )

    elif ts_length == -1 or ts_length is None:
                ts_length = randint(1000, 10000)

    elif 0 < ts_length:
        ts_length = ts_length

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

    ts_length: int(optional), default=None
        Number of repetition of games.
        If None or -1, pick random number from 1000 to 10000.
    '''
    def __init__(self, payoff, strategies, ts_length=None, **kwargs):
        # kwargs: discount factor, is_play_with_myself...

        # type and size checking of payoff
        self.payoff, self.actlen = is_valid_payoff(payoff)

        # type checking of strategies
        self.strategies =  is_valid_strategies(strategies)

        # type checking of ts_length
        self.ts_length = is_valid_ts_length(ts_length)
            
    def set_payoff(self, payoff):
        self.payoff, self.actlen = is_valid_payoff(payoff)

    def set_strategies(self, strategies):
        self.strategies = is_valid_strategies(strategies)

    def add_strategies(self, strategies):
        self.strategies = self.strategies + is_valid_strategies(strategies)

    def show_strategies(self):
        print("The object has {0} strategy functions below.".format(len(self.strategies)))
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


    def __play__(self, strategy1, strategy2):
        history1 = []
        history2 = []
        score1 = 0
        score2 = 0

        for i in range(self.ts_length):
            action1 = strategy1(history1, history2)
            action2 = strategy2(history2, history1)

            """
            print("----------------------")
            print("{0} 期目".format(i+1))
            m1 = "協調" if action1 == 0 else "攻撃"
            m2 = "協調" if action2 == 0 else "攻撃"
            print("プレイヤー1の行動は {0}".format(m1))
            print("プレイヤー2の行動は {0}".format(m2))
            print("----------------------\n")
            """

            history1.append(action1)
            history2.append(action2)

            score1 += self.payoff[action1][action2]
            score2 += self.payoff[action2][action1]
            
        return score1, score2


    def play(self):
        strlen = len(self.strategies)
        if strlen < 2:
            print("To play, need at least 2 strategies functions.")
            return

        result = np.zeros((strlen, strlen), dtype=int)
        count = 1
        print("Start")
        self.show_strategies()
        print("Time series length: {0}".format(self.ts_length))
        
        for i, str1 in enumerate(self.strategies):
            for j, str2 in enumerate(self.strategies[i+1:]):
                score1, score2 = self.__play__(str1, str2)
                print("-"*50)
                print("Game {0}: \"{1}\" vs \"{2}\"".format(count, str1.__name__, str2.__name__))
                print("stage score of", str1.__name__, ": " , score1)
                print("stage score of", str2.__name__, ": " , score2)
                result[i][i+j+1] = score1
                result[i+j+1][i] = score2
                count += 1;
                
        print("-"*50)
        print("Score table:")
        print(result)

        print("\nRanking:")

        total = np.zeros(strlen, dtype=int)
        for i in range(strlen):
            total[i] = np.sum(result[i])
        
        ranking = np.argsort(total)[::-1]
        for i in range(strlen):
            s = ranking[i]
            print("{0}. \"{1}\"".format(i+1, self.strategies[s].__name__))
            print("total points: {0}, average points per game: {1}, average points per stage: {2}"
                .format( total[s], total[s]/(strlen-1), total[s]/((strlen-1)*self.ts_length) ))


if __name__ == '__main__':
    payoff = np.array([[2, 0], [3, 1]])
    discount_v = 0.9999
    playtimes = geometric(1 - discount_v)

    strategies = [grim_trigger, random_strategy, allC, allD, alternate, two_one, tit_for_tat, probability]
    game = RepeatedMatrixGame(payoff, strategies, playtimes)
    game.play()


