#-*- encoding: utf-8 -*-
'''
サンプル戦略集
'''

from __future__ import division, print_function
import math
import functools #for python3
from random import randint


# テンプレート
class MyStrategy():
    def __init__(self, RandomState):
        # RandomStateオブジェクトのインスタンスを受け取る
        # 確率変数を使いたい場合は、このインスタンスを使う
        self.RandomState = RandomState
        # 自分の行動の履歴
        self.my_history = []
        # 過去の全てのシグナル
        self.signals = []


    # 各ステージゲームの実行時に呼び出されるメソッド
    # その期の行動を0（=協調）, または1（=攻撃）のいずれかから選ぶ
    def play(self):
        # 第1期は協調
        if len(self.signals) < 1:
            self.my_history.append(0)
            return 0

        # 前期のシグナル
        prior_signal = self.signals[-1]

        # 前期のシグナルがBadの時、20%の割合でこちらも攻撃する
        epsilon = self.RandomState.uniform()
        if epsilon > 0.8 and prior_signal == 1:
            self.my_history.append(1)
            return 1
        
        else:
            self.my_history.append(0)
            return 0


    # 各期のゲーム終了時に呼び出されるメソッド
    def get_signal(self, signal):
        # 前期のゲームのシグナルを受け取る
        # 受け取ったシグナルをシグナルの履歴に追加
        self.signals.append(signal)


# 常に協調
class AllC():
    def __init__(self, RandomState):
        pass

    def play(self):
        return 0

    def get_signal(self, signal):
        pass


# 常に攻撃
class AllD():
    def __init__(self, RandomState):
        pass

    def play(self):
        return 1

    def get_signal(self, signal):
        pass



# 最初は協調を続け、相手が1度でも攻撃してきたら以後ずっと攻撃
# imperfect monitoringの場合は、シグナルが1になれば、以降ずっと攻撃
class GrimTrigger():
    def __init__(self, RandomState):
        # 相手が協力的かどうかのflag
        # 相手が1度でも攻撃してきたらFalseにする
        self.cooperation_flag = True

    def play(self):
        if self.cooperation_flag:
            return 0

        else:
            return 1

    def get_signal(self, signal):
        if signal == 1:
            self.cooperation_flag = False


# 協調と攻撃を交互に繰り返す
class Alternate():
    def __init__(self, RandomState):
        # 次にどの手をだすかのflag
        # Trueなら次は0, Falseなら次は1を出す
        self.flag = True

    def play(self):
        if self.flag:
            return 0

        else:
            return 1

    def get_signal(self, signal):
        self.flag = not self.flag


# ランダム
class RandomStrategy():
    def __init__(self, RandomState):
        self.RandomState = RandomState

    def play(self):
        return self.RandomState.randint(0, 1)

    def get_signal(self, signal):
        pass


