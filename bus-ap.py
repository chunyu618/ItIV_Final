import os, sys
from numpy import mean
import json

def readData(path, date):
    encounteringTime = {}
    print(path, date)
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
        s = dic[key][0] - int(Sum / cnt)
        for t in range(len(dic[key])):
            dic[key][t] -= s

        dic[key] = dic[key][0: min(100, len(dic[key]))]

def makeLog(date, dic):
    with open("result/bus-ap-res/" + date + ".txt", "w") as f:
        json.dump(dic, f, indent=4)

if __name__ == '__main__':
    print("bus-ap")
    #path = "/Users/enfyshsu/NTU/110-1/ITIV/FinalProject/mobicom-traces/bus-ap/"
    path = sys.argv[1]
    files = os.listdir(path)
    cnt = {}
    for f in files:
        date = f
        dic = readData(path, date)
        shift(dic)
        countDiff(dic)
        #for key in dic.keys():
        #    print(key, dic[key])
        makeLog(date, dic)

    #for key in cnt.keys():
    #    print(key, cnt[key])
