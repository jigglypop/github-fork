import math
import os
import random
import re
import sys
from pprint import pprint


class Solution:
    def check(self, num, broken):
        for i in num:
            if i in broken:
                return False
        return True

    def solution(self, page, broken):
        result = abs(page - 100)
        broken = [str(word) for word in broken]
        for i in range(1000001):
            num = str(i)
            if self.check(num, broken):
                result = min(result, len(num) + abs(i - page))
        return result


solution = Solution()
print(solution.solution(5457, [6, 7, 8]))
print(solution.solution(100, [1, 0, 5]))
print(solution.solution(99999, [0, 2, 3, 4, 5, 6, 7, 8, 9]))
# print(solution.solution(158, [1, 9, 2, 5, 4]))
# print(solution.solution(151241, [0, 1, 2, 3, 4, 7, 8, 9]))
