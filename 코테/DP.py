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

def oddNumbers(l, r):
    # Write your code here
    return [i for i in range(l, r+1) if i % 2 == 1]


print(oddNumbers(1, 8))
