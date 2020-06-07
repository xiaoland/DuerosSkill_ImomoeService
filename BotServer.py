#!/usr/bin/env python2
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018/1/3

"""
    desc:pass
"""
from cgi import parse_qs, escape
import json
from index import handler
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def application(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except(ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
    print('request_body = %s\n' % request_body)
    if not request_body:
        return writeResponse(start_response,'未获取到请求数据')

    bot = handler(request_body)
    #添加错误回调方法
    # bot.setCallBack(callback)

    #验证签名enableVerifyRequestSign  disableVerifyRequestSign 关闭验证签名
    # bot.initCertificate(environ).enableVerifyRequestSign()
    bot.init_certificate(environ).disable_verify_request_sign()
    bot.set_private_key(priKey)

    body_str = bot.run()
    print(body_str)
    return writeResponse(start_response, body_str)

def writeResponse(start_response, body_str):

    body = body_str.encode('utf-8')
    response_headers = [('Content-Type', 'application/json'),
                        ('Content-Length', str(len(body)))]
    status = '200 OK'
    print(body)
    start_response(status, response_headers)
    return [body]


priKey = '''-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA3ES11uq/tJj7tDOKYBvJhkeCvsz3AP6qdwW6oJ56ZoW5KoWEbfQz5qfmBy3e
BAFLFBM5jKDGSUD5DSYjQmL+9rBtDfbzLu4IyhfsEcWhFsteVUqRj6+vBikHlWhlJGpRuvpZ19OL
uhcmxzClZ8msyEBcw1sk+5Xg0zwwf2qN+yMb9u/pHKwGw0A+9M04b/7I25ozRmu+mMP1LQKL3M6c
eKPGNhwHtXxFOqFnwY1BLgUqpuaLmzeda03O5fEG/k7F23ZPEJ0uByJjegIPXbrOVSZ+JsbeLGuA
opUugRS9/eHtQtIV3KpzJfep7v4MBl8kFyF5PWJ6dRrxT0Ji422HCQIDAQABAoIBAQChh1HCNYw4
KCgNUe6b5ES40CA1Q6GvfRINDop51z3ziQTtBdTDvV2CPIYXpa82SKyCIEcHta8zcQ4yclFREb/f
sCmJIBvdwnl3mmtn7QHg8WpQKcrtD+zOG7CQBGqHdeBRud3AxEWnResOD8J8hgzLHUfpiyFnzdV9
kpoOFlngW9Zf/oGqBqdHsQ/R/h22CBTM4Rb3u0sQesfT9XNIuJfI71wCPs10I6PkildEdQpsThDQ
yjBhBPEdtq4ZDJLGSKsxlK4HIWEI9C+x3WEZ/9KGfv8n4gmChkdNphdCRcQGM4L/M20nRrlLUmtc
V3gFa1+NB1m/qXft3txomj9znSvBAoGBAPWPXi5opoRC6TZLsW5BfDgHQFdvu0carziG98DDQGPb
TCuzVP3bpmh3hhXyqX7c8/entLY/MRe46Lj8DfVqPKN3FFoawlvOPOvHMJ1LCO1ywkGeTco7z6hJ
OLW0hNj+T6t57XBhmCXdeFMUiFelHFTS35hCDx8ya0smNyiB9uw9AoGBAOWiEqBCPfcvhZdxGq7z
cDShWqBo7S0MUJCCAXcN/JZQN2zn7T41BbIa68kL/uNxANnbEFVEj0zFw4SVAheXzW8FNM9gWUv/
uVaDV1IzlmPYIooCni/OWUXzfIibURzdWvA6w7nFif/4ugZicgRBBvQ11quHSyJgCCqQIgEvAXa9
AoGBAPDIYetTxmPOUGtjEVoxcCJoSdjywEpaihH9lhY33n2L3UbEk8RQiv3IpXwD89tnwPnIQlSp
5fOC5v/sd6t7PnZzH0uzDX2D3wy6xpqVpu1eJ8i79z8kIty635acqd80jt5vsjkOGWiXn5KngYGf
bwZlt8XOkJFgmQCZOmDH/11pAoGAI0CfVWT1+FWeT6J4czVCG4JN1GRnTMwgLh8XNHy8MyM7bwen
3y3qou4JFoM17RqzA77iogR1b1bI7jil6pNOYWXONqvW6ZjnjgV5yU/MHaXXn5JJUJOAFwILMzmM
2T6OMGUFGSbfSaGYhVRlpouJEsKVIx4RBcTyW/5migH6Wo0CgYAccQonJTcnIzy4tmrH/R5stFoZ
Dp/ndWismyxaaGLB7F7iCGYqzsj3NGU/Zs+CpWerM5pf/92B5EfJrX3inUlCwOsFLgr5pZQBN9O9
xwHRsRXIjExXZ0wPC6KHG1+dSzXohqdieZdP7Iirf622A1i/Y6RoksC7Uefg2D3IFZ4BlQ==
-----END RSA PRIVATE KEY-----'''
