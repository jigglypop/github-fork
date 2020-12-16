import math
import os
import random
import re
import sys
from pprint import pprint
from collections import deque

# 수학

# N, M = map(int, input().split())


# def gcd(a, b):
#     if b == 0:
#         return a
#     else:
#         return gcd(b, a % b)


# g = gcd(N, M)
# l = g * (M // g) * (N // g)
# print(str(g) + "\n" + str(l))

# import sys
# sys.stdin = open("1373.txt", "r")
# input = sys.stdin.readline

# s = input()
# n = len(s)
# ans = ''
# if n % 3 == 1:
#     print(s[0], end='')
# elif n % 3 == 2:
#     print((ord(s[0])-ord('0'))*2 + ord(s[1])-ord('0'), end='')
# for i in range(n % 3, n, 3):
#     print((ord(s[i])-ord('0'))*4 + (ord(s[i+1])-ord('0'))
#           * 2 + (ord(s[i+2])-ord('0')), end='')


# import sys
# sys.stdin = open("1978.txt", "r")
# input = sys.stdin.readline

# N = int(input())
# nums = list(map(int, input().split()))

# def isPrime(a):
#     if a < 2:
#         return False
#     for i in range(2, int(a ** 0.5)+1):
#         if a % i == 0:
#             return False
#     return True

# count = 0
# for num in nums:
#     if isPrime(num):
#         count += 1
# print(count)

# 에라토스테네스

# import sys
# sys.stdin = open("1929.txt", "r")
# input = sys.stdin.readline

# MAX = 1000001
# check = [0] * MAX
# check[0] = check[1] = True

# for i in range(2, MAX):
#     if not check[i]:
#         j = i+i
#         while j < MAX:
#             check[j] = True
#             j += i
# m, n = map(int, input().split())
# for i in range(m, n+1):
#     if check[i] == False:
#         print(i)

# 나머지

# a, b, c = map(int, input().split())
# print((a % c+b % c) % c)
# print((a % c+b % c) % c)
# print((a % c*b % c) % c)
# print((a % c*b % c) % c)


def oddNumbers(l, r):
    # Write your code here
    return [i for i in range(l, r+1) if i % 2 == 1]


print(oddNumbers(1, 8))
