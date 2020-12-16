import math
import os
import random
import re
import sys
from pprint import pprint


class Solution:
    # goods가 3개밖에 존재하지 않으므로 순서를 모두 직접 고려하는 것이 빠름
    def solution(self, goods):
        N = len(goods)
        results = [
            # 1개
            [goods[0], goods[1], goods[2]],
            # 3개
            [goods[0] + goods[1] + goods[2]],
            # 2개
            [goods[0] + goods[1], goods[2]],
            [goods[0], goods[1] + goods[2]],
            [goods[1], goods[0] + goods[2]],
        ]
        Min = sys.maxsize
        for result in results:
            temp = 0
            for r in result:
                if r >= 50:
                    r -= 10
                temp += r
            Min = min(temp, Min)
        return Min


solution = Solution()
print(solution.solution([5, 31, 15]))
