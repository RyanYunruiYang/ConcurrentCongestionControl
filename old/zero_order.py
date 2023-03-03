# Transferred from FTS/

import random

def tputPerConnection(n):
    if(n==0):
        return 0
    return min(max(0, 1350-10*n),1000) /n

def main():
    m = 10 #number of agents
    weightedTputs = [[0] for i in range(m)]
    # increased = [True for i in range(m)]
    prevDelta = [0 for i in range(m)]
    decisions = [0 for i in range(m)]

    simlength = 20
    for t in range(simlength):
        if(t==0):
            decisions = [1 for i in range(m)]
            prevDelta = [1 for i in range(m)]
        else:
            for i in range(m):
                if(weightedTputs[i][t]>weightedTputs[i][t-1]):
                    decisions[i] += prevDelta[i]
                elif(weightedTputs[i][t]<weightedTputs[i][t-1]):
                    decisions[i] -= prevDelta[i]
                    prevDelta[i] *= -1
                else:
                    if(prevDelta[i]==1):
                        decisions[i] += prevDelta[i]
                    else:
                        decisions[i] -= prevDelta[i]
                        prevDelta[i] *=-1


        tputs = [x * tputPerConnection(sum(decisions)) for x in decisions]
        print(t)
        print(decisions)
        print(tputs)
        for i in range(m):
            pwe = 0.3
            weightedTputs[i].append(pwe*tputs[i] + (1-pwe) * sum(tputs)/m)



if __name__ == "__main__":
    main()
