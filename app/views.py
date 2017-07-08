# -*- coding: utf-8 -*-
from flask import jsonify, make_response, request
from app import app, data, calc
import urllib.request, urllib.parse
import json
import base64, time


# import datetime, time
# import hmac, base64, urllib.request
# from hashlib import sha1

@app.route('/api/reg', methods=["GET", "POST"])
def register():
    datam = json.loads((request.get_data()).decode(encoding="utf-8"))
    username = datam['username']
    password = datam['password']
    if (username == ""):
        result = {
            "error": "缺少用户名"
        }
        return jsonify(result), 400
    elif (password == ""):
        result = {
            "error": "缺少密码"
        }
        return jsonify(result), 400
    else:
        result = data.register(username, password)
        if (result):
            response = make_response("")
            response.set_cookie('username', username)
            return response
        else:
            result = {
                "error": "用户名已占用"
            }
            return jsonify(result), 400


@app.route('/api/login', methods=["GET", "POST"])
def login():
    datam = json.loads((request.get_data()).decode(encoding="utf-8"))
    username = datam['username']
    password = datam['password']
    if (username == ""):
        result = {
            "error": "缺少用户名"
        }
        return jsonify(result), 400
    elif (password == ""):
        result = {
            "error": "缺少密码"
        }
        return jsonify(result), 400
    else:
        result = data.login(username, password)
        if (result == 1):
            response = make_response("")
            response.set_cookie('username', username)
            response.set_cookie('password', password)
            return response
        elif (result == -1):
            result = {
                "error": "用户名不存在"
            }
            return jsonify(result), 400
        else:
            result = {
                "error": "密码错误"
            }
            return jsonify(result), 400


@app.route('/api/login/status', methods=["GET", "POST"])
def login_check():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    response = make_response("")
    if username == None or password == None or data.login(username, password) != 1:
        result = {
            'error': '未登录'
        }
        return jsonify(result)
    else:
        return response

@app.route('/api/video/upload', methods=["POST"])
def upload():
    rawData = json.loads((request.get_data()).decode(encoding="utf-8"))
    enString=rawData['base64String']
    deString=base64.decodebytes(enString)
    filename="temp_%s.webm" % str(time.clock())
    file = open('/upload/%s' % filename, 'wb')
    file.write(deString)

@app.route('/api/user/info',methods=["GET","POST"])
def info():
        return jsonify({
            'avatar':'',
            'name':'Test',
            'tried':233
        })

@app.route('/api/video/list/<word>', methods=["GET","POST"])
def video_list(word):

    return jsonify({
        'list':[
            {
                'imageSrc':'',
                'stars': 4,
                'viewed':1234,
                'title':'Nice'
            },
            {
                'imageSrc': '',
                'stars': 5,
                'viewed': 321,
                'title': 'Hard'
            }
        ]
    })

@app.route('/api/word/list/<tag>', methods=["GET","POST"])
def word_list(tag):

    return jsonify({
        'list':[
            {
                'word': 'love',
                'played': 1314
            },
            {
                'word': 'gg',
                'played': 1322
            }
        ]
    })

@app.route('/api/word/search/<keyword>', methods=["GET","POST"])
def search(keyword):

    return jsonify({
        'list':[
            {
                'word': 'love',
                'played': 1314
            },
            {
                'word': 'gg',
                'played': 1322
            }
        ]
    })

@app.route('/test',methods=["GET","POST"])
def atest():
    return jsonify(calc.test())
     


