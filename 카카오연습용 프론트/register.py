import requests
import json
from pprint import pprint


def request(method, url, data, token, is_urlencoded=True):
    method = method.upper()
    if method not in ('GET', 'POST'):
        raise Exception('올바른 형식을 입력해 주세요')
    if method == 'GET':
        headers = {'Content-Type': 'application/json'}
        if token != '':
            headers['Authorization'] = f'Token {token}'
        res = requests.get(url=url, params=data, headers=headers)
    elif method == 'POST':
        headers = {}
        if token != '':
            headers['Authorization'] = f'Token {token}'
        if is_urlencoded is True:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            res = requests.post(
                url=url, data=json.dumps(data), headers=headers)
        else:
            headers['Content-Type'] = 'application/json'
            res = requests.post(
                url=url, data=json.dumps(data), headers=headers)

    dict_meta = {'status_code': res.status_code, 'ok': res.ok,
                 'encoding': res.encoding, 'Content-Type': res.headers['Content-Type']}
    if 'json' in str(res.headers['Content-Type']):
        return {**dict_meta, **res.json()}
    else:
        return {**dict_meta, **{'text': res.text}}


host = 'http://localhost:8000'

# GET으로 포스트 가져오기
route_get = "/api/posts"
get_url = host + route_get
res = request(method='GET', url=get_url, data={'': ''}, token='')
if res['ok'] == True:
    pprint(res)
else:
    print('오류')

# # POST로 로그인하기
# route_post = "/api/auth/login/"
# post_url = host + route_post
# data = {'username': 'ydh2244', 'password': '1127star'}
# res = request(method='POST', url=post_url, data=data, token='')
# if res['ok'] == True:
#     pprint(res)
# else:
#     print('오류')

# # post 보내기 + 토큰
# route_post = "/api/posts/"
# post_url = host + route_post
# data = {
#     "category": "board",
#     "content": "안녕하세요",
#     "title": "안녕하세요",
#     "username": "염동환",
#     "profileid": 1
# }
# token = 'd9f37c894c1ae9d18084249c367dd640e4ff4968e5f65f0d2473a61281610ff4'
# res = request(method='POST', url=post_url, data=data,
#               token=token, is_urlencoded=False)
# if res['ok'] == True:
#     pprint(res)
# else:
#     print('오류')

# # user 로그인 체크하기
# route_post = "/api/auth/user/"
# post_url = host + route_post
# data = {'username': 'ydh2244', 'password': '1127star'}
# token = 'd9f37c894c1ae9d18084249c367dd640e4ff4968e5f65f0d2473a61281610ff4'
# res = request(method='GET', url=post_url, data=data, token=token)
# if res['ok'] == True:
#     pprint(res)
# else:
#     pass
# route_post = "/api/auth/login/"
# post_url = host + route_post
# data = {'username': 'ydh2244', 'password': '1127star'}
# res = request(method='POST', url=post_url, data=data, token='')
# if res['ok'] == True:
#     pprint(res)
# else:
#     print('오류')
