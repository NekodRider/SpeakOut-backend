# -*- coding: utf-8 -*-
from flask import jsonify, make_response, request ,url_for
from app import data, app, calc
import urllib.request, urllib.parse
import json, os
import base64, time


# import datetime, time
# import hmac, base64, urllib.request
# from hashlib import sha1


@app.route('/static/<file>', methods=["GET", "POST"])
def static(file):
    url_for('static', filename=file)

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
            response = make_response(jsonify({}))
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
    enString = rawData['base64String']
    question_id = rawData['questionID']
    linkword = rawData['link_words']
    deString = base64.b64decode(enString)
    filename = "%s_%s.webm" % (question_id, str(time.clock()))
    if filename in os.listdir(os.getcwd() + '/app/upload'):
        os.remove(os.getcwd() + '/app/upload/%s' % filename)
    os.mknod(os.getcwd() + '/app/upload/%s' % filename)
    file = open(os.getcwd() + '/app/upload/%s' % filename, 'wb')
    file.write(deString)
    res_linkword = []
    for i in linkword:
        print(i)
        end = i['time']['end'] / 100
        start = i['time']['start'] / 100
        if (end == start):
            continue
        end_score = calc.judge(filename, question_id, end - (end - start) * 1 / 4)
        mid_score = calc.judge(filename, question_id, (end + start) / 2)
        start_score = calc.judge(filename, question_id, start + (end - start) * 1 / 4)
        res_linkword.append({
            'word': i['words'],
            'score': [start_score, mid_score, end_score]
        })
    return jsonify({
        'link_words': res_linkword
    })


@app.route('/api/user/info', methods=["GET", "POST"])
def info():
    # avatar,name,times,[questionIDs]
    # user=request.cookies.get('username')
    # info=data.get_info(user)
    return jsonify({
        'avatar': '',
        'name': 'Test',
        'tried': 233
    })


@app.route('/api/video/list/<word>', methods=["GET", "POST"])
def video_list(word):
    # res_list=data.get_list(word=word)
    return jsonify({
        'list': [
            {
                'imageSrc': '',
                'videoID': 1,
                'stars': 4,
                'viewed': 1234,
                'title': 'test1'
            },
            {
                'imageSrc': '',
                'videoID': 2,
                'stars': 5,
                'viewed': 321,
                'title': 'test2'
            },
            {
                'imageSrc': '',
                'videoID': 3,
                'stars': 3,
                'viewed': 121,
                'title': 'test3'
            },
            {
                'imageSrc': '',
                'videoID': 4,
                'stars': 3,
                'viewed': 21,
                'title': 'test4'
            }
        ]
    })


@app.route('/api/word/list/<tag>', methods=["GET", "POST"])
def word_list(tag):
    # res_list=data.get_list(tag=tag)
    return jsonify({
        'list': [
            {
                'word': 'love',
                'played': 1314
            },
            {
                'word': 'peace',
                'played': 1522
            },
            {
                'word': 'fire',
                'played': 1122
            },
            {
                'word': 'world',
                'played': 722
            },
            {
                'word': 'hero',
                'played': 1722
            }
        ]
    })


@app.route('/api/word/search/<keyword>', methods=["GET", "POST"])
def search(keyword):
    # res_list=data.get_list(keyword=keyword)
    return jsonify({
        'list': [
            {
                'word': 'communication',
                'played': 1314
            },
            {
                'word': 'manner',
                'played': 1322
            },
            {
                'word': 'interview',
                'played': 2122
            },
            {
                'word': 'interaction',
                'played': 1022
            },
            {
                'word': 'reading',
                'played': 1622
            }
        ]
    })


@app.route('/api/video/detail/<videoID>', methods=["GET", "POST"])
def detail(videoID):
    # data.get_detail(videoID)
    res = {
        "test1": {
            'videoURL': 'https://storage.fredliang.cn/web/test2.mp4',
            'subtitle': {
                'time': 0,
                'text': 'In this American English pronunciation video, we are going to go over some difference in  sounds in American English and British English'
            }
        }, "test2": {
            'videoURL': 'https://storage.fredliang.cn/web/test3.mp4',
            'subtitle': {
                'time': 0,
                'text': "Today I'm going to make a video with another awesome English Channel on Youtube, Minuenlolink. The reason why I cooperating with them because they are in the UK. So together we are going to talk about some differences between American English and British English."
            }
        }
    }
    return jsonify(res[videoID])

# @app.route('/test',methods=["GET","POST"])
# def atest():
#    res=calc.test()
#    return jsonify({'res':res})
