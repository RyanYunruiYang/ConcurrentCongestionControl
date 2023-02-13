import random

def printg():
	

def main():
	a,b = 2,3
	garden = [[0 for i in range(b)] for j in range(a)]

	min_x = random.randint(0, a-1)
	min_y = random.randint(0, b-1)

	garden[min_x][min_y] = 1
	neighbors = [(min_x,min_y),(min_x,min_y),(min_x,min_y),(min_x,min_y)]

	# while(True):
	printg()

	print(garden[min_x][min_y])

if __name__ == "__main__":
	main()