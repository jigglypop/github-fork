import math
import os
import random
import re
import sys
from pprint import pprint
from collections import deque

# 트리순회

# def num(x):
#     return ord(x)-64


# def word(x):
#     return chr(x+64)


# def preorder(x):
#     if x == -1:
#         return
#     print(word(x), end="")
#     preorder(tree[x][0])
#     preorder(tree[x][1])


# def inorder(x):
#     if x == -1:
#         return
#     inorder(tree[x][0])
#     print(word(x), end="")
#     inorder(tree[x][1])


# def postorder(x):
#     if x == -1:
#         return
#     postorder(tree[x][0])
#     postorder(tree[x][1])
#     print(word(x), end="")


# N = int(input())
# tree = [[-1, -1] for _ in range(N+1)]
# for _ in range(N):
#     a, b, c = map(str, input().split())
#     tree[num(a)][0] = -1 if b == '.' else num(b)
#     tree[num(a)][1] = -1 if c == '.' else num(c)
# preorder(1)
# print()
# inorder(1)
# print()
# postorder(1)

# LCA

# import sys
# from math import log2
# sys.setrecursionlimit(200000)
# sys.stdin = open("upper.txt", "r")
# input = sys.stdin.readline

# N = int(input())
# log = 20
# tree = [[] for _ in range(N+1)]
# for _ in range(N-1):
#     a, b = map(int, input().split())
#     tree[a].append(b)
#     tree[b].append(a)

# P = [[0] * (log+2) for i in range(N+1)]
# tin = [0 for _ in range(N+1)]
# tout = [0 for _ in range(N+1)]
# timer = 0


# def dfs(u, parent):
#     global timer
#     timer += 1
#     tin[u] = timer
#     P[u][0] = parent
#     for i in range(1, log+1):
#         P[u][i] = P[P[u][i-1]][i-1]
#     for v in tree[u]:
#         if v != parent:
#             dfs(v, u)
#     timer += 1
#     tout[u] = timer


# dfs(1, 1)


# def upper(u, v):
#     return tin[u] <= tin[v] and tout[u] >= tout[v]


# def LCA(u, v):
#     if upper(u, v):
#         return u
#     if upper(v, u):
#         return v
#     for i in range(log, -1, -1):
#         if not upper(P[u][i], v):
#             u = P[u][i]
#     return P[u][0]


# M = int(input())

# for _ in range(M):
#     a, b = map(int, input().split())
#     print(LCA(a, b))

# 펜윅 트리

# def update(tree, i, x):
#     while i < len(tree):
#         tree[i] += x
#         i += (i & -i)


# def sum(tree, i):
#     s = 0
#     while i > 0:
#         s += tree[i]
#         i -= (i & -i)
#     return s


# input = sys.stdin.readline
# n, m, k = map(int, input().split())

# tree = [0]*(n+1)
# board = [0]
# for i in range(1, n+1):
#     board.append(int(input()))
#     update(tree, i, board[i])
# for i in range(0, m+k):
#     q, a, b = map(int, input().split())
#     if q == 1:
#         update(tree, a, b-board[a])
#         board[a] = b
#     if q == 2:
#         print(sum(tree, b) - sum(tree, a-1))


# 세그먼트 트리

# # from math import ceil, log2
# input = sys.stdin.readline
# N, M = map(int, input().split())
# # size = (1 << (ceil(log2(N))+1))
# board = [int(input()) for _ in range(N)]
# tree = [0] * (4*N)


# def init(x, start, end):
#     if start == end:
#         tree[x] = board[end]
#     else:
#         init(2 * x, start, (start + end) // 2)
#         init(2 * x + 1, (start + end) // 2 + 1, end)
#         tree[x] = min(tree[x * 2], tree[x * 2 + 1])


# init(1, 0, N-1)


# def query(x, start, end, s, e):
#     if end < s or start > e:
#         return -1
#     if start >= s and end <= e:
#         return tree[x]
#     mid = (start + end) // 2
#     left = query(2 * x, start, mid, s, e)
#     right = query(2 * x + 1, mid + 1, end, s, e)
#     if left == -1:
#         return right
#     elif right == -1:
#         return left
#     else:
#         return min(left, right)


# for _ in range(M):
#     start, end = map(int, input().split())
#     print(query(1, 0, N-1, start-1, end-1))

# 트라이

# class Trie:
#     head = {}

#     def add(self, words):
#         _head = self.head
#         for word in words:
#             if word not in _head:
#                 _head[word] = {}
#             _head = _head[word]
#         _head['*'] = True

#     def search(self, words):
#         _head = self.head
#         for word in words:
#             if word not in _head:
#                 return False
#             _head = _head[word]
#         if '*' in _head:
#             return True
#         else:
#             return False

# 크루스칼

# V = int(input())
# E = int(input())
# parent = [i for i in range(V+1)]

# edges = []
# for _ in range(E):
#     a, b, cost = map(int, input().split())
#     edges.append((cost, a, b))
# edges.sort()
# result = 0

# def find(parent, x):
#     if parent[x] != x:
#         parent[x] = find(parent, parent[x])
#     return parent[x]

# def union(parent, a, b):
#     a = find(parent, a)
#     b = find(parent, b)
#     if a > b:
#         parent[b] = a
#     else:
#         parent[a] = b

# for edge in edges:
#     cost, a, b = edge
#     if find(parent, a) != find(parent, b):
#         union(parent, a, b)
#         result += cost

# 프림

# from collections import deque
# import heapq


# V, E = map(int, input().split())
# graph = [[] for _ in range(V+1)]
# visited = [False] * (V+1)

# for _ in range(E):
#     a, b, c = map(int, input().split())
#     graph[a].append((c, b))
#     graph[b].append((c, a))

# heap = []
# visited[1] = True
# result = 0
# cnt = 1
# for a in graph[1]:
#     heapq.heappush(heap, a)
# while heap:
#     cost, to = heapq.heappop(heap)
#     if not visited[to]:
#         visited[to] = True
#         cnt += 1
#         result += cost
#         for u in graph[to]:
#             heapq.heappush(heap, u)
#     if cnt == V:
#         break


def oddNumbers(l, r):
    # Write your code here
    return [i for i in range(l, r+1) if i % 2 == 1]


print(oddNumbers(1, 8))
