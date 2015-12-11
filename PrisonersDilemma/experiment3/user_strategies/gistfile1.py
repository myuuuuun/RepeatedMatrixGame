#-*- encoding: utf-8 -*-

import numpy as np


# 基本協調で二回連続badのシグナルを受けたら70%で攻撃する
class MyStrategy():
    def __init__(self, random_state=None):
        # RandomStateオブジェクトのインスタンスを受け取る
        # 確率変数を使いたい場合は、このインスタンスを使う
        if random_state is None:
            random_state = np.random.random_state()
        self.random_state = random_state

        # 自分の行動の履歴
        self.my_history = []

        # 過去の全てのシグナル
        self.signals = []


    # 各ステージゲームの実行時に呼び出されるメソッド
    # その期の行動を0（=協調）, または1（=攻撃）のいずれかから選ぶ
    def play(self):
        # 第1,2期は協調
        if len(self.signals) < 2:
            self.my_history.append(0)
            return 0

        # 前期と前々期のシグナル
        prior_signal = self.signals[-1]
        prior2_signal = self.signals[-2]

        # 前期と前々期のシグナルがBadの時、70%の割合でこちらも攻撃する
        epsilon = self.random_state.uniform()
        if epsilon > 0.3 and prior_signal == 1 and prior2_signal == 1 :
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

