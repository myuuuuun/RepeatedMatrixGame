class GrimTrigger(object):
    def __init__(self, random_state=None):
        self.cooperation_flag = True
        if random_state is None:
            random_state = np.random.random_state()
        self.random_state = random_state

    def play(self):
        if self.cooperation_flag:
            return 0
        else:
            return 1

    def get_signal(self, signal):
        if signal == 1:
            epsilon = self.random_state.uniform()
            if epsilon > 0.5:
                self.cooperation_flag = False
            else:
                self.cooperation_flag = True