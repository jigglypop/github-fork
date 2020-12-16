import numpy as np

array1 = np.array([1, 2, 3])
print(type(array1))
print(array1.shape, array1.ndim)
array2 = np.array([
    [1, 2, 3],
    [1, 2, 3]
])
print(array2.shape, array2.ndim)
array3 = np.array([[1, 2, 3]])
print(array3.shape, array3.ndim)
