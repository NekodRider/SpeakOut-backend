# -*- coding: utf-8 -*-
import math
import os, base64, requests, json, subprocess
import urllib, http
from qcloud_image import Client
from qcloud_image import CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers
appid = '1252308077'
secret_id = 'AKIDvicP4aJ1znQq9OsgjcQ6ZptkOp46pfDc'
secret_key = 'OagaIn5A2hDYhdN0ITTHsRp0zlKgroaD'
bucket = 'faceidentify'

headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '5a496ffbc8694f27a07d04bd3fa87762',
}
params = urllib.parse.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'true'
})


def faceplus(filepath):
    #result = {
    #    'underLipTop':0,
    #    'mouthRight':0,
    #    'upperLipTop':0,
    #    'upperLipBottom':0,
    #    'mouthLeft':0,
    #    'underLipBottom':0
    #}
    #face_file = filepath
    #image = open(face_file, "rb")
    #image_body = image.read()
    
    client = Client(appid, secret_id, secret_key, bucket)
    client.use_http()
    client.set_timeout(30)
    result=client.face_shape(CIFile(filepath),1)["data"]["face_shape"][0]['mouth']



    
    #conn = http.client.HTTPSConnection('api.cognitive.azure.cn')
    #conn.request("POST", "/face/v1.0/detect?%s" % params, image_body, headers)
    #response = conn.getresponse()
    #rawData = response.read().decode()
    #if not json.loads(rawData)[0]:
    #    return False
    #print(json.loads(rawData))
    #rawData = json.loads(rawData)[0]['faceLandmarks']
    #conn.close()
    #for i in rawData:
    #    if 'Lip' in i or 'mouth' in i:
    #        result[i]=rawData[i]
    #        print(i)
    return result

# underLipTop
# mouthRight
# upperLipTop
# upperLipBottom
# mouthLeft
# underLipBottom

def get_lenth(a,b):
    return math.sqrt(pow(a['x'] - b['x'],2) + pow(a['y'] - b['y'],2))

def update_sample(sample,standard):
    width_standard = standard['mouthRight']['x'] - standard['mouthLeft']['x']
    width_sample = get_lenth(sample['mouthRight'],sample['mouthLeft'])

    center_standard = {
        'x': standard['mouthRight']['x'] - width_standard / 2,
        'y': standard['mouthRight']['y'] + standard['mouthLeft']['y'] / 2
    }

    center_sample = {
        'x': sample['mouthRight']['x'] - width_sample / 2,
        'y': sample['mouthRight']['y'] + sample['mouthLeft']['y'] / 2
    }

    mask = width_sample / width_standard
    print("mask:", mask)
    sample={
        'underLipTop': {
            'x':center_standard['x'],
            'y':-get_lenth(sample['underLipTop'],center_sample)*mask+center_standard['y']
        },
        'mouthRight': standard['mouthRight'],
        'upperLipTop': {
            'x':center_standard['x'],
            'y':get_lenth(sample['upperLipTop'],center_sample)*mask+center_standard['y']
        },
        'upperLipBottom': {
            'x':center_standard['x'],
            'y':get_lenth(sample['upperLipBottom'],center_sample)*mask+center_standard['y']
        },
        'mouthLeft': standard['mouthLeft'],
        'underLipBottom': {
            'x':center_standard['x'],
            'y':-get_lenth(sample['underLipBottom'],center_sample)*mask+center_standard['y']
        }
    }
    return sample



def get_score(pos,sample, standard):
    get_frame(pos, sample)
    get_frame(pos, standard)
    dot_sample = faceplus(sample)
    dot_standard = faceplus(standard)
    dot_sample=update_sample(dot_sample,dot_standard)







    return False


def get_frame(pos, filepath):
    subprocess.run("ffmpeg -i %s.webm -y -f  image2  -ss %s -vframes 1  %s.jpg" % (filepath, str(pos), filepath),
                   shell=True)



def test():
    get_frame(1, '~/hackinit/app/question/test')
    res = faceplus('app/question/test.jpg')
    return res
