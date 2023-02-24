def print_matrix(matrix):
    if(print_on):
        for row in matrix:
            print("[", end='')
            for number in row:
                print(f"{number:3.2f}", end=', ')
            print("]")
        print()

def printc(s):
    if(print_on):
        print(s)

def simplex_slack(coef_mat, bounds, payoffs):#conditions should be an mxn matrix,
    m = len(coef_mat) #number of rows
    n = len(coef_mat[0]) #number of columns

    #We start by creating the canonical simplex tableau.
    tableau = [[0 for _ in range(m+n+1)] for _ in range(m+1)]
    #There are six things we need to initalize, four of which are nonzero
    #1. We add the identity matrix for the slack variables (which is great 
    # because we don't need to work for our basic feasible solution!)
    for i in range(m):
        tableau[i][i] = 1
    #2. We add in the coefficients
    for i in range(m):
        for j in range(m):
            tableau[i][j+m] = coef_mat[i][j]
    #3. We add the bounds
    for i in range(m):
        tableau[i][m+n] = bounds[i]
    #4. We add the payoff
    for j in range(n):
        tableau[m][m+j] = payoffs[j]
    print_matrix(tableau)

    #Computation Phase
    # We track which column (variable) is the basis vector for each row
    basis = [i for i in range(m)] #basis[i] is the column which equals e_i
    #Now we can attempt pivots

    worked_last_time = True
    while(worked_last_time):
        printc("----new pivot round-----")
        print_matrix(tableau)
        worked_last_time = False
        pivoted_already = False

        for j in range(m+n+1): #Run through each column
            if(not pivoted_already and tableau[m][j]>0):
                #We have found a row with positive r_j -- a candidate.
                min_y = (10**100, -1)
                for i in range(m): #run down the column
                    if(tableau[i][j]>0):
                        y_ratio = tableau[i][m+n] / tableau[i][j]

                        if(y_ratio < min_y[0]):
                            # print((y_ratio, i))
                            min_y = (y_ratio, i)
                printc(min_y) #Minimum leap
                # We may now pivot about tableau[index][j] where index = min_y[0]
                if(min_y[1] != -1):
                    #Bookkeeping
                    pivoted_already = True
                    worked_last_time = True

                    #Variable Calculation
                    index = min_y[1]
                    basis[index] = j
                    val = tableau[index][j]
                    # print(f"index: {index}, val: {val}, j: {j}")
                    for i in range(m+n+1):
                        tableau[index][i] /= val # everyone divides by val
                    print_matrix(tableau)
                    
                    for i in range(m+1): #For each row, we do a row reduction
                        if(i != index):
                            multiplier = tableau[i][j]
                            for j_alt in range(m+n+1):
                                # print(f"{tableau[i][j_alt]} -= {tableau[index][j_alt]: .3f} * {multiplier :.3f}")
                                tableau[i][j_alt] -= tableau[index][j_alt] * multiplier
                    print_matrix(tableau)
        
        printc(basis)
    
    final_sol = [0 for i in range(m)]
    
    for i in range(m):
        if(basis[i]>=m):
            final_sol[basis[i]-m] = tableau[i][m+n]
    printc(final_sol)
    return final_sol


print_on = False
def main():
    conditions = [[3,4,0],
                  [2,0,10],
                  [0,5,7]]
    # conditions = [[1,1,0],
    #               [1,0,1],
    #               [0,1,1]]    
    print(simplex_slack(conditions, [3,5,7], [1,1,1]))

if __name__ == "__main__":
    main()


