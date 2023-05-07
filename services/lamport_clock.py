class LamportClock(object):
    def __init__(self):
        self._clock = 0
        
    def get(self):
        return self._clock
    
    def update(self, other_clock: int):
        self._clock = max(other_clock, self._clock) + 1
        
lamport_clock = LamportClock()