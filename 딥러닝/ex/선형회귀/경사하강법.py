from sklearn.datasets import load_diabetes
import matplotlib.pyplot as plt


class Neuron:
    def __init__(self):
        self.w = 1.0
        self.b = 1.0

    def forpass(self, x):
        _y = x * self.w + self.b
        return _y

    def backprop(self, x, err):
        dw = x * err
        db = 1 * err
        return dw, db

    def fit(self, x, y, epochs=100):
        for _ in range(epochs):
            for nx, ny in zip(x, y):
                _y = self.forpass(nx)
                err = -(ny - _y)
                dw, db = self.backprop(nx, err)
                self.w -= dw
                self.b -= db
            print('w: {}, b: {}'.format(self.w, self.b))


diabetes = load_diabetes()
x = diabetes.data[:, 2]
y = diabetes.target
neuron = Neuron()
neuron.fit(x, y)

plt.scatter(x, y)
pt1 = (-0.1, -0.1 * neuron.w + neuron.b)
pt2 = (0.15, 0.15 * neuron.w + neuron.b)
plt.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]])
plt.xlabel('x')
plt.ylabel('y')
plt.show()
