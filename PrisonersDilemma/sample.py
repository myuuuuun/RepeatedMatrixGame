#-*- encoding: utf-8 -*-
'''
サンプル関数集
'''

from __future__ import division, print_function
import math
import functools #for python3
from random import randint


# 常に協調
def allC(my_history, opponent_history):
    return 0


# 常に攻撃
def allD(my_history, opponent_history):
    return 1


# 相手が協調をする限りは、協調を続ける。攻撃してきたら、次の1回だけ自分も攻撃する
# 相手が直前に出した手を出すのと同じ
def tit_for_tat(my_history, opponent_history):
    if len(opponent_history) < 1:
        return 0

    return opponent_history[-1]


# 最初は協調を続け、相手が1度でも攻撃してきたら以後ずっと攻撃
def grim_trigger(my_history, opponent_history):
    if len(opponent_history) < 1:
        return 0

    if 1 in opponent_history:
        return 1

    else:
        return 0


# 協調と攻撃を交互に繰り返す
def alternate(my_history, opponent_history):
    if(len(my_history) < 1):
        return 0


    return 0 if my_history[-1] == 1 else 1


# 2回協調, 1回攻撃を繰り返す
def two_one(my_history, opponent_history):
    if len(my_history) < 2:
        return 0

    if(my_history[-1] == 0 and my_history[-2] == 0):
        return 1

    else:
        return 0

# 過去に相手が多く出した行動に合わせる
def probability(my_history, opponent_history):
    if len(my_history) < 1:
        return 0

    zeros = opponent_history.count(0)
    ones = len(opponent_history) - zeros

    if zeros >= ones:
        return 0

    else:
        return 1

# ランダム
def random_strategy(my_history, opponent_history):
    return randint(0, 1)



