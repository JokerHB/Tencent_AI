# -*- coding: utf-8 -*-

# request
def postRequest(key, url):
    import urllib
    import urllib2
    import httplib
    import requests


    # keysList = key.items()
    # keysList.sort()

    post_data = ''
    for keys in key:
        post_data += '%s=%s&' %(str(keys),str(key[keys]))
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json'}

    req = urllib2.Request(url, post_data, headers=headers)
    resp = urllib2.urlopen(req)
    file=resp.read()
    print file

# Json encode
def jsonEncode(para):
    import json        
    pass

# Json decode
def jsonDecode(para):
    import json
    pass

# timestamp
def getTimestamp(tType = 0):
    from time import time

    def timeError(parm = None):
        print 'error# 1: can not handle this time type ' + str(parm) + ', please check it'

    tType = int(tType)
    if tType == 0:
        # integer time
        return int(time())
    elif tType == 1:
        # float time
        return time()
    else:
       errorProcess(errorType = 'CRASH', process = timeError, parm = tType)

# error process
def errorProcess(errorType, process, parm = None):
    if errorType == 'CRASH':
        # exit all threads
        process(parm)
        exit(-1)
    elif errorType == 'EXCEPTION':
        # handle the exception
        process(parm)
    else:
        # can not handle
        exit(0)

# BASE 64
def base64Endcode(content, sizelimit = 1 * 1024 * 1024):
    import sys
    import base64

    try:
        _content = base64.b64encode(content)
    except Exception, e:
        def baseError(error):
            print 'error#2: can not encode this content, ' + str(e)
        errorProcess(errorType = 'CRASH', process = baseError, parm = e)
    
    if sys.getsizeof(_content) >= sizelimit:
        def sizeError(error = None):
            print 'error#3: size limit is %d bytes, please short your content, current size is %d' % (sizelimit, sys.getsizeof(_content))
        errorProcess(errorType = 'CRASH', process = sizeError, parm = None)
    return _content

# Random string
def getRandomString(length = 10):
    from random import choice
    
    rs = ''
    baseStr = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    
    for i in range(length):
        rs += choice(baseStr)
    return rs

# md5 sum
def getMD5(content):
    import hashlib

    md5 = hashlib.md5()
    md5.update(content)
    return md5.hexdigest().upper()

# usage
def usage():
    print 'please input the image src'
    exit(-1)

def main():
    import sys
    from random import randint
    
    if len(sys.argv) < 2:
        # usage()
        pass

    # imagePath = str(sys.argv[1])
    # imagePath = imagePath.strip()
    # imageType = imagePath[len(imagePath) - 3:]

    if len(sys.argv) < 2:
        imagePath = './test.jpg'
        imageType = imagePath[len(imagePath) - 3:]

    if imageType != 'jpg':
        print 'please input the *.jpg file'
        exit(-1)

    try:
        imageFile = open(imagePath, 'rb')
        image = imageFile.read()
    except Exception, e:
        def fileError(error):
            print 'error#4: image read file failed, ' + str(error)
        errorProcess(errorType = 'CRASH', process = fileError, parm = e)
    imageFile.close()

    keys = {'app_id': 'your_app_id',
            'time_stamp': '', 
            'nonce_str': '',
            'format': '1',
            'topk': '5',
            'image': ''
            }
    url = 'https://api.ai.qq.com/fcgi-bin/vision/vision_objectr'

    keys['time_stamp'] = str(getTimestamp())
    keys['nonce_str'] = getRandomString(length = randint(10, 20))
    keys['image'] = base64Endcode(image)

    for key in keys:
        from urllib import quote_plus as quote
        keys[key] = quote(keys[key])

    keysList = keys.items()
    keysList.sort()
    tmpStr = ''
    for key,value in keysList:
        if key == 'sign':
            continue
        tmpStr += '%s=%s&' %(str(key),str(value))
    
    tmpStr += 'app_key=' + quote('your_app_key')
    keys['sign'] = quote(getMD5(content=tmpStr))
    print tmpStr
    postRequest(key = keys, url = url)

if __name__ == '__main__':
    main()