class yamagishi():
    def __init__(self, random_state=None):
        # 相手が協力的かどうかのflag
        # 相手が1度でも攻撃してきたらFalseにする
        self.cooperation_flag = True
        self.signals = []
        
    def play(self):
        if self.cooperation_flag:
            return 0

        else:
            return 1

    def get_signal(self, signal):
        if signal == 1:
            self.cooperation_flag = False
        if signal == 0:
            self.cooperation_flag = True