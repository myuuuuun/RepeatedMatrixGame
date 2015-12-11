# -*- coding: utf-8 -*-
class Iida_ipm():
    def __init__(self, random_state=None):
        # RandomStateオブジェクトのインスタンスを受け取る
        # 確率変数を使いたい場合は、このインスタンスを使う
        if random_state is None:
            random_state = np.random.Random_state()
        self.random_state = random_state

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

        #前期のシグナルが1のときは、確率0.8で攻撃、確率0.2で協調
        epsilon = self.random_state.uniform()
        if self.signals[-1] == 1 and epsilon > 0.2:
            self.my_history.append(1)
            return 1

        if self.signals[-1] == 1 and epsilon <= 0.2:
            self.my_history.append(0)
            return 0

        #前期のシグナルが0のときは、2期前に攻撃していたときのみ攻撃、そのほかは協調
        if len(self.signals) > 2 and self.signals[-1] == 0 and self.my_history[-2] == 1:
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