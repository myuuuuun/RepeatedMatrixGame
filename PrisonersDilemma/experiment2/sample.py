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

        # 過去の全てのシグナル
        self.my_signals = []
        self.opponent_signals = []


    # 各ステージゲームの実行時に呼び出されるメソッド
    # その期の行動を0（=協調）, または1（=攻撃）のいずれかから選ぶ
    def play(self):
        return self.RandomState.randint(0, 1)


    # 各期のゲーム終了時に呼び出されるメソッド
    def get_signal(self, signal):
        # 前期のゲームのシグナルを配列形式で受け取る
        # signal = [前期の自分の行動のシグナル, 相手の行動のシグナル]
        my_signal = signal[0]
        opponent_signal = signal[1]

        # 受け取ったシグナルをシグナルの履歴に追加
        self.my_signals.append(my_signal)
        self.opponent_signals.append(opponent_signal)


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


# しっぺ返し
class TitForTat():
    def __init__(self, RandomState):
        # 相手の1期前のシグナル
        self.opponent_signal = 0

    def play(self):
        return self.opponent_signal

    def get_signal(self, signal):
        # シグナルを更新
        self.opponent_signal = signal[1]


# 最初は協調を続け、相手が1度でも攻撃してきたら以後ずっと攻撃
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
        if signal[1] == 1:
            self.cooperation_flag = 0


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


