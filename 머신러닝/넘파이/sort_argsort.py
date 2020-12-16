import numpy as np

# sort
org_array = np.array([3, 1, 9, 5])
sort_array1 = np.sort(org_array)
print(org_array)
print(sort_array1)
# 내림차순
sort_array2 = np.sort(org_array)[::-1]
print(sort_array2)

# 2차원 이상 sort
array2D = np.array([
    [8, 12],
    [7, 1]])
sort_array2D_axis0 = np.sort(array2D, axis=0)
sort_array2D_axis1 = np.sort(array2D, axis=1)
print(array2D)
print(sort_array2D_axis0)
print(sort_array2D_axis1)

# 정렬된 행의 인덱스 반환
org_array = np.array([3, 1, 9, 5])
sort_indices = np.argsort(org_array)
print(type(sort_indices))
print(sort_indices)
