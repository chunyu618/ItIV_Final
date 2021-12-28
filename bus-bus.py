import os, sys
from numpy import mean

def readData(path, date):
    dic = {}
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

def makeLog(date, dic):
    f = open("result/bus-bus-res/" + date + ".txt", "w")
    for d in dic:
        f.write(str(dic[d]) + "\n")

if __name__ == '__main__':
    print("bus-bus")
    path = sys.argv[1]
    files = os.listdir(path)
    for f in files:
        date = f
        dic = readData(path, date)
        for key in dic.keys():
            print(key, dic[key])
        #countDiff(dic)
        #makeLog(date, dic)
