#Taken from FTS/ folder

def tputPerConnection(n):
    if(n==0):
        return 0
    return min(max(0, 1350-10*n),1000) /n

def util(n):
    if(sum(n)==0):
        return 0
    else:
        # print(sum([x*tputPerConnection(sum(n)) for x in n]))
        # print(sum(n) * tputPerConnection(sum(n)))

        # return int(1000*sum([x*tputPerConnection(sum(n)) for x in n]))
        return sum(n) * tputPerConnection(sum(n))


def main():
    k=10
    n = [0 for i in range(k)]

    runtime = 100

    for t in range(runtime):
        for i in range(k):
            #checking increase
            curutil = util(n)
            n[i] +=1
            if(util(n) < curutil):
                #checking decrease
                n[i] -= 2
                if(util(n)<= curutil):
                    n[i]+=1

            n[i] = max(n[i],0)
        print(n)




if __name__ == "__main__":
    main()
