# -*- coding: utf-8 -*-
from PIL import Image
import os, base64, requests, json, subprocess
import urllib, http

headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '5a496ffbc8694f27a07d04bd3fa87762',
}
params = urllib.parse.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'true'
})


def faceplus(filepath):
    result = []
    face_file = filepath
    image = open(face_file, "rb")
    image_body = image.read()

    conn = http.client.HTTPSConnection('api.cognitive.azure.cn')
    conn.request("POST", "/face/v1.0/detect?%s" % params, image_body, headers)
    response = conn.getresponse()
    rawData = response.read().decode()
    if not json.loads(rawData)[0]:
        return False
    print(json.loads(rawData))
    rawData = json.loads(rawData)[0]['faceLandmarks']
    conn.close()
    for i in rawData:
        if 'Lip' in i or 'mouth' in i:
            result.append(rawData[i])
            print(i)
    return result


def get_score(sample, standard):
    dot_sample = get_frame(sample)
    dot_standard = get_frame(standard)

    width_standard = dot_sample[5] - dot_sample[0]
    height_standard = dot_sample[3] - dot_sample[2]

    width_sample = dot_sample[5] - dot_sample[0]
    height_sample = dot_sample[3] - dot_sample[2]

    center_standard = {
                    'x':dot_standard[5]-width_standard/2,
                    'y':dot_standard[3]-height_standard/2
    }

    center_sample = {
                    'x':dot_sample[5]-width_sample/2,
                    'y':dot_sample[3]-height_sample/2
    }




    return False


def get_frame(pos, filepath):
    subprocess.run("ffmpeg -i %s.webm -y -f  image2  -ss %s -vframes 1  %s.jpg" % (filepath, str(pos), filepath),
                   shell=True)


def judge(filename):
    get_score(a)
    return False


def test():
    get_frame(1, '~/hackinit/app/question/test')
    res = faceplus('app/question/test.jpg')
    return res
