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
        #encounteringTime = json.load(f)['3214']
        #encounteringTime = json.load(f)['3032']
        encounteringTime = json.load(f)['3201']

print(encounteringTime)

dataSize = 1e8 # 100 Mbits file
utility = 2500 # At most about 250s to download
B_r = 5e6 # 8 Mbits/s
B_c = 1e6 # 1 Mbits/s 
cost = 1000 # cost for cellular
timeToDownload = 8 # 5s to download from RSU on average
decay_list = [6, 8, 10, 12, 14]
print("%15s%15s%15s%15s" % ("decay", "Best cost", "Best delay", "proposed"))

for d in decay_list:
    decay = d
    bc = best_cost(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    bd = best_delay(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    ps = cnt(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    print("%15d%15d%15d%15d" % (decay, bc, bd, ps))
