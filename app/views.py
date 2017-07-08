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
    question_id=str(rawData['questionID'])
    linkword=rawData['link_words']
    deString=base64.decodebytes(enString)
    filename="%s_%s.webm" % (question_id,str(time.clock()))
    file = open('/upload/%s' % filename, 'wb')
    file.write(deString)
    token=""
    for i in linkword:
        end=i['time']['end']
        start=i['time']['start']
        end_score=calc.judge(filename,question_id,end-(end-start)*1/4)
        mid_score=calc.judge(filename,question_id,(end+start)/2)
        start_score =calc.judge(filename,question_id,start+(end-start)*1/4)
        token+='?'+i['words']+'&'+str(start_score)+'&'+str(mid_score)+'&'+str(end_score)
    return jsonify({
        'token':token
    })


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
                'videoID':1,
                'stars': 4,
                'viewed':1234,
                'title':'Nice'
            },
            {
                'imageSrc': '',
                'videoID': 2,
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

@app.route('/api/video/detail/<videoID>',methods=["GET","POST"])
def detail(videoID):
    return jsonify({
        'videoURL':'storage.fredliang.cn/web/test2.mp4',
        'subtitle':{
            'time':132,
            'text':'gg'
        }
    })



@app.route('/test',methods=["GET","POST"])
def atest():
    res=calc.test()
    if res:
        print(res)
    return jsonify(res)