import math
import os
import random
import re
import sys
from pprint import pprint
from collections import deque


arr = 'ABC'
result = []

# 패턴 추출
# text = "My favorite numbers are 19 and 43 and 123455"
# # ['19', '43', '123455']
# num = re.findall('[0-9]+', text)
# # ['My', 'favorite', 'numbers', 'are', 'and', 'and']
# string = re.findall('[a-zA-Z]+', text)

# 탐욕 패턴찾기
# text = "From: Using the: character"
# # ['From: Using the:']
# string1 = re.findall('^F.+:', text)
# # ['From:']
# string2 = re.findall('^F.+?:', text)

# 숫자 찾기
# text = "문의사항이 있으면 032-232-3245 으로 연락주시기 바랍니다"
# # ['032-232-324']
# string = re.findall(r'\d{3}-\d{3}-\d{3}', text)

# 공백 아닌 문자 찾기
# text = "From chlgmltn101@naver.com Sat Jan  5 09:14:16 2019"

# # ['chlgmltn101@naver.com']
# string1 = re.findall('\S+@\S+', text)

# 소괄호
# text = "From chlgmltn101@naver.com Sat Jan  5 09:14:16 2019"

# # ['chlgmltn101@naver.com']
# string2 = re.findall('From (\S+@\S+)', text)

# 이메일 호스트 출력

# text = "From chlgmltn101@naver.com Sat Jan  5 09:14:16 2019"
# # ['naver.com']
# string3 = re.findall('@([^ ]+)', text)


# 지정된 문자열이 포함되는지 판단하기

# * `^` : 문자열이 맨 앞에 오는지
# * `$` : 문자열이 맨 뒤에 오는지

# r1 = re.findall("^Hello", "Hello,world")
# r2 = re.findall("^Hello", "hi,Hello,world")
# r3 = re.findall("world$", "Hello, world")

# 문자열이 하나라도 포함되는지
# * `|` : 문자열이 하나라도 포함되는지

# r1 = re.findall("hello|world", "hello")


# 범위 판단하기
# * `*` : 문자(숫자)가 0개 이상인지
# * `+` : 문자(숫자)가 1개 이상인지

# r1 = re.findall('[0-9]+', '1234')
# r2 = re.findall('[0-9]*', '1234')
# r3 = re.findall('[0-9]*', 'abcd')

# 문자가 한 개만 있는지 판단하기
# * `?` : 문자가 0개 또는 1개인지
# * `.` : 문자가 1개인지

# r1 = re.findall('H?', 'H')
# r2 = re.findall('H?', 'Hi')
# r3 = re.findall('H.', 'Hi')


# 문자 개수 판단하기
# * `문자{개수}`: "문자"가 "개수"만큼 있는지
# * `문자열{개수}`: "문자열"이 "개수"만큼 있는지
# * `[0-9]{개수}`: "숫자"기 "개수"만큼 있는지

# r1 = re.findall('h{3}', 'hhhello')
# r2 = re.findall('(hello){3}', 'hellohellohello')
# r3 = re.findall('[0-9]{3}-[0-9]{3}-[0-9]{4}', '010-101-0101')

# 숫자와 영문 문자를 조합해서 판단하기
# * `a-z`: 소문자
# * `A-Z`: 대문자
# * `가-힣`: 한글

# r1 = re.findall('[a-zA-Z0-9]+', 'Hello1234')
# r2 = re.findall('[A-Z0-9]+', 'hello')
# r3 = re.findall('[가-힣]+', '홍길동')


# 특정 문자 범위에 포함되지 않는지

# * `[^범위]*`
# * `[^범위]+`

# r1 = re.findall("[^A-Z]*", 'hello')
# r2 = re.findall("[^A-Z]+", 'hello')

# 특수 문자 판단하기

# * `\특수문자` :  특수 문자 판단
# * `\d` : 모든 숫자
# * `\D` : 숫자가 아닌 모든 문자
# * `\w` : 영문 대소문자, 숫자, 밑줄 문자
# * `\D` : 영문 대소문자, 숫자, 밑줄 문자가 아닌 모든 문자

# r1 = re.findall('\*+', "1 ** 2")
# r2 = re.findall('\d+', '1234')
# r3 = re.findall('\D+', '1234')
# r4 = re.findall('\D+', 'Hello')
# r5 = re.findall('\w+', 'Hello_1234')


# 공백 처리하기

# * `\s` : 공백,  \t, \n, \r, \f, \v 을 포함
# * `\S` : 공백을 제외하고 \t, \n, \r, \f, \v만 포함

# r1 = re.findall('[a-zA-Z0-9 ]+', "Hello 1234")
# r2 = re.findall('[a-zA-Z0-9\s]+', "Hello 1234")


# 그룹 사용하기

# * `(정규 표현식) (정규 표현식)`
# * `매치객체.group(숫자)` : 그룹에 해당하는 문자열(숫자)를 가져옴
# * `매치객체.groups()` : 그룹에 해당하는 문자열(숫자)을 튜플로 반환
# * `(?P<이름>정규표현식)` ->  `매치객체.group('그룹이름')`: 그룹에 이름을 지은 뒤 반환

# r1 = re.findall('([0-9]+) ([0-9]+)', '10 123')

# 문자열 바꾸기

# * `re.sub('패턴','바꿀 문자열','문자열',바꿀 횟수)`
# * `re.sub('패턴',교체함수,'문자열',바꿀 횟수)

# r1 = re.sub('apple|orange', 'fruit', 'apple box orange tree')


def oddNumbers(l, r):
    # Write your code here
    return [i for i in range(l, r+1) if i % 2 == 1]


print(oddNumbers(1, 8))
