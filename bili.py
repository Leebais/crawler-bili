# -*-coding:utf-8-*-    #编码，防乱码
#from lxml import etree #xpath分析image's url使用，

import hashlib      #用于文件校验
import requests     #模拟hppts请求
import re           #正则表达式，用于提取image、cv号
import os           #提供文件读写操作
import time         #提供延时函数

header = {          #自定义请求头，防止反爬（ps：bili站为啥没有？）
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43'
}
rule_for_cvnumber = '{"id":(.*?),".*?":{".*?,".*?",".*?"'   #提取cv号的正则表达式

def run(current_url):   #对每一个cv号进行遍历爬取
    html = getrequests(current_url) #爬取当前cv号的专栏网页
    dir_name,urls = analysi(html)   #从网页的文本中提取标题（dir_name）、image's urls（urls）
    dir_name =tryMkdir(dir_name)    #以标题为文件夹名尝试创建文件夹
    writeTodisk(dir_name,urls)  #将网页中的image写入磁盘
    return


def getrequests(str):   #返回网页的text文本
    print(str)          #显示当前爬取的网页地址
    respones = requests.get(str, headers=header)
    return respones.text


def tryMkdir(s_dir_name):   #尝试创建文件夹
    dir_name = '../Download/'+s_dir_name    #由原始dir_name转换为适合的名称
    if not os.path.exists(dir_name):        #在父目录下的Download下创建文件夹名为dir_name的文件夹
        os.mkdir(dir_name)
    return dir_name #返回经过修改的dir_name


def writeTodisk(dir_name,urls): #遍历网页中的image并存储到磁盘文件
    i = 0   #计数
    for url in urls:
        Filename_Extension = url.split('.')[-1] #解析文件扩展名
        response = requests.get('https:' + url, headers=header) #连接image's url
        fullpath = dir_name + '/' + str(i) + '.' + Filename_Extension   #生成完整的文件path
        print("now downloading " + fullpath )   #显示当前下载的文件path
        if os.path.isfile(fullpath):    #判断是否已下载过这个文件（叫它 A）
            t = open(fullpath,'rb')     #打开文件path所对对应的文件 A
            local_sha256 = hashlib.sha256()     #新建一个sha256校验码A'
            local_sha256.update(t.read())       #更新A'
            t.close()                   #关闭A
            url_sha256 =hashlib.sha256()    #再为iamge新建一个sha256校验码B'
            url_sha256.update(response.content) #更新B'
            if(local_sha256.hexdigest()==url_sha256.hexdigest()):   #判断A和B的sha256校验码是否相同
                print('exexists '+ fullpath)    #A和B相同，即下载过且文件完整
            else:
                f = open(fullpath,'wb') #A文件不完整
                f.write(response.content)   #重新下载A
                f.close()   #关闭A
        else:   #查无词文件，下载它
            f = open(fullpath, 'wb')    #打开（新建）文件A
            f.write(response.content)   #将A写入磁盘
            f.close()   #关闭A
        i += 1
    #print(len(urls))
    print('downloaded ' + dir_name) #提示此网页已爬取完成
    time.sleep(1)   #休眠1秒
    os.system('clear')  #调用系统命令清屏
    return


def analysi(html):  #分析当前cv号对应的网页
    dir_name = re.findall('<h1 class="title">(.*?)</h1>', html)[-1] #解析网页的标题
    print(dir_name) #打印网页标题（文件的名字）
    urls = re.findall('<img data-src="(.*?)".*?>', html)    #用正则表达式提取image's urls
    for i in urls:
        print('https:'+i)   #打印每个image's url
    return dir_name,urls    #返回文件夹名称和image's urls


def findCvNumber(rst1,mid): #更具mid查找cvhao
    page = 0    #预定义page，即从第零页开始查找
    while (1):
        localurl = 'https://api.bilibili.com/x/space/article?mid=' + mid + '&pn=' + str(page)   #合成具有cv号信息的网页A
        res = requests.get(url=localurl, headers=header)    #请求A
        html = res.text #转换A为文本
        length = len(res.content)   #计算A的文本的长度
        if(length<100): #小于100算作无新的cv号了
            break
        #print('len=' + str(length))    #输出A的文本的长度
        rst = re.findall(rule_for_cvnumber, html)   #更具正则表达式提取具有cv号的文本
        rst1.append(re.findall('[0-9]{7}', str(rst)))   #提取cv号
        rstforprint = re.findall('[0-9]{7}', str(rst))  #用于打印的cv号列表
        print('page=' + str(page))  #打印这是第几页
        print(rstforprint)  #打印cv号列表
        page+=1
        time.sleep(1)   #休眠1秒
    return rst1 #返回二维cv号列表


def main(cv_list):  #对每个cv号进行爬取
    per_url = 'https://www.bilibili.com/read/cv'    #专栏的固定前缀
    for i in cv_list:   #遍历cv——list
        for j in i:
            run(per_url+j)  #调用run进行爬取
    return
if __name__ == '__main__':
    #main()
    #findurl()
    cv_list = []    #初始化一个cv_list
    mid = '2776454' #一个mid
    cv_list=findCvNumber(cv_list,mid)   #调用findCvNumber抓去cv号列表
    main(cv_list)   #调用main进行对每个cv号进行爬取
    print('Hello World')    #标志性输出