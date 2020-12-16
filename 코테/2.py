import math
import os
import random
import re
import sys
from pprint import pprint
from collections import Counter

Min = sys.maxsize


class Solution:
    def go(self, count_alpha, n):
        global Min
        temp = []
        for count in count_alpha:
            if count == 0 or count == -1:
                continue
            temp.append(count)
        if len(temp) == 0:
            Min = min(Min, 0)
        else:
            Min = min(Min, max(temp) - min(temp))

        for i in range(1, n+1):
            for j in range(26):
                if count_alpha[j] == -1:
                    continue
                if count_alpha[j] >= i:
                    count_alpha[j] -= i
                    self.go(count_alpha, n - i)
                    count_alpha[j] += i

    def solution(self, s, n):
        global Min
        count_alpha = [-1] * 26
        for i in s:
            if count_alpha[ord(i) - 97] == -1:
                count_alpha[ord(i) - 97] = 0
            count_alpha[ord(i) - 97] += 1
        self.go(count_alpha, n)
        temp = []
        for count in count_alpha:
            if count == 0 or count == -1:
                continue
            temp.append(count)
        zero = max(temp) - min(temp)
        Min = min(zero, Min)
        return Min


solution = Solution()
print(solution.solution("a", 1))
# print(solution.solution("aaaabbbbc", 5))
