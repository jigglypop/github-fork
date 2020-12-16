import math
import os
import random
import re
import sys
from pprint import pprint
from collections import deque


# 핵심 소스코드의 설명을 주석으로 작성하면 평가에 큰 도움이 됩니다.
class Solution:
    def solution(self, votes):
        me = votes[0]
        another = votes[1:]
        if len(another) == 0:
            return 0
        result = 0
        while True:
            another.sort(reverse=True)
            if me <= another[0]:
                another[0] -= 1
                me += 1
                result += 1
            else:
                break
        return result


solution = Solution()
print(solution.solution([5, 7, 7]))
print(solution.solution([10, 10, 10, 10]))
print(solution.solution([1]))
print(solution.solution([5, 10, 7, 3, 8]))
print(solution.solution([100]))
