import numpy as np


# Base class
class TwoStateAutomatonBase(object):
    num_states, num_signals = 2, 2
    cooperate, punish = 0, 1
    good, bad = 0, 1

    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state

        # Initial state
        self.state = self.cooperate

        # Probabilities of transition to the other state,
        # to be set by child classes
        # `self.trans_prob[state, signal]`:
        # probability of transition from `state` (= 0, 1) to `1 - state`
        # when the signal is `signal`
        self.trans_prob = np.zeros((self.num_states, self.num_signals))

    def play(self):
        return self.state

    def get_signal(self, signal):
        self.state_transition(signal)

    def state_transition(self, signal):
        if self.trans_prob[self.state, signal] == 0:
            pass
        elif self.trans_prob[self.state, signal] == 1:
            self.state = 1 - self.state
        else:
            r = self.random_state.random_sample()
            if r < self.trans_prob[self.state, signal]:
                self.state = 1 - self.state


# Class for perfect monitoring
class OyamaPerfectMonitoring(TwoStateAutomatonBase):
    def __init__(self, random_state=None):
        super(OyamaPerfectMonitoring, self).__init__(random_state)

        self.trans_prob[self.cooperate, self.bad] = 1


# Class for imperfect public monitoring
class OyamaImperfectPublicMonitoring(TwoStateAutomatonBase):
    def __init__(self, random_state=None):
        super(OyamaImperfectPublicMonitoring, self).__init__(random_state)

        self.trans_prob[self.cooperate, self.bad] = 0.3


# Class for imperfect private monitoring
class OyamaImperfectPrivateMonitoring(TwoStateAutomatonBase):
    def __init__(self, random_state=None):
        super(OyamaImperfectPrivateMonitoring, self).__init__(random_state)

        self.trans_prob[self.cooperate, self.bad] = 0.3
        self.trans_prob[self.punish, self.good] = 0.3
