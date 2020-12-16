import math
import os
import random
import re
import sys
from pprint import pprint
from collections import deque


arr = 'ABC'
result = []

# 배열조작

# board = [[1, 2, 3],
#          [4, 5, 6],
#          [7, 8, 9]]
# y = 1
# x = 1
# #  -1,-1   -1, 0    -1,1
# #   0,-1    0, 0     0,1
# #   1,-1    1, 0     1,1
# di = [(-1, -1), (-1, 0), (-1, 1),
#       (0, -1), (0, 0), (0, 1),
#       (1, -1), (1, 0), (1, 1)]
# # 북서 -1, -1
# ny, nx = y + di[0][0], x + di[0][1]
# print(board[ny][nx])
# # 위 -1, 0
# ny, nx = y + di[1][0], x + di[1][1]
# print(board[ny][nx])
# # 북동 -1, 1
# ny, nx = y + di[2][0], x + di[2][1]
# print(board[ny][nx])
# # 서 0, -1
# ny, nx = y + di[3][0], x + di[3][1]
# print(board[ny][nx])
# # 가운데 0, 0
# ny, nx = y + di[4][0], x + di[4][1]
# print(board[ny][nx])
# # 동 0, 1
# ny, nx = y + di[5][0], x + di[5][1]
# print(board[ny][nx])
# # 남서 1, -1
# ny, nx = y + di[6][0], x + di[6][1]
# print(board[ny][nx])
# # 아래 1, 0
# ny, nx = y + di[7][0], x + di[7][1]
# print(board[ny][nx])
# # 남동 1, 1
# ny, nx = y + di[8][0], x + di[8][1]
# print(board[ny][nx])


# 투포인터

# left = right = 0
# Sum = A[0]
# result = 0
# while left <= right and right < N:
#     if Sum < M:
#         right += 1
#         if right < N:
#             Sum += A[right]
#     elif Sum == M:
#         result += 1
#         right += 1
#         if right < N:
#             Sum += A[right]
#     elif Sum > M:
#         Sum -= A[left]
#         left += 1
#         if left > right and left < N:
#             right = left
#             Sum = A[left]

# 부분집합


# def subset(k):
#     N = len(arr)
#     for i in range(1 << N):
#         temp = []
#         for j in range(N):
#             if i & (1 << j):
#                 continue
#             temp.append(arr[j])
#         result.append(temp)


# 순열


# def perm(k, choice, used, r):
#     if k == r:
#         result.append(choice[::])
#         return
#     for i in range(len(arr)):
#         if used & (1 << i):
#             continue
#         choice.append(arr[i])
#         perm(k+1, choice, used | (1 << i))
#         choice.pop()


# 조합

# def comb(k, chosen, start, r):
#     if k == r:
#         result.append(chosen[::])
#         return
#     for i in range(start, len(arr)):
#         chosen.append(arr[i])
#         comb(k+1, chosen, i+1)
#         chosen.pop()

# nums = [1, 2, 3, 4, 4, 4, 5, 6, 7, 8]

# lower_bound

# start, end = 0, N-1
# result = 0
# while start <= end:
#     mid = (start + end) // 2
#     temp = nums[mid]
#     # 여기
#     if temp < M:
#         start = mid + 1
#     else:
#         # 여기
#         result = mid
#         end = mid - 1

# upper_bound

# start, end = 0, N-1
# result = 0
# while start <= end:
#     mid = (start + end) // 2
#     temp = nums[mid]
#     # 여기
#     if temp <= M:
#         start = mid + 1
#     else:
#         # 여기
#         result = mid
#         end = mid - 1

# 정수

# import math

# x, y, c = 30, 40, 10
# left, right = 0, min(x, y)
# while(abs(right-left) > 1e-6):
#     mid = (left+right)/2.0
#     d = mid
#     h1 = math.sqrt(x*x-d*d)
#     h2 = math.sqrt(y*y-d*d)
#     h = (h1*h2)/(h1+h2)
#     if h > c:
#         left = mid
#     else:
#         right = mid


# 모듈

# from bisect import bisect_left, bisect_right

# # 1 2 3 4 4 4 5 6 7 8
# print(bisect_left(nums, 4))
# print(bisect_right(nums, 4))



def oddNumbers(l, r):
    # Write your code here
    Q = deque()
    Q.append(1)
    print(Q)
    return [i for i in range(l, r+1) if i % 2 == 1]


print(oddNumbers(1, 8))
