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
    result=[]
    raw=client.face_shape(CIFile(filepath+'.jpg'),1)
    rawData=raw["data"]
    if "face_shape" in rawData:
        result=rawData["face_shape"][0]['mouth']
    else:
        print(raw)



    
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

def get_length(a,b):
    return math.sqrt(pow(a['x'] - b['x'],2) + pow(a['y'] - b['y'],2))

def update_sample(sample,standard):
    #print(sample,standard)
    width_standard = standard[6]['x'] - standard[0]['x']
    width_sample = get_length(sample[6],sample[0])
    width=sample[6]['x']-sample[0]['x']

    center_standard = {
        'x': standard[6]['x'] - width_standard / 2,
        'y': (standard[6]['y'] + standard[0]['y'] )/ 2
    }

    center_sample = {
        'x': sample[6]['x'] - width / 2,
        'y': (sample[6]['y'] + sample[0]['y'] )/ 2
    }

    mask = width_sample / width_standard
    #print("mask:", mask)
    for i in range(22):
        if i!=0 and i!=6:
            sample[i]={
                'x':(sample[i]['x']-center_sample['x'])*mask+center_standard['x'],
                'y':(sample[i]['y']-center_sample['y'])*mask+center_standard['y']
            }
    sample[0]=standard[0]
    sample[6]=standard[6]
    return sample



def get_score(pos,sample, standard):
    get_frame(pos, sample)
    get_frame(pos, standard)
    dot_sample = faceplus(sample)
    dot_standard = faceplus(standard)
    dot_sample=update_sample(dot_sample,dot_standard)







    return [dot_standard,dot_sample]


def get_frame(pos, filepath):
    subprocess.run("ffmpeg -i %s.webm -y -f  image2  -ss %s -vframes 1  %s.jpg" % (filepath, str(pos), filepath),
                   shell=True)



def test():
    get_frame(1, os.getcwd()+'/app/question/a')
    dot_sample = faceplus(os.getcwd()+'/app/question/a')

    get_frame(1, os.getcwd()+'/app/question/b')
    dot_standard = faceplus(os.getcwd()+'/app/question/b')

    dot_sample = update_sample(dot_sample, dot_standard)

    return {'st':dot_standard, 'sample':dot_sample}
