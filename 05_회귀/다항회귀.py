from sklearn.preprocessing import PolynomialFeatures
import numpy as np

X = np.arange(4).reshape(2,2)
print(X)
poly = PolynomialFeatures(degree=3)
poly_fitr = poly.fit(X).transform(X)
print(poly_fitr) 