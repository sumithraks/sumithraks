# 1 == \ and 2 == /
def can_be_extended_to_solution(perm,matrix_size):
    #print("can_be_extended_to_solution")
    for k in range(len(perm)):
        #print("\ncurrent cell:",k)
        value=perm[k]
    
        # next cell
        if ( (k+1) % matrix_size > 0 and k+1 < len(perm)):
            #print("next cell:",k+1)
            if (value == 1 and perm[k+1]==2 or value == 2 and perm[k+1]==1):
                return False

        # prev cell
        if (k-1 >= 0 and k %matrix_size != 0):
            #print("prev cell:",k-1)
            if (value == 1 and perm[k-1]==2 or value == 2 and perm[k-1]==1):
                return False

        # top cell
        if (k - matrix_size >= 0 ):
            #print("top cell:",k-matrix_size)
            if (value == 1 and perm[k-matrix_size]==2 or value == 2 and perm[k-matrix_size]==1):
                return False

        # bottom cell
        if ( k + matrix_size < matrix_size * matrix_size and k + matrix_size < len(perm)):
            #print("bottom cell:",k+matrix_size)
            if (value == 1 and perm[k+matrix_size]==2 or value == 2 and perm[k+matrix_size]==1):
                return False

        # upper left cell
        if (k - matrix_size - 1 >= 0  and k % matrix_size !=0):
            #print("upper left cell:",k-matrix_size-1)
            if (value == 1 and perm[k- matrix_size - 1]==1): 
                return False

        # upper right cell
        if (k - matrix_size + 1 >= 0 and k%matrix_size != matrix_size-1 ):
            #print("upper right cell:",k-matrix_size+1)
            if (value == 2 and perm[k- matrix_size + 1]==2):
                return False

        # lower left cell
        if (k % matrix_size != 0 and k + matrix_size - 1 < matrix_size * matrix_size and  k + matrix_size - 1 < len(perm) ):
            #print("lower left cell:",k+matrix_size-1)
            if (value == 2 and perm[k+ matrix_size - 1 ]==2):
                return False

        # lower right cell
        if (k + matrix_size + 1 < matrix_size * matrix_size and k%matrix_size != matrix_size-1 and k + matrix_size + 1 < len(perm) ):
            #print("lower right cell:",k+matrix_size+1)
            if (value == 1 and perm[k+matrix_size + 1] == 1):
                return False
        
    return True


def extend(perm,num_diagnols,matrix_size):

    #print("*************")
    #print(perm)
    #print("*************")
    if num_diag(perm,num_diagnols):
        print("Solution")
        print(perm)
        exit()

    if (len(perm) >= matrix_size * matrix_size):
        #print("arr len:",len(perm))
        #print(perm)
        return
    for i in range(0,3):
        perm.append(i)
        if can_be_extended_to_solution(perm,matrix_size):
            ##print("possible extension")
            #print(perm)
            extend(perm,num_diagnols,matrix_size)
        perm.pop()
    return 

def num_diag(solution_vector,num_diagnols):
    # return number of / or \ diagonals present in the solution
    sum=0
    for x in solution_vector:
        if x>0:
            sum=sum+1
    if (sum==num_diagnols):
        return True;
    return False;

matrix_size=5
num_diagnols=16
perm=[]
extend(perm,num_diagnols,matrix_size)
