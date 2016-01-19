from __future__ import division, print_function
import numpy as np
import math
import sys
sys.path.append('../')
import play as pl

class Strategy1():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.my_history = []
        self.signals = []
        self.flag = False

    def play(self):
        if len(self.signals) < 1:
            self.my_history.append(0)
            return 0

        if self.flag:
            self.my_history.append(1)
            return 1

        prior_signal = self.signals[-1]
        prior_action = self.my_history[-1]

        epsilon = self.random_state.uniform()
        if prior_action == 0:
            if prior_signal == 1 and epsilon < 0.9:
                self.my_history.append(1)
                return 1

            else:
                self.my_history.append(0)
                return 0
        
        else:
            if prior_signal == 0 and epsilon < 0.4:
                self.my_history.append(1)
                self.flag = True
                return 1

            else:
                self.my_history.append(0)
                return 0

    def get_signal(self, signal):
        self.signals.append(signal)


class Strategy2():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.prior_action = 0
        self.prior_signal = 0

    def play(self):
        if self.prior_action == 0 and self.prior_signal == 0:
            self.prior_action = 0
            return 0

        elif self.prior_action == 0 and self.prior_signal == 1:
            self.prior_action = 1
            return 1

        elif self.prior_action == 1 and self.prior_signal == 0:
            self.prior_action = 1
            return 1

        elif self.prior_action == 1 and self.prior_signal == 1:
            self.prior_action = 0
            return 0

        else:
            raise ValueError()

    def get_signal(self, signal):
        self.prior_signal = signal


class Strategy3():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.prior_action = 0
        self.prior_signal = 0

    def play(self):
        if self.prior_action == 0:
            if self.prior_signal == 0:
                self.prior_action = 0
                return 0

            else:
                self.prior_action = 1
                return 1
        
        else:
            epsilon = self.random_state.uniform()
            if self.prior_signal == 1 and epsilon < 0.8:
                self.prior_action = 0
                return 0

            else:
                self.prior_action = 1
                return 1

    def get_signal(self, signal):
        self.prior_signal = signal


class Strategy4():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.my_history = []
        self.prior_signal = 0
        self.bads = 0

    def play(self):
        if self.bads < 3:
            if self.prior_signal == 0:
                self.bads = 0
            
            self.my_history.append(0)
            return 0

        if self.bads >= 3:
            if self.prior_signal == 0 or self.bads >=6:
                self.bads = 2
                self.my_history.append(0)
                return 0
            
            else:
                self.my_history.append(1)
                return 1

    def get_signal(self, signal):
        self.prior_signal = signal
        self.bads += signal


class Strategy5():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.prior_signal = 0
        self.current_place = 0

    def play(self):
        if self.current_place == 0:
            self.current_place = 1
            return 0

        elif 1 <= self.current_place <= 4:
            if self.prior_signal == 0:
                self.current_place += 1
                return 0

            else:
                self.current_place = 7
                return 0

        elif self.current_place == 5:
            if self.prior_signal == 0:
                self.current_place = 6
                return 1

            else:
                self.current_place = 7
                return 0

        elif self.current_place == 6:
            self.current_place = 7
            return 0

        elif self.current_place == 7:
            if self.prior_signal == 0:
                self.current_place = 1
                return 0

            else:
                self.current_place = 8
                return 1

        elif self.current_place == 8:
            self.current_place = 1
            return 0

        raise ValueError()


    def get_signal(self, signal):
        self.prior_signal = signal


class Strategy6():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.bads = 0

    def play(self):
        if self.bads % 3 == 2:
            return 1

        else:
            return 0

    def get_signal(self, signal):
        self.bads += signal


class Strategy7():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.signals = []

    def play(self):
        if len(self.signals) < 1:
            return 0

        epsilon = self.random_state.uniform()
        if epsilon < 0.08:
            return 1 - self.signals[-1]

        else:
            return self.signals[-1]

    def get_signal(self, signal):
        self.signals.append(signal)


class Strategy8():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.bads = 0

    def play(self):
        if self.bads <= 10:
            return 0

        else:
            return 1

    def get_signal(self, signal):
        self.bads += signal


