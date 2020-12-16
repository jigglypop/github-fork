import math
import os
import random
import re
import sys
from pprint import pprint


class Solution:

    def check(self, page, not_broken, num_list):
        length = len(page)
        if length == 0:
            return "9999999"
        small = list(filter(lambda x: x in not_broken,
                            num_list[0: int(page[0])]))
        big = list(filter(lambda x: x in not_broken,
                          num_list[int(page[0]) + 1: 10]))

        a = small[-1] + not_broken[-1] * (length - 1) if len(small) else "9999999"
        b = page[0] if length == 1 and page[0] in not_broken else page[0] + self.check(page[1:], not_broken,
                       num_list) if page[0] in not_broken else "9999999"
        c = big[0] + not_broken[0] * (length - 1) if len(big) else "9999999"
        abcde = [a, b, c]
        if length == len(page):
            d = not_broken[-1] * (length - 1) if len(not_broken) and length >= 2 else "9999999"
            e = ((not_broken[0] if not_broken[0] != '0' else not_broken[1] if len(
                not_broken) > 1 else "9999999") + not_broken[0] * length) if len(not_broken) else "9999999"
            abcde += [d, e]
        abcde.sort(key=lambda x: len(x))
        abs_page = list(map(lambda x: abs(int(page) - int(x)), abcde))
        return str(abcde[abs_page.index(min(abs_page))])

    def solution(self, page, broken):
        broken = [str(word) for word in broken]
        num_list = list(map(str, range(10)))
        not_broken = list(filter(lambda x: x not in broken, num_list))
        near_num = self.check(str(page), not_broken, num_list)
        return min(abs(page - int(near_num)) + len(near_num), abs(100 - page))


solution = Solution()
print(solution.solution(5457, [6, 7, 8]))
print(solution.solution(100, [1, 0, 5]))
print(solution.solution(99999, [0, 2, 3, 4, 5, 6, 7, 8, 9]))
# print(solution.solution(158, [1, 9, 2, 5, 4]))
# print(solution.solution(151241, [0, 1, 2, 3, 4, 7, 8, 9]))
