class KatoStrategy(object):
    def __init__(self, random_state=None):
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state

        self.my_history = []
        
        self.signals = []
        
    def normal_action(self):
        if len(self.signals)%3 == 1:
            self.my_history.append(1)
            return 1
        elif len(self.signals)%3 == 2:
            self.my_history.append(0)
            return 0
        else:
            self.my_history.append(0)
            return 0
        
    def attack_action(self):
        self.my_history.append(1)
        return 1
    
    def research1(self):
        num_attack = 0.0
        for i in self.signals:
            if i == 1:
                num_attack += 1.0
        attack_percent = num_attack / (float(len(self.signals))+1)
        if attack_percent >= 0.5:
            return 1
        else:
            return 0
        
    def research2(self):
        for i in range(len(self.signals)-3):
            if self.signals[-i-1] == 1 and self.signals[-i-2] == 1 and self.signals[-i-3] == 1:
                return 1
        else:
            return 0
        
    def research3(self):
        num_attack = 20.0
        for i in self.signals:
            if i == 1:
                num_attack += 1.0
        attack_percent = num_attack / (float(len(self.signals))+1)
        if attack_percent >= 0.2:
            return 1
        else:
            return 0

    def play(self):
        research1_result = self.research1()
        research3_result = self.research3()
        if len(self.signals) <= 3:
            if research1_result == 0:
                return self.normal_action()
            else:
                return self.attack_action()
        else:
            prior_signal = self.signals[-1]
            research2_result = self.research2()
            if research2_result == 1:
                return self.attack_action()
            elif research1_result == 1:
                return self.attack_action()
            elif lem(self.myself) >= 20 and research3_result == 1:
                return self.attack_action()
            else:
                return self.normal_action()

    def get_signal(self, signal):
        self.signals.append(1)
