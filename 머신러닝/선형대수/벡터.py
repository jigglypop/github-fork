import numpy as np
import matplotlib.pylab as plt

a = np.array([1, 2])
red = {'facecolor': 'red'}
# 벡터 길이
print(np.linalg.norm(a))
b = 2 * a
c = -a
plt.annotate('', xy=b, xytext=(0, 0), arrowprops=red)
plt.show()
print(c)
