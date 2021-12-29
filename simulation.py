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
        

print("--------------- Encountering RSU Time ---------------")
print(encounteringTime)
print("--------------- Encountering Bus Time ---------------")
print(encounteringBusTime)

dataList = [[1, 0, 2, 0, 1, 2, 3, 3, 2, 0, 2, 2, 2], 
            [3, 0, 3, 3, 0, 3, 1, 2, 0, 2, 0, 0, 3, 1, 2, 3, 0, 1, 0, 3],
            [2, 1, 2, 2, 2, 1, 2, 3, 3, 3, 0, 3, 0, 1, 3, 1, 3, 0, 1, 0, 1, 3, 0, 0, 1, 2]
            ]
#usage = MDP_approach(dataList, 6, 2, encounteringTime, encounteringBusTime)
#dataSize = 1e8 # 100 Mbits file

dataSizeList = [100, 150, 200] # 100 Mbits file
utilityList = [2500, 3000, 4000] # At most about 250s to download
#B_r = 5e6 # 8 Mbits/s
#B_c = 1e6 # 1 Mbits/s 
B_r = 5 # 8 Mbits/s
B_c = 1 # 1 Mbits/s 
costList = [1000, 1500, 2000] # cost for cellular
timeToDownload = 5 # 5s to download from RSU on average
decay = 10
print("%20s%15s%15s%15s%15s" % ("size/utility/cost", "Best cost", "Best delay", "proposed", "MDP"))

for i in range(1):
    dataSize = dataSizeList[i]
    utility = utilityList[i]
    cost = costList[i]
    dataComingList = dataList[i]
    bc_usage, bc_time = best_cost(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    bd_usage, bd_time = best_delay(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    ps_usage, ps_time = proposed_method(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload)
    MDP_usage, MDP_time = MDP_approach(dataComingList, B_r+1, B_c+1, encounteringTime, encounteringBusTime)
    
    tmp = "%d/%d/%d" % (dataSize, utility, cost)
    print("%20s" %(tmp))
    print("%20s%15d%15d%15d%15d" % ("usage", bc_usage, bd_usage, ps_usage, MDP_usage))
    print("%20s%15d%15d%15d%15d" % ("time", bc_time, bd_time, ps_time, MDP_time))

