import os, sys
from numpy import mean
import json

def readData_bus_bus(path, date):
    dic = {}
    #print(path, date)
    
    with open(os.path.join(path, date), "r") as f:
        for line in f:
            if line.split()[0] != 'null' and line.split()[1] != 'null':
                ID, time = line.split()[0], line.split()[2]
                h, m, s = int(time.split(':')[0]), int(time.split(':')[1]), int(time.split(':')[2])
                relatedTime = h * 3600 + m * 60 + s
                tmpList = dic[ID] if ID in dic.keys() else []
                tmpList.append(relatedTime)
                dic[ID] = tmpList
    return dic

def readData_bus_ap(path, date):
    encounteringTime = {}
    #print(path, date)
    
    with open(os.path.join(path,date), "r") as f:
        for line in f:
            l = line.split()
            ID = l[0]
            time = l[2].split(':')
            duration = l[4]

            h = int(time[0])
            m = int(time[1])
            s = int(time[2])
            relatedTime = h * 3600 + m * 60 + s

            if ID not in encounteringTime.keys():
                encounteringTime[ID] = []
            encounteringTime[ID].append(relatedTime)
    return encounteringTime

def countDiff(dic):
    totalAvg = []
    for d in dic:
        meetTimeList = []
        for i in range(1, len(dic[d])):
            diff = dic[d][i] - dic[d][i-1]
            meetTimeList.append(diff) if diff <= 100 else -1
        if len(meetTimeList) > 0:
            avg = mean(meetTimeList)
            totalAvg.append(avg)
            # print(avg)
    print(mean(totalAvg))
    
def shift(dic):

    for key in dic.keys():
        cnt = 0
        Sum = 0

        for i in range(1, len(dic[key])):
            if dic[key][i] - dic[key][i - 1] < 100:
                Sum += dic[key][i] - dic[key][i - 1]
                cnt += 1
        
        if cnt == 0:
            return
        
        shift_val = dic[key][0] - int(Sum / cnt)
        for t in range(len(dic[key])):
            dic[key][t] -= shift_val

        dic[key] = dic[key][0: min(100, len(dic[key]))]

def makeLog(date, dic_bus_ap, dic_bus_bus):
    with open("result/bus-ap-res/" + date + ".json", "w") as f:
        json.dump(dic_bus_ap, f, indent=4)
    
    with open("result/bus-bus-res/" + date + ".json", "w") as f:
        json.dump(dic_bus_bus, f, indent=4)

if __name__ == '__main__':
    print("bus-ap")
    #path = "/Users/enfyshsu/NTU/110-1/ITIV/FinalProject/mobicom-traces/bus-ap/"
    path = sys.argv[1]
    path_bus_ap = os.path.join(path, "bus-ap")
    path_bus_bus = os.path.join(path, "bus-bus")
    dates = os.listdir(path_bus_ap)
    cnt = {}
    for date in dates:
        dic_bus_ap = readData_bus_ap(path_bus_ap, date)
        dic_bus_bus = readData_bus_bus(path_bus_bus, date)
        
        shift(dic_bus_ap)
        shift(dic_bus_bus)

        #print(date)
        #print(dic_bus_ap)
        #print(dic_bus_bus)
        #countDiff(dic)
        #for key in dic.keys():
        #    print(key, dic[key])
        makeLog(date, dic_bus_ap, dic_bus_bus)

    #for key in cnt.keys():
    #    print(key, cnt[key])