class Strategy9():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.signal = 1

    def play(self):
        return self.signal

    def get_signal(self, signal):
        self.signal = signal


class Strategy10():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.signals = []

    def play(self):
        if len(self.signals) < 1:
            return 0

        epsilon = self.random_state.uniform()
        if epsilon < 0.1:
            return 1 - self.signals[-1]

        else:
            return self.signals[-1]

    def get_signal(self, signal):
        self.signals.append(signal)


class Strategy11():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.place = 0
        self.signal = 0

    def play(self):
        if self.place == 0:
            self.place = 1
            return 0

        if self.place == 1:
            if self.signal == 0:
                return 0
            else:
                self.place = 2
                return 0

        if self.place == 2:
            if self.signal == 0:
                return 0
            else:
                self.place = 3
                return 1

        if self.place == 3:
            if self.signal == 1:
                return 1
            else:
                self.place = 1
                return 0

        else:
            raise ValueError()

    def get_signal(self, signal):
        self.signal = signal


class Strategy12():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.start = True
        self.flag1 = False
        self.flag2 = False
        self.flag3 = False

    def play(self):
        if self.start:
            self.start = False
            self.flag1 = True
            return 0
        
        if self.flag1:
            self.flag1 = False
            if self.signal == 0:
                self.flag3 = True
                return 1
            else:
                self.flag2 = True
                return 1
        
        if self.flag2:
            if self.signal == 0:
                self.flag2 = False
                self.flag3 = True
                return 1
            else:
                return 1

        if self.flag3:
            self.flag3 = False
            if self.signal == 0:
                self.flag1 = True
                return 0
            else:
                self.flag2 = True
                return 1

    def get_signal(self, signal):
        self.signal = signal


class Strategy13():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.signals = 0

    def play(self):
        if self.signals < 2:
            return 0
        else:
            return 1

    def get_signal(self, signal):
        self.signals += 1


class Strategy14():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.start = True
        self.flag1 = False
        self.flag2 = False
        self.flag3 = False
        self.flag4 = False
        self.signal = 0

    def play(self):
        epsilon = self.random_state.uniform()
        if self.start:
            self.start = False
            self.flag1 = True
            return 0
        
        if self.flag1:
            if self.signal == 0:
                return 0
            else:
                self.flag1 = False
                if epsilon < 0.5:
                    self.flag2 = True
                    return 0

                else:
                    self.flag3 = True
                    return 1
        
        if self.flag2:
            if self.signal == 0:
                return 0
            else:
                self.flag2 = False
                self.flag3 = True
                return 1

        if self.flag3:
            if self.signal == 0:
                return 1
            else:
                self.flag3 = False
                if epsilon < 0.5:
                    self.flag4 = True
                    return 1

                else:
                    self.flag1 = True
                    return 0

        if self.flag4:
            if self.signal == 0:
                return 1
            else:
                self.flag4 = False
                self.flag1 = True
                return 0

        raise ValueError

    def get_signal(self, signal):
        self.signal = signal


class Strategy15():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.my_prior_action = 0
        self.signals = []

    def play(self):
        if len(self.signals) < 1:
            self.my_prior_action = 0
            return 0

        epsilon = self.random_state.uniform()
        if self.my_prior_action == 0:
            if epsilon < 0.8:
                self.my_prior_action = self.signals[-1]
                return self.my_prior_action
            else:
                self.my_prior_action = 1 - self.signals[-1]
                return self.my_prior_action

        else:
            if epsilon < 0.2:
                self.my_prior_action = self.signals[-1]
                return self.my_prior_action
            else:
                self.my_prior_action = 1 - self.signals[-1]
                return self.my_prior_action


    def get_signal(self, signal):
        self.signals.append(signal)


class Strategy16():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.prior_action = 0
        self.prior_signal = 0

    def play(self):
        if self.prior_action == 0 and self.prior_signal == 0:
            self.prior_action = 0
            return 0

        elif self.prior_action == 0 and self.prior_signal == 1:
            self.prior_action = 1
            return 1

        elif self.prior_action == 1 and self.prior_signal == 0:
            self.prior_action = 1
            return 1

        elif self.prior_action == 1 and self.prior_signal == 1:
            self.prior_action = 0
            return 0

        else:
            raise ValueError()

    def get_signal(self, signal):
        self.prior_signal = signal


