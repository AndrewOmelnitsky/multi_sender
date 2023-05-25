class LamportClock(object):
    def __init__(self):
        self._clock = 0
        self._history = [self._clock, ]
        
    def get(self):
        return self._clock
    
    def get_history(self):
        return self._history
    
    def update(self, other_clock: int):
        self._clock = max(other_clock, self._clock) + 1
        self._history.append(self._clock)
        
lamport_clock = LamportClock()