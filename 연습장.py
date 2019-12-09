import numpy as np





# 행렬내적
A = np.array([[1,2,3],
              [4,5,6]])
B = np.array([[7,8],
              [9,10],
              [11,12]])
C = np.dot(A,B)
print(C)


# 전치행렬
arr = np.array([0,1,2,3,4,5,6,7,8,9,10,11])
arr2 = np.array([[0,1,2],[3,4,5],[6,7,8]])
arr2_ = np.transpose(arr2)
print(arr2_)