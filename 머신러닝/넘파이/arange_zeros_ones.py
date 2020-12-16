import numpy as np

sequence_array = np.arange(10)
print(sequence_array)
print(sequence_array.dtype, sequence_array.shape)

zero_array = np.zeros((3, 2), dtype='int32')
print(zero_array)
print(zero_array.dtype, zero_array.shape)
ones_array = np.ones((3, 2))
print(ones_array)
print(ones_array.dtype, ones_array.shape)
