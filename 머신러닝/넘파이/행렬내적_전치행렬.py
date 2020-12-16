import numpy as np

# 행렬내적
A = np.array([
    [1, 2, 3],
    [4, 5, 6]])

B = np.array([
    [7, 8],
    [9, 10],
    [11, 12]])
C = np.dot(A, B)
print(C)

# 전치행렬
D = np.array([
    [1, 2],
    [3, 4]])
E = np.transpose(D)
print(E)
