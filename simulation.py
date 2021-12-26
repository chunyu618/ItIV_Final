import random
from lib.utils import *
from lib.data import ExponentialEncounteringTime
from lib.data import GaussianEncounteringTime

dataGenerator = ExponentialEncounteringTime(20, 500)
encounteringTime = dataGenerator.rand()
dataSize = 6e6
utility = 10000
B_r = 5e4
B_c = 1e4
decay = 12
cost = 150
timeToDownload = 3
decay_list = [2, 4, 6, 8, 10]
print("%15s%15s%15s%15s" % ("decay", "Best cost", "Best delay", "proposed"))

for d in decay_list:
    decay = d
    bc = best_cost(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    bd = best_delay(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    ps = cnt(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    print("%15d%15d%15d%15d" % (decay, bc, bd, ps))
