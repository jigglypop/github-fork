import math
import os
import random
import re
import sys
from pprint import pprint
from collections import deque

# DFS node

# graph = [[], [2, 3, 8], [1, 7], [1, 4, 5],
#          [3, 5], [3, 4], [7], [2, 6, 8], [1, 7]]


# def DFS(v, visited):
#     visited[v] = True
#     print(v, end=" ")
#     for i in graph[v]:
#         if not visited[i]:
#             DFS(i, visited)


# visited = [False] * 9

# DFS(1, visited)

# BFS node

# from collections import deque


# def BFS(graph, start, visited):
#     queue = deque([start])
#     visited[start] = True
#     while queue:
#         v = queue.popleft()
#         print(v, end=" ")
#         for i in graph[v]:
#             if not visited[i]:
#                 queue.append(i)
#                 visited[i] = True


# graph = [[], [2, 3, 8], [1, 7], [1, 4, 5],
#          [3, 5], [3, 4], [7], [2, 6, 8], [1, 7]]


# BFS

# Y, X = 4, 6
# board = [[1, 0, 1, 1, 1, 1], [1, 0, 1, 0, 1, 0],
#          [1, 0, 1, 0, 1, 1], [1, 1, 1, 0, 1, 1]]

# di = ((-1, 0), (1, 0), (0, -1), (0, 1))
# visited = [[0] * X for _ in range(Y)]


# def bfs():
#     Q = deque([(0, 0)])
#     visited[0][0] = 1
#     while Q:
#         y, x = Q.popleft()
#         if x == X-1 and y == Y-1:
#             print(visited[y][x])
#             return
#         for dy, dx in di:
#             nx = x + dx
#             ny = y + dy
#             if 0 <= nx < X and 0 <= ny < Y:
#                 if visited[ny][nx] > 0 or board[ny][nx] == 0:
#                     continue
#                 visited[ny][nx] = visited[y][x] + 1
#                 Q.append((ny, nx))


# bfs()

# dfs

# Y, X = 4, 6
# board = [[1, 0, 1, 1, 1, 1], [1, 0, 1, 0, 1, 0],
#          [1, 0, 1, 0, 1, 1], [1, 1, 1, 0, 1, 1]]

# di = ((-1, 0), (1, 0), (0, -1), (0, 1))
# visited = [[0] * X for _ in range(Y)]


# def dfs():
#     Q = deque([(0, 0)])
#     visited[0][0] = 1
#     while Q:
#         y, x = Q.pop()
#         if x == X-1 and y == Y-1:
#             print(visited[y][x])
#             return
#         for dy, dx in di:
#             nx = x + dx
#             ny = y + dy
#             if 0 <= nx < X and 0 <= ny < Y:
#                 if visited[ny][nx] > 0 or board[ny][nx] == 0:
#                     continue
#                 visited[ny][nx] = visited[y][x] + 1
#                 Q.append((ny, nx))


# dfs()

# 다익스트라

# from heapq import heappop, heappush
# import sys

# INF = sys.maxsize
# n, m = map(int, input().split())
# start = int(input())
# graph = [[] for _ in range(n+1)]
# for _ in range(m):
#     a, b, c = map(int, input().split())
#     graph[a].append([b, c])
#     graph[b].append([a, c])

# visited = [INF] * (n+1)


# def dijkstra(start):
#     heap = []
#     heappush(heap, (0, start))
#     visited[start] = 0
#     while heap:
#         w, u = heappop(heap)
#         if visited[u] < w:
#             continue
#         for v, dw in graph[u]:
#             if visited[v] > w + dw:
#                 visited[v] = w + dw
#                 heappush(heap, (w + dw, v))


# dijkstra(start)
# for i in range(1, n+1):
#     if visited[i] == INF:
#         print('INF')
#     else:
#         print(visited[i])

# 플로이드

# import sys
# INF = sys.maxsize
# N, M = map(int, input().split())
# graph = [[INF]*(N) for _ in range(N)]
# for _ in range(M):
#     a, b, c, = map(int, input().split())
#     graph[a-1][b-1] = c

# for y in range(N):
#     for x in range(N):
#         if y == x:
#             graph[y][x] = 0
# for z in range(N):
#     for y in range(N):
#         for x in range(N):
#             graph[y][x] = min(graph[y][x], graph[y][z] + graph[z][x])

# for g in graph:
#     print(*g)


# DAG

# from collections import deque
# N, M = map(int, input().split())
# graph = [[] for _ in range(N+1)]
# check = [0 for _ in range(N+1)]
# for i in range(M):
#     a, b = map(int, input().split())
#     graph[a].append(b)
#     check[b] += 1
# Q = deque()
# for i in range(1, N+1):
#     if check[i] == 0:
#         Q.append(i)
# while Q:
#     u = Q.popleft()
#     for v in graph[u]:
#         check[v] -= 1
#         if check[v] == 0:
#             Q.append(v)
#     print(u, end=" ")

from collections import deque


class Solution:

    def solution(self, n):
        Q = deque([1, 2, 3, 4, 5])
        Q.rotate(2)
        print(Q)
        return n


solution = Solution()
print(solution.solution(2))
