from twolinks import *
import random,math

def a(n): #objective function
	if(sum(n)==0):
		return 0
	# #Independent
	# return -sum([(i+1-n[i])**2 for i in range(len(n))])

	perchannel = 1000/sum(n)
	return sum([(i+1)*n[i]*perchannel for i in range(len(n))])

def noise(): #generate noise. values from [-1,0,1].
	p = 0.2
	seed = random.random()
	if(seed<p):
		return -1
	if(seed>1-p):
		return 1
	return 0
#Vector Operations:
def mult(a,b): #adding two vectors
	return [a[i]*b[i] for i in range(len(a))]
def add(a,b): #adding two vectors
	return [a[i]+b[i] for i in range(len(a))]
def sub(a,b): #subtracting two vectors
	return [a[i]-b[i] for i in range(len(a))]
def scale(l,v):
	return [l*x for x in v]
def mag(n):
	return math.sqrt(sum([x**2 for x in n]))
#Real to Int casting
def realToInt(x): #mapping reals to ints probabilistically.
	if(x>=0):
		if(random.random()<x-math.floor(x)):
			# print("ceil")
			return math.ceil(x)
		else:
			# print("floor")
			return math.floor(x)
	else: #x<0
		return -realToInt(-x)

def realToIntVector(n,scale): #mapping vector of reals to vector of ints
	return [realToInt(scale*x) for x in n]


def simulate(alpha,k):
	random.seed(12202004)
	n = [0 for i in range(k)]
	iterations = 50

	total = [0 for i in range(k)]
	ema = [0 for i in range(k)]
	ema2 = [0 for i in range(k)]
	regret = 0

	adam = False
	momentum = not adam
	for t in range(iterations):
		x = [i+noise() for i in n]
		magn = mag(sub(x,n))
		while(magn==0):
			x = [i+noise() for i in n]
			magn = mag(sub(x,n))

		regret += a(x)
		if(adam):
			rate = a(x)-a(n)
		if(momentum):
			rate = 0.1*(a(x)-a(n))
		# print("rate: ")
		# print(rate)
		# print("delta:")
		# print(sub(x,n))
		# print("step: ")
		# print(realToIntVector(sub(x,n), rate))
		step = realToIntVector(sub(x,n), rate) #change vector
		ema = add(scale(alpha,ema),scale(1-alpha,step))

		squared = mult(step,step)
		ema2 = add(scale(alpha,ema2),scale(1-alpha,squared))

		# totalsum = #(1-alpha)*(1+alpha+alph**2 + )
		#TODO normalise with^

		if(adam):
			n = add(n,1000*scale(1/mag(ema2),ema))
		if(momentum):
			n = [min(max(x,10),50) for x in realToIntVector(add(x,ema),1)]


		total = add(total,n)
		regret += a(n)
		print(n)
	print("average choice:")
	print(scale(1/iterations,total))
	print('avg regret:')
	print(regret/(2*iterations))
	print(2*iterations)
	return (regret/(2*iterations))

def searchOptimal(k):
	maxim = float('-inf')
	search = 20
	for i in range(search):
		print(i/search)
		val = simulate(i/search,k)
		if(val>maxim):
			maxim = val
			maxalpha = i/search
	return maxalpha

	print("optimal: " + str(maxalpha))
def main():
	# maxk = 20
	# vals = [0 for i in range(maxk)]
	# for k in range(1,maxk):
	# 	vals[k] = searchOptimal(k)
	# print(vals)

	simulate(0.1,10)

if __name__ == "__main__":
	main()
#[0, 0.95, 0.95, 0.7, 0.4, 0.9, 0.55, 0.4, 0.85, 0.7, 0.75, 0.55, 0.35, 0.4, 0.05, 0.3, 0.15, 0.65, 0.6, 0.8]

	#20: 0.85
	#25: 0.5
	#30: 0.35
	#40: 0.25
	#50: 0.25
