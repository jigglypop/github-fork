import math
import os
import random
import re
import sys
from pprint import pprint
from collections import deque

# 수학

# def fibonacci(n):
#     DP[0] = 0
#     DP[1] = 1
#     for i in range(2, n+1):
#         DP[i] = DP[i-1] + DP[i-2]


# n = int(input())
# DP = [-1] * (n+1)
# fibonacci(n)
# print(DP[n])

# N = int(input())
# S = [0] + list(map(int, input().split()))
# DP = [0] * (N+1)
# DP[1] = 1
# for i in range(2, N+1):
#     for j in range(1, i):
#         if S[i] > S[j]:
#             DP[i] = max(DP[j], DP[i])
#     DP[i] += 1
# print(max(DP))

# import sys
# sys.setrecursionlimit(2000*2000)


# def fibonacci(n):
#     if n == 0:
#         return 0
#     if n == 1:
#         return 1
#     if DP[n] != -1:
#         return DP[n]
#     DP[n] = fibonacci(n-1) + fibonacci(n-2)
#     return DP[n]


# n = int(input())
# DP = [-1] * (n+1)
# fibonacci(n)
# print(DP[n])

# 배열회전

# def diagonal(arr):
#     N, M = len(arr), len(arr[0])
#     for diag in range(0, N + M - 1):
#         x = 0 if diag < M else (diag - M + 1)
#         y = diag if diag < M else M - 1
#         while x < N and y >= 0:
#             print('%2d ' % arr[x][y], end='')
#             x += 1
#             y -= 1
#         print()

# 지그재그

# def zigzag(arr):
#     N, M = len(arr), len(arr[0])
#     for i in range(N):
#         if i & 1 == 0:
#             for j in range(M):
#                 print('%2d ' % arr[i][j], end='')
#         else:
#             for j in range(M - 1, -1, -1):
#                 print('%2d ' % arr[i][j], end='')
#         print()


# spiral

# def spiral(arr):
#     X = len(arr[0])
#     Y = len(arr)
#     arr = [[0 for _ in range(X)] for _ in range(Y)]
#     y_start = x_start = 0
#     y_end, x_end = Y - 1, X - 1
#     cnt = 0
#     while y_start <= y_end and x_start <= x_end:
#         i = x_start
#         while i <= x_end:
#             cnt += 1
#             arr[y_start][i] = cnt
#             i += 1
#         y_start += 1
#         i = y_start
#         while i <= y_end:
#             cnt += 1
#             arr[i][x_end] = cnt
#             i += 1
#         x_end -= 1
#         i = x_end
#         while i >= x_start:
#             cnt += 1
#             arr[y_end][i] = cnt
#             i -= 1
#         y_end -= 1
#         i = y_end
#         while i >= y_start:
#             cnt += 1
#             arr[i][x_start] = cnt
#             i -= 1
#         x_start += 1

#     for i in range(Y):
#         for j in range(X):
#             print("%2d " % arr[i][j], end="")
#         print()

# 정규표현식

# text = 'name=yeomdonghwan, gender=male, major=ml'
# text1 = re.sub('[a-z]+=', '', text)
# print(re.split(', ', text1))

# 역행렬

# def inverse(m, size):
#     a = 0
#     det = 1
#     k = 0
#     inv = [[1 if x == y else 0 for x in range(size)] for y in range(size)]
#     while k < len(m):
#         if m[k][k] == 0:
#             m = m[k+1:len(m)] + m[k:k+1]
#             inv = inv[k+1:len(inv)] + inv[k:k+1]
#             continue
#         else:
#             if m[k][k] == 1:
#                 for i in range(k+1, len(m)):
#                     a = -m[i][k]
#                     for j in range(len(m)):
#                         if a == 0:
#                             break
#                         m[i][j] = a*m[k][j]+m[i][j]
#                         inv[i][j] = a*inv[k][j]+inv[i][j]
#             else:
#                 a = 1/m[k][k]
#                 for i in range(len(m)):
#                     m[k][i] = m[k][i]*a
#                     inv[k][i] = inv[k][i]*a

