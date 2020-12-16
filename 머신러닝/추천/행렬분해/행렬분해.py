import numpy as np
from sklearn.metrics import mean_squared_error
R = np.array([
    [4, np.NaN, np.NaN, 2, np.NaN],
    [np.NaN, 5, np.NaN, 3, 1],
    [np.NaN, np.NaN, 3, 4, 4],
    [5, 2, 1, 2, np.NaN],
])
num_users, num_items = R.shape
K = 3
np.random.seed(1)
P = np.random.normal(scale=1./K, size=(num_users, K))
Q = np.random.normal(scale=1./K, size=(num_items, K))


def get_rmse(R, P, Q, non_zeros):
    error = 0
    P = np.dot(P, Q.T)
    X = [non_zero[0] for non_zero in non_zeros]
    Y = [non_zero[1] for non_zero in non_zeros]
    R = R[X, Y]
    P = P[X, Y]
    mse = mean_squared_error(R, P)
    rmse = np.sqrt(mse)
    return rmse


steps = 1000
Pi = 0.01
Lambda = 0.01
non_zeros = [(y, x, R[y, x]) for y in range(num_users)
             for x in range(num_items) if R[y, x] > 0]

for step in range(steps):
    for y, x, r in non_zeros:
        E = r - np.dot(P[y, :], Q[x, :].T)
        P[y, :] = P[y, :] + Pi*(E * Q[x, :] - Lambda * P[y, :])
        Q[x, :] = Q[x, :] + Pi*(E * P[y, :] - Lambda * Q[x, :])
        rmse = get_rmse(R, P, Q, non_zeros)
        if (step % 50) == 0:
            print(f'스텝 {step} : rmse : {rmse}')

pred_matrix = np.dot(P, Q.T)
print(pred_matrix)
