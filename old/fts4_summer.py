import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from matplotlib import animation
from IPython import display
# from matplotlib.animation import FuncAnimation

def exponentialMovingAverage(sample, alpha, cur):
    if (sample>=0):
        cur = (sample * alpha) + ((1 - alpha) * cur);
    return cur

class logicalLink:
    def __init__(self, minimum, maximum, arrivaltime):
        self.minimum = minimum
        self.maximum = maximum
        self.arrivaltime = arrivaltime

        self.decision = maximum
        self.running = 0
        self.throughput = 0
        self.ema = 0
        self.prevDec = 0
        self.prevEMA = 0
        self.sumDec = 0
    def process(self, perChannel, t, alpha):
        self.prevDec = self.decision
        self.throughput = self.running*perChannel
        self.prevEMA = self.ema
        if(t==self.arrivaltime): #update ema value. if new, set as current throughput
            self.ema = self.throughput
        else:
            # self.ema = exponentialMovingAverage(self.throughput,alpha,self.prevEMA)
            self.ema = exponentialMovingAverage(self.throughput,alpha,self.prevEMA)
        self.decision = self.newDecision()
        self.enforceBounds() #makes sure n_i in [m_i,M_i]
        self.sumDec += self.decision
    def avgDec(self,t):
        return self.sumDec/(t-self.arrivaltime)

    def enforceBounds(self):
        if(self.decision>self.maximum):
            self.decision = self.maximum
        if(self.decision<self.minimum):
            self.decision = self.minimum
    def newDecision(self):  
        decision = self.decision
        if(increaseCond(self.ema, self.prevEMA)):
            decision += 1
        elif(f(self.ema)<f(self.prevEMA)): #this is to handle deteriorating throughput.
            decision -=1
        return decision
    def updateRunning(self,t):
        if(t>=self.arrivaltime):
            self.running = self.decision
    
    def __str__(self):
        return "decision: " + str(self.decision) + " throughput: " + str(round(self.throughput,5)) + " ema: " + str(round(self.ema,5))
        #+ "minimum: " + str(self.minimum) + " maximum: " + str(self.maximum)
        #+ " running: " + str(self.running)
def perChannel(n):
    # Set the slope so that when all nodes are at maximum, the total capacity is overLoad
    # s = (maxcapacity-overLoad)/(sum([link.maximum for link in llink])-maxNumChannels)
    s=10
    if(n<=maxNumChannels):
        val =  maxcapacity/n
    else:
        val = (maxcapacity - s*(n-maxNumChannels))/n
    if(val>0):
        return val
    return 0


def simulate(sim_length, printing, llink):
    global t,x,y,z,ax,dataSet,numDataPoints,fig
    num_links = len(llink) #number of links
    linkSave = [[] for i in range(num_links)]
    nummax = 0
    for t in range(sim_length):
        for link in llink: #figuring out which links are actually running.
            link.updateRunning(t)
        totalLinks = sum([llink[i].running for i in range(num_links)])#if t>=llink[i].arrivaltime
        allmax=True
        for i in range(num_links):
            llink[i].process(perChannel(totalLinks), t, alpha)
            # print("Link "+str(i+1)+": " + str(llink[i]))
            linkSave[i].append(llink[i].decision)
            if(llink[i].decision!=llink[i].maximum):
                allmax=False
        print([link.decision for link in llink], end=' ')
        print([link.throughput for link in llink], end=' ')
        print([link.ema for link in llink])

    print("----------\nFinal Five Decisions: ", end='')
    for d in range(5,1,-1):
        print([linkSave[i][sim_length-d] for i in range(num_links)],end='; ')
    print([linkSave[i][sim_length-1] for i in range(num_links)])        
    digits=2
    print("Average Decision: ",end='')
    print([round(link.avgDec(sim_length),digits) for link in llink],end=' ')
    print("with a total sum of: " + str(round(sum([link.avgDec(sim_length) for link in llink]),digits)))
    print("sum of ema: " + str(sum([link.ema for link in llink])) + "; maxCapacity: " + str(maxcapacity))
    print("----------")

    with open('output.txt', 'w') as file: #Printing to Output file
        for i in range(sim_length):
            for j in range(num_links):
                file.write(str(linkSave[j][i]) +" ")
            file.write("\n")


def increaseCond(ema, prevema):
    return (ema >= prevema)
    # return ema + 10**-3 > prevema
    # return ema>prevema
    # return g(self.ema)>g(self.prevEMA)

def g(x):
    return x
    # return math.floor(x)
def f(x):
    return round(math.log10(x))
    # return math.floor(math.log10(x+1)**3) #polylogs don't guarantee convergence to (max,max)    
    # return x
    # return math.floor(0.055*x)
    # return math.floor(math.sqrt(x))

def main():
    global maxcapacity,maxNumChannels,overLoad #for modelling the physical link capacity
    global alpha, sim_length, llink
    maxcapacity = 1000 #normal max
    maxNumChannels = 100 #pivot point
    overLoad = 10**-4 #capacity when all at max

    alpha = 0.1 #weight given to new throughput values in the ema
    sim_length = 1000
    llink = [logicalLink(0,110,0) , logicalLink(1,110,5)] #links

    simulate(sim_length,True, llink)
    # print("If the other guy has "+str(llink[1].maximum)+" connections. You can get:")
    # for num in range(31):
    #     print("with a "+str(num)+": " + str(str(num*perChannel(num+30))))

    # sim_length = 10**5
    # for c in range(100): #1,2,...,2048
    #     test = (c%10) * 10**(c//10)
    #     simulate(sim_length,test,False) 



if __name__ == "__main__":
    # print(exponentialMovingAverage(1,0.5,10))
    main()        
