
class Self_Centered_perfect:
    
    def __init__(self, random_state=None):
        
        if random_state is None:
            random_state = np.random.RandomState()
        self.random_state = random_state

        self.my_history = []

        self.signals = []
        
        self.count = 0
        
        self.count_rate = 0

        
    def play(self):
        
        if self.count_rate >= 0.3:
            return 1
        
        else:
            return 0
    
    def count(self):
        
        if self.signal[-1] == 1:
            self.count += 1
        
        self.count_rate = slef.count / len(self.signal)
        
    
    def get_signal(self, signal):
        self.signals.append(signal)