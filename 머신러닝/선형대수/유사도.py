import math
from scipy.spatial.distance import cosine
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


def sums(A, B):
    Y = len(A)
    Sum = 0
    try:
        X = len(A[0])
        for y in range(Y):
            for x in range(X):
                Sum += A[y][x] * B[y][x]
        return Sum
    except:
        for y in range(Y):
            Sum += A[y] * B[y]
        return Sum
    # if Y == 1:

    # else:


def cosine_similarity(a, b):
    return sum(ae * be for ae, be in zip(a, b)) / (math.sqrt(sum_of_square(a)) * math.sqrt(sum_of_square(b)))


def sum_of_square(x):
    return sum([e * e for e in x])


def Exp(arr):
    return [1 / (1 + math.exp(-i)) for i in arr]


a = np.array([1.00000000e-05,   1.00000000e+00,   2.00000000e+00,
              4.00000000e+00,   1.00000000e+01,   1.00000000e+02])

print(Exp([1.00000000e-05,   1.00000000e+00,   2.00000000e+00,
           4.00000000e+00,   1.00000000e+01,   1.00000000e+02]))
# print(cosine_similarity(a, b))
