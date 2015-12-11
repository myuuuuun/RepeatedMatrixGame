class beeleb():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.random_state()
        self.random_state = random_state        
        self.my_history = []
        self.signals = []

    def play(self):
        # 5期目まではシグナルに関わらず協調
        if len(self.signals) < 5:
            self.my_history.append(0)
            return 0

        # 直近5期分のシグナルと自分の行動から今期の行動を決定
        # 終了確率が前回より高いのでちょっとだけ短絡的にしてみた
        # シグナルの正誤についてはあまり考えていない
        # 複数回のシグナルをもとに考えたらそこまで間違いはないだろう，ぐらい
        prior_signals = sum(self.signals[-5:])
        prior_my_histories = sum(self.signals[-5:])

        # 5回中4回以上裏切りシグナルなら完全に裏切りの方針だと判断
        if prior_signals >= 4:
            self.my_history.append(1)
            return 1
        # 裏切りシグナルが少ないか自分の行動に裏切りが多いと協調する
        elif prior_signals <= 2 or prior_my_histories >= 3 :
            self.my_history.append(0)
            return 0
        # 上記で判断ができない時はとりあえず裏切っておく
        else:
            self.my_history.append(1)
            return 1


    # 各期のゲーム終了時に呼び出されるメソッド
    def get_signal(self, signal):
        # 前期のゲームのシグナルを受け取る
        # 受け取ったシグナルをシグナルの履歴に追加
        self.signals.append(signal)