#                 for i in range(k+1, len(m)):
#                     a = -m[i][k]
#                     for j in range(len(m)):
#                         if a == 0:
#                             break
#                         m[i][j] = a*m[k][j]+m[i][j]
#                         inv[i][j] = a*inv[k][j]+inv[i][j]
#         k = k+1
#     for i in range(len(m)):
#         det *= m[i][i]
#     if det == 0:
#         return False
#     else:
#         for k in range(len(m)-1, -1, -1):
#             for i in range(k-1, -1, -1):
#                 a = -m[i][k]
#                 for j in range(len(m)-1, -1, -1):
#                     if a == 0:
#                         break
#                     m[i][j] = a * m[k][j] + m[i][j]
#                     inv[i][j] = a * inv[k][j] + inv[i][j]
#         return inv

# 행렬곱

# def dot(A, B):
#     xA = len(A[0])
#     yA = len(A)
#     xB = len(B[0])
#     yB = len(B)
#     if xA == 0 or yA == 0 or xB == 0 or yB == 0 or yB != xA:
#         return False
#     C = [[0] * yA for _ in range(xB)]
#     for y in range(xB):
#         for x in range(yA):
#             for k in range(yB):
#                 C[y][x] += A[y][k] * B[k][x]
#     return C

# 전치행렬

# def transpose(A):
#     X = len(A[0])
#     Y = len(A)
#     B = [[0] * Y for _ in range(X)]
#     for y in range(Y):
#         for x in range(X):
#             B[x][y] = A[y][x]
#     return B

# 더하기

# def plus(A, B):
#     X = len(A[0])
#     Y = len(A)
#     C = [[0] * Y for _ in range(X)]
#     for y in range(Y):
#         for x in range(X):
#             C[y][x] = A[y][x] + B[y][x]
#     return C

# 회전
# def rotate(arr, d):
#     N = len(arr)
#     temp = [[0] * N for _ in range(N)]
#     if d % 4 == 1:
#         for y in range(N):
#             for x in range(N):
#                 temp[x][N-1-y] = arr[y][x]
#     elif d % 4 == 2:
#         for y in range(N):
#             for x in range(N):
#                 temp[N-1-x][N-1-y] = arr[y][x]
#     elif d % 4 == 3:
#         for y in range(N):
#             for x in range(N):
#                 temp[N-1-x][y] = arr[y][x]
#     else:
#         for y in range(N):
#             for x in range(N):
#                 temp[y][x] = arr[y][x]
#     return temp


import math


class SigmoidNeuron:

    def __init__(self):
        self.w = None
        self.b = None

    def sums(self, x):
        Sum = 0
        for i in range(len(self.w)):
            Sum += self.w[i] * x
        return Sum

    def Exp(self, x):
        return 1 / (1 + math.exp(-x))

    def forpass(self, x):
        z = self.sums(x) + self.b
        return z

    def backprop(self, x, err):
        dw = x * err
        db = 1 * err
        return dw, db

    def activation(self, z):
        a = 1 / (1 + self.Exp(z))
        return a

    def fit(self, x, y, label, epochs=10):
        self.w = [1 for _ in range(len(x))]
        self.b = 0
        for j in range(epochs):
            for nx, ny, nz in zip(x, y, label):
                sx = (nx ** 2 + ny ** 2) ** 0.5
                z = self.forpass(sx)
                a = self.activation(z)
                err = -(nz - a)
                dw, db = self.backprop(nz, err)
                for i in range(len(x)):
                    self.w[i] -= abs(dw)
                print(f'---{j}---')
                print(self.w)
                self.b -= db

    def predict(self, x, y):
        sx = (x ** 2 + y ** 2) ** 0.5
        z = self.forpass(sx)
        print(z)
        a = self.activation(z)
        print(a)
        return a > 0.5


sys.stdin = open('배열.txt', 'r')

N = int(input())
train_x = []
train_y = []
train_label = []
for _ in range(N):
    a, b, c = map(float, input().split())
    train_x.append(a)
    train_y.append(b)
    train_label.append(c)
    print(a, b, c)
sigmoidneuron = SigmoidNeuron()
sigmoidneuron.fit(train_x, train_y, train_label)
M = int(input())
for _ in range(M):
    y, x = map(float, input().split())
    print(int(sigmoidneuron.predict(y, x)))
