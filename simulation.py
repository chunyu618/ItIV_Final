import random
import sys
import json
from lib.utils import *
from lib.data import ExponentialEncounteringTime
from lib.data import GaussianEncounteringTime

encounteringtime = []
dataGenerator = ExponentialEncounteringTime(30, 500)
#encounteringTime = dataGenerator.rand()

if '--real' in sys.argv:
    
    with open('./result/bus-ap-res/2007-11-02.txt') as f:
        encounteringTime = json.load(f)['3204']

print(encounteringTime)

dataSize = 6e6
utility = 10000
B_r = 1e5
B_c = 2e4
cost = 1000
timeToDownload = 5
decay_list = [2, 4, 6, 8, 10, 12]
print("%15s%15s%15s%15s" % ("decay", "Best cost", "Best delay", "proposed"))

for d in decay_list:
    decay = d
    bc = best_cost(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    bd = best_delay(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    ps = cnt(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    print("%15d%15d%15d%15d" % (decay, bc, bd, ps))