# @app.route('/api/user/girl/add', methods=["GET", "POST"])
# def add_girl():
#     datam = json.loads((request.get_data()).decode(encoding="utf-8"))
#     username = request.cookies.get('username')
#     password = request.cookies.get('password')
#     response = make_response("")
#     if username == None or password == None or data.login(username, password) != 1:
#         result = {
#             'error': '未登录'
#         }
#         return jsonify(result)
#     else:
#         for i in datam:
#             if datam[i] == None:
#                 return jsonify({
#                     'error': '信息不完整'
#                 }), 400
#         data.commit_girl(username, datam)
#         return response
#
#
# @app.route('/api/user/girl/fail/<name>', methods=["GET", "POST"])
# def fail_girl(name):
#     username = request.cookies.get('username')
#     password = request.cookies.get('password')
#     response = make_response("")
#     if username == None or password == None or data.login(username, password) != 1:
#         result = {
#             'error': '未登录'
#         }
#         return jsonify(result)
#     else:
#         if name == None:
#             return jsonify({
#                 'error': '信息不完整'
#             }), 400
#         data.change_girl(username, name, 'F')
#         return response
#
#
# @app.route('/api/user/girl/success/<name>', methods=["GET", "POST"])
# def succ_girl(name):
#     username = request.cookies.get('username')
#     password = request.cookies.get('password')
#     response = make_response("")
#     if username == None or password == None or data.login(username, password) != 1:
#         result = {
#             'error': '未登录'
#         }
#         return jsonify(result)
#     else:
#         if name == None:
#             return jsonify({
#                 'error': '信息不完整'
#             }), 400
#         data.change_girl(username, name, 'T')
#         return response
#
#
# @app.route('/api/user/girl/pull', methods=["GET", "POST"])
# def pull_girl():
#     username = request.cookies.get('username')
#     password = request.cookies.get('password')
#     if username == None or password == None or data.login(username, password) != 1:
#         result = {
#             'error': '未登录'
#         }
#         return jsonify(result)
#     else:
#         result = data.pull_girl(username)
#         return jsonify(result)
#
#
# @app.route('/api/user/girl/analyse/<girlName>', methods=["GET", "POST"])
# def analyse(girlName):
#     username = request.cookies.get('username')
#     password = request.cookies.get('password')
#     if username == None or password == None or data.login(username, password) != 1:
#         result = {
#             'error': '未登录'
#         }
#         return jsonify(result)
#     else:
#         tagg = data.get_tags(username, girlName)
#         result = calc.get_score(tagg)
#         return jsonify(result)
#
#
# @app.route('/api/user/girl/method/<way>', methods=["GET", "POST"])
# def method(way):
#     datam = json.loads((request.get_data()).decode(encoding="utf-8"))
#     mt = {
#         'Ba': calc.Ba,
#         'Xue': calc.Xue,
#         'Fa': calc.Fa
#     }
#     result = mt[way](datam.array, datam.n)
#     return jsonify({"result": result})
#
#
# @app.route('/api/motion', methods=["GET", "POST"])
# def motion():
#     # argv = {'Action': '', 'Nonce': '', 'Region': '', 'SecretId': '', 'Timestamp': ''}
#     # content=request.content
#     # keys = ['Action', 'SecretId', 'Region', 'Timestamp', 'Nonce']
#     # secret_key = b'72lIdGziNtEPOAk9MNBnDRSHuLaeYIqB'
#     # secret_id = 'AKIDoV3Pcj5rJckgQy7cgYDhz4xfBVfdrzNZ'
#     # method = 'GET'
#     # url = 'wenzhi.api.qcloud.com/v2/index.php?'
#     # argv['Action'] = 'TextSentiment'
#     # argv['Region'] = 'sz'
#     # argv['Timestamp'] = str(int(time.mktime(datetime.datetime.now().timetuple())))
#     # argv['Nonce'] = str(random.randint(1, 23333))
#     # argv['SecretId'] = secret_id
#     # data = method + url
#     # for i in sorted(argv.keys()):
#     #     data += i + "=" + argv[i] + "&"
#     # data = data[:-1]
#     # data = data.encode('utf-8')
#     # print(data)
#     # signature = hmac.new(secret_key, data, sha1).digest()
#     # signature = base64.b64encode(signature)
#     # return urllib.request.quote(signature,safe="")
#     datam = json.loads((request.get_data()).decode(encoding="utf-8"))
#     datam['content'] = urllib.parse.quote(datam['content'])
#     url = 'https://api.prprpr.me/emotion/wenzhi?password=DIYgod&text=' + datam['content']
#     res = urllib.request.urlopen(url)
#     result = json.loads(res.read().decode('utf-8'))
#     return jsonify({'rate': result['positive']})
