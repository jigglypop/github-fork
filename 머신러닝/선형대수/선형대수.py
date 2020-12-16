import numpy as np
# 행렬곱


def dot(A, B):
    xA = len(A[0])
    yA = len(A)
    xB = len(B[0])
    yB = len(B)
    if xA == 0 or yA == 0 or xB == 0 or yB == 0 or yB != xA:
        return False
    C = [[0] * yA for _ in range(xB)]
    for y in range(xB):
        for x in range(yA):
            for k in range(yB):
                C[y][x] += A[y][k] * B[k][x]
    return C

# 전치행렬


def transpose(A):
    X = len(A[0])
    Y = len(A)
    B = [[0] * Y for _ in range(X)]
    for y in range(Y):
        for x in range(X):
            B[x][y] = A[y][x]
    return B

# 더하기


def plus(A, B):
    X = len(A[0])
    Y = len(A)
    C = [[0] * Y for _ in range(X)]
    for y in range(Y):
        for x in range(X):
            C[y][x] = A[y][x] + B[y][x]
    return C


A = [[1, 2, 3],
     [4, 5, 6]]

B = [[1, 2],
     [3, 4],
     [5, 6]]
C = dot(A, B)
An = np.array([
    [1, 2, 3],
    [4, 5, 6]])
Bn = np.array([
    [1, 2],
    [3, 4],
    [5, 6]])
Cn = np.dot(A, B)
Dn = np.transpose(An)
D = transpose(A)
print(D)
print(Dn)
