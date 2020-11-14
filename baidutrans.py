import http.client
import hashlib
import urllib.parse
import random
import json


def baiduTranslate(q="苹果", fromLang="jp", toLang="zh"):
    appid = '20201107000610820' #你的appid(这里是必填的, 从百度 开发者信息一览获取)
    secretKey = 'ONlxCCkk82ZOCYIsQdEe' #你的密钥(这里是必填的, 从百度 开发者信息一览获取)

    httpClient = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode())
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    result = ""
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        result = response.read()
    except Exception as e:
        print (e)
    finally:
        if httpClient:
            httpClient.close()
    rest = json.loads(result)['trans_result'][0]['dst']
    #print(rest)
    return rest


def main():
    word = input("请输入：")
    print(baiduTranslate(word))

if __name__ == '__main__':
    main()