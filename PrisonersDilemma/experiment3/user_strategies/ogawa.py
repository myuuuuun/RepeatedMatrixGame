class ogawa(object):
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.my_history = []
        self.signals = []

    def play(self):
        if len(self.signals) <= 1:
            return 0

        prior_signal = self.signals[-1]
        prior2_signal = self.signals[-2]
        epsilon = self.random_state.uniform()

        if len(self.signals) < 33:
            if epsilon < 0.05:
                self.my_history.append(1)
                return 1
            elif prior_signal == 1 and prior2_signal == 1:
                self.my_history.append(1)
                return 1
            else:
                self.my_history.append(0)
                return 0
        else:
            self.my_history.append(1)
            return 1

    def get_signal(self, signal):
        self.signals.append(signal)
