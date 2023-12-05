def matmul(m1, m2):
    # Mismatched axes result in ValueError
    if len(m1[0])!=len(m2):
        raise ValueError("The indices of matrices don't match for multiplication")
    # check if matrices are given
    try:
        iter(m1)
    except TypeError:
        raise TypeError("Given objects are not matrices")
    try:
        iter(m2)
    except TypeError:
        raise TypeError("Given objects are not matrices")
    # check if each is a valid matrix
    for i in m1:
        try:
            iter(i)
        except TypeError:
            raise TypeError("The matrices given are not row-wise iterable")
    for i in m2:
        try:
            iter(i)
        except TypeError:
            raise TypeError("The matrices given are not row-wise iterable")
    # check if all inputs are numeric 
    for i in m1:
        for j in i:
            if not (isinstance(j, int) or isinstance(j, float)):
                raise TypeError("Non Numeric input present in matrices")             
    for i in m2:
        for j in i:
            if not (isinstance(j, int) or isinstance(j, float)):
                raise TypeError("Non Numeric input present in matrices")
    # finding the resultant matrix by multiplying elements from a row of first matrix with elements from column of second matrix
    l=[[0 for j in range(len(m2[0]))] for i in range(len(m1))]
    for i in range(len(m1)):
        for k in range(len(m2[0])):
            for j in range(len(m1[0])):
                l[i][k]+=m1[i][j]*m2[j][k]
            
    return l

