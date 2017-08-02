# -*- coding: utf-8 -*-

# request
def postRequest(key, url):
    import urllib
    import urllib2
    import httplib
    import requests
    
    post_data = urllib.urlencode(key)
    req = urllib2.Request(url,post_data)
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
        _content = base64.urlsafe_b64encode(content)
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
        usage()

    imagePath = str(sys.argv[1])
    imagePath = imagePath.strip()
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

    keys = {'app_id': '', 
            'time_stamp': '', 
            'nonce_str': '',
            'sign': '', 
            'format': '1',
            'topk': '5',
            'image': ''
            }
    url = 'https://api.ai.qq.com/fcgi-bin/vision/vision_objectr'

    # time_stamp
    from urllib import quote_plus as quote

    keys['time_stamp'] = quote(str(getTimestamp()))
    keys['nonce_str'] = quote(getRandomString(length = 10))
    keys['image'] = quote(base64Endcode(image))
    
    keysList = keys.items()
    keysList.sort()
    tmpStr = ''
    for key,value in keysList:
        if key == 'sign':
            continue
        tmpStr += '%s=%s&' %(quote(str(key)), quote(str(value)))
    
    tmpStr += quote('app_key=*********')
    keys['sign'] = quote(getMD5(content=tmpStr))
    req = postRequest(key = keys, url = url)

if __name__ == '__main__':
    main()