import random

def best_delay(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload):
    rev = 0
    currTime = 0
    currIndex = 0
    currUtility = utility
    n = len(encounteringTime)

    while dataSize > 0 and currIndex < n and currUtility > 0:
        #print(currTime, dataSize, currUtility)
        if currTime <= encounteringTime[currIndex] and currTime + 1 > encounteringTime[currIndex]:
            # Download from the RSU
            t = timeToDownload
            while t > 0 and dataSize > 0 and currUtility > 0:
                rev += currUtility * min(B_r, dataSize)
                dataSize -= min(B_r, dataSize)
                rev += (currUtility - cost) * min(B_c, dataSize)
                dataSize -= min(B_c, dataSize)
                currUtility -= decay
                currTime += 1
                t -= 1

            currIndex += 1
        else:
            rev += (currUtility - cost) * min(B_c, dataSize)
            dataSize -= min(B_c, dataSize)
            currUtility -= decay
            currTime += 1

    #print("DataSize is ", dataSize)
    #print("Utility ", currUtility)
    print("Best delay currTime ", currTime)
    return rev if dataSize == 0 else -1   

def best_cost(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload):
    rev = 0
    currTime = 0
    currIndex = 0
    currUtility = utility
    n = len(encounteringTime)
    while dataSize > 0 and currIndex < n and currUtility > 0:
        if currTime <= encounteringTime[currIndex] and currTime + 1 > encounteringTime[currIndex]:
            #print(currTime, dataSize, currUtility)
            # Download from the RSU
            t = timeToDownload
            while t > 0 and dataSize > 0 and currUtility > 0:
                rev += currUtility * min(B_r, dataSize)
                dataSize -= min(B_r, dataSize)
                currTime += 1
                currUtility -= decay
                t -= 1

            currIndex += 1
            continue

        while currTime < n and currTime > encounteringTime[currIndex]:
            currIndex += 1;
            
        currUtility -= decay
        currTime += 1
    
    #print("DataSize is ", dataSize)
    #print("Utility ", currTime, currUtility, currIndex, dataSize)
    print("Best cost currTime ", currTime)
    return rev if dataSize == 0 else -1   

def cnt(dataSize, utility, B_r, B_c, decay, cost, encounteringTime, timeToDownload):
    rev = 0
    currTime = 0
    currIndex = 0
    currUtility = utility
    n = len(encounteringTime)
    T = (utility / decay) / (dataSize / (B_r * timeToDownload))
    tau = T
    m_bar = timeToDownload * B_r
    n_bar = dataSize / m_bar
    alpha = 0.8
    useCellular = False
    prevTime = 0
    
    if n_bar * decay * (T - m_bar / B_c) > 2 * cost - decay * T - 4 / 5 * pow(n_bar, 3/2) * tau:
        #print("To use cellular")
        useCellular = True
    while dataSize > 0 and currUtility > 0 and currIndex < n:
        if currTime <= encounteringTime[currIndex] and currTime + 1 > encounteringTime[currIndex]:
            #print(currTime, encounteringTime[currIndex])
            #print("Downloading...")

            # Update parameters
            T = alpha * (currTime - prevTime) + (1 - alpha) * T
            #print("Updated T ", T)
            prevTime = currTime
            # Make decision again
            if n_bar * decay * (T - m_bar / B_c) > 2 * cost - decay * T - 4 / 5 * pow(n_bar, 3/2) * tau:
                # use Cellular
                #print("Decide to use cellular at ", currTime)
                useCellular = True
            else:
                #print("Decide not to use cellulat at ", currTime)
                useCellular = False
            
            # Download from RSU
            t = timeToDownload
            while t > 0 and dataSize > 0 and currUtility > 0:
                rev += currUtility * min(B_r, dataSize)
                dataSize -= min(B_r, dataSize)
                if useCellular == True:
                    rev += currUtility * min(B_c, dataSize)
                    dataSize -= min(B_c, dataSize)
                    n_bar = dataSize / m_bar
                    if n_bar * decay * (T - m_bar / B_c) > 2 * cost - decay * T - 4 / 5 * pow(n_bar, 3/2) * tau:
                        #print("Decide to use cellular at ", currTime)
                        useCellular = True
                    else:
                        #print("Decide not to use cellulat at ", currTime)
                        useCellular = False
                currTime += 1
                currUtility -= decay
                t -= 1

            currIndex += 1
            continue
        elif useCellular == True:
            rev += (currUtility - cost) * min(B_c, dataSize)
            dataSize -= min(B_c, dataSize)
            n_bar = dataSize / m_bar
            if n_bar * decay * (T - m_bar / B_c) > 2 * cost - decay * T - 4 / 5 * pow(n_bar, 3/2) * tau:
                #print("Decide to use cellular at ", currTime)
                useCellular = True
            else:
                #print("Decide not to use cellulat at ", currTime)
                useCellular = False
                
        while currTime > encounteringTime[currIndex]:
            currIndex += 1;
        
        currUtility -= decay
        currTime += 1
    
    #print("Utility ", currUtility)
    #print("currTime", currTime)
    print("Proposed currTime ", currTime)
    return rev if dataSize == 0 else -1   
            