class Strategy17():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.place = 0
        self.signal = 0

    def play(self):
        if self.place == 0:
            self.place = 1
            return 0

        if self.place == 1:
            if self.signal == 0:
                return 0
            else:
                self.place = 2
                return 0

        if self.place == 2:
            if self.signal == 0:
                return 0
            else:
                self.place = 3
                return 1

        if self.place == 3:
            if self.signal == 1:
                return 1
            else:
                self.place = 4
                return 1

        if self.place == 4:
            if self.signal == 1:
                return 1
            else:
                self.place = 1
                return 0

        else:
            raise ValueError()

    def get_signal(self, signal):
        self.signal = signal


class Strategy18():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.place = 0
        self.signal = 0

    def play(self):
        if self.place == 0:
            self.place = 1
            return 0

        if self.place == 1:
            if self.signal == 0:
                return 0
            else:
                self.place = 2
                return 1

        if self.place == 2:
            if self.signal == 0:
                return 1
            else:
                self.place = 3
                return 1

        if self.place == 3:
            if self.signal == 0:
                self.place = 2
                return 1
            else:
                self.place = 4
                return 1

        if self.place == 4:
            if self.signal == 0:
                self.place = 2
                return 1
            else:
                self.place = 1
                return 0

        else:
            raise ValueError()

    def get_signal(self, signal):
        self.signal = signal


class Strategy19():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.signal = 0

    def play(self):
        return self.signal

    def get_signal(self, signal):
        self.signal = signal


class Strategy20():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.prior_action = 0
        self.signals = []

    def play(self):
        if len(self.signals) < 1:
            self.prior_action = 0
            return 0

        epsilon = self.random_state.uniform()
        if (self.signals[-1] == 0 and epsilon < 0.9) or (self.signals[-1] == 1 and epsilon < 0.1):
            return self.prior_action

        else:
            self.prior_action = 1 - self.prior_action
            return self.prior_action

    def get_signal(self, signal):
        self.signals.append(signal)


class Strategy21():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.prior_action = 0
        self.signals = []

    def play(self):
        if len(self.signals) < 1:
            self.prior_action = 0
            return 0

        epsilon = self.random_state.uniform()
        if (self.signals[-1] == 0) or (self.signals[-1] == 1 and epsilon < 0.08):
            return self.prior_action

        else:
            self.prior_action = 1 - self.prior_action
            return self.prior_action

    def get_signal(self, signal):
        self.signals.append(signal)


class Strategy22():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.place = 0
        self.signal = 0

    def play(self):
        if self.place == 0:
            self.place = 1
            return 0

        if self.place == 1:
            if self.signal == 0:
                return 0
            else:
                self.place = 2
                return 1

        if self.place == 2:
            if self.signal == 0:
                return 1
            else:
                self.place = 3
                return 0

        if self.place == 3:
            self.place = 1
            return 0

        else:
            raise ValueError()

    def get_signal(self, signal):
        self.signal = signal


class Strategy23():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.place = 0
        self.signal = 0

    def play(self):
        if self.place == 0:
            self.place = 1
            return 0

        if self.place == 1:
            if self.signal == 0:
                return 0
            else:
                self.place = 2
                return 0

        if self.place == 2:
            if self.signal == 0:
                self.place = 1
                return 0
            else:
                self.place = 3
                return 1

        if self.place == 3:
            self.place = 1
            return 0

        else:
            raise ValueError()

    def get_signal(self, signal):
        self.signal = signal


class Strategy24():
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state
        self.place = 0
        self.signal = 0

    def play(self):
        if self.place == 0:
            self.place = 1
            return 1

        if self.place == 1:
            if self.signal == 0:
                return 1
            else:
                self.place = 2
                return 0

        if self.place == 2:
            self.place = 1
            return 1

        else:
            raise ValueError()

    def get_signal(self, signal):
        self.signal = signal


