import pandas as pd
def print_matrix(matrix) -> None:
    df = pd.DataFrame(matrix)
    print(df)

def corner(a: list=[10,15,7,8], b: list=[8,6,9,12,5]) -> list:
	grid = [[0 for i in range(len(b))]for i in range(len(a))]

	curx = 0
	cury = 0
	# print_matrix(grid)

	while(curx+cury<len(a)+len(b)-1):
		xdebt = a[curx] - sum(grid[curx])
		ydebt = b[cury] - sum([grid[i][cury] for i in range(len(a))])

		print(f"xdebt: {xdebt}, ydebt: {ydebt}")
		if(ydebt < xdebt):
			grid[curx][cury] = ydebt
			cury+=1
		else:
			grid[curx][cury] = xdebt
			curx +=1 

		print((curx,cury))
		print_matrix(grid)

	# print(xdebt)
	# print(ydebt)

	return grid


def main():
	# a = [int(_) for _ in input().split()]
	# b = [int(_) for _ in input().split()]
	# corner(a,b)
	corner()

if __name__ == "__main__":
	main()
