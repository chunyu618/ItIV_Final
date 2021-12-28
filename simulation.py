import random
import sys
import json
from lib.utils import *
from lib.data import ExponentialEncounteringTime
from lib.data import GaussianEncounteringTime

encounteringTime = []
enounterBusTime = []
dataGenerator = ExponentialEncounteringTime(30, 500)
#encounteringTime = dataGenerator.rand()

realSet = ['3214', '3032', '3201']
if '--real' in sys.argv:
    with open('./result/bus-ap-res/2007-11-02.json') as f:
        #encounteringTime = json.load(f)['3214']
        #encounteringTime = json.load(f)['3032']
        #encounteringTime = json.load(f)['3201']
        encounteringTime = json.load(f)[realSet[int(sys.argv[2])]]
    with open('./result/bus-bus-res/2007-11-02.json') as f:
        encounteringBusTime = json.load(f)[realSet[int(sys.argv[2])]]
        


print(encounteringTime)
print(encounteringBusTime)
dataList = [1, 3, 2, 0, 2, 1, 2, 2, 3, 3, 0, 1]
usage = MDP_approach(dataList, 6, 2, encounteringTime, encounteringBusTime)
print(usage)
exit(0)
#dataSize = 1e8 # 100 Mbits file
dataSize = 100 # 100 Mbits file
utility = 2500 # At most about 250s to download
#B_r = 5e6 # 8 Mbits/s
#B_c = 1e6 # 1 Mbits/s 
B_r = 5 # 8 Mbits/s
B_c = 1 # 1 Mbits/s 
cost = 1000 # cost for cellular
timeToDownload = 5 # 5s to download from RSU on average
decay_list = [6, 8, 10, 12, 14]
print("%15s%15s%15s%15s" % ("decay", "Best cost", "Best delay", "proposed"))

for d in decay_list:
    decay = d
    bc = best_cost(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    bd, bd_cellular_usage = best_delay(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    ps, ps_cellular_usage = proposed_method(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    print("%15d%15d%15d%15d" % (decay, bc, bd, ps))
    print("%15d%15d%15d%15d" % (decay, 0, bd_cellular_usage, ps_cellular_usage))
