import random

class GeneralEncounteringTime():
    def __init__(self):
        pass

    def countEncounteringTime(self, intervals):
        encounteringTime = []
        encounteringTime.append(intervals[0])

        for i in range(1, len(intervals)):
            encounteringTime.append(encounteringTime[i - 1] + intervals[i])

        return encounteringTime
    

class ExponentialEncounteringTime(GeneralEncounteringTime):
    def __init__(self, mu, eventNumber):
        self.mu = mu
        self.eventNumber = eventNumber
        self.intervals = []
        pass;

    def rand(self):
        self.intervals = [2 + random.expovariate(1./(self.mu-2)) for i in range(self.eventNumber)]
        return super(ExponentialEncounteringTime, self).countEncounteringTime(self.intervals)
    
    def fix(self):
        return super(ExponentialEncounteringTime, self).countEncounteringTime(self.intervals)

class  GaussianEncounteringTime(GeneralEncounteringTime):
    def __init__(self, mu, sigma, eventNumber):
        self.intervals = []
        self.mu = mu
        self.sigma = sigma
        self.eventNumber = eventNumber
        pass;

    def rand(self):
        self.intervals = [2 + random.gauss(self.mu-2, self.sigma) for i in range(self.eventNumber)]
        return super(GaussianEncounteringTime, self).countEncounteringTime(self.intervals)
    
    def fix(self):
        return super(GaussianEncounteringTime, self).countEncounteringTime(self.intervals)
