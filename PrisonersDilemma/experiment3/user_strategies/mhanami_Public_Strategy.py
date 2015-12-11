class PubStrategy():
    def __init__(self,random_state=None):
        self.signals = []
        self.my_history = []

    def play(self):
        if len(self.signals) < 1:
            self.my_history.append(0)
            return 0

        prior_signal = self.signals[-1]

        if 1 <= len(self.signals) < 3:
            if 1 in self.signals:
                self.my_history.append(1)
                return 1

            else:
                return 0

        if 3 <= len(self.signals):
            dob_prior_signal = self.signals[-2]
            trip_prior_signal = self.signals[-3]
            my_prior_action = self.my_history[-1]


            if prior_signal == 1 and my_prior_action == 0:
                self.my_history.append(1)
                return 1

            elif prior_signal == 0 and dob_prior_signal == 0 and trip_prior_signal == 0 and my_prior_action == 1:
                self.my_history.append(0)
                return 0

            else:
                self.my_history.append(my_prior_action)
                return my_prior_action


    def get_signal(self, signal):
        self.signals.append(signal)



