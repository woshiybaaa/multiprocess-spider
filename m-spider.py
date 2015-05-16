#coding=utf-8
#!/usr/bin/python
from urllib2 import Request, urlopen, URLError, HTTPError
from multiprocessing import Pool
import os
import chardet
import sys
import urllib2
import re
import time
# import socket
# urllib2.socket.setdefaulttimeout(60) # Python2.6以前的版本用

number_of_at_the_same_time_the_process = 1        #同时进程数
number_of_tasks = 1        # alignment number # 列队中的数目

def open_file(source_file):

    result_file = source_file+"-result"  # 执行结果以源文件名+result形式保存
                                
    with open("log", 'a') as output:
        output.write("开始时间:"+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+"\n")
    print "进程"+source_file+"开始"
    # 以下两行引用文件和输出文件!

    for text_line in open(source_file):        # 轮询源文件中的网址
        host_value = text_line.split()        # 用空格分割字符串
        status = spider(host_value[0])
        # 如果source_file这个文本中第一列的网址能够访问的话，执行第二列中的网址
        if status == 0:  spider(host_value[1])
    with open("log", 'a') as output:
        output.write("结束时间:"+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+"\n")    
    print "进程"+source_file+"结束"


def spider(text_line):
    
    text_line = text_line.replace("\n", "")        # 替换上一步中，轮询到的每行结果中的换行字符为空白
    req_url = "http://"+text_line        # 因为self*的域名是不带http://的，这边加下

    try:
        response_of_req_url = urlopen(req_url)
    except Exception, e:
        with open(result_file, 'a') as output:
            output.write("url_Error "+str(e)+" "+req_url+"\n")
        return 0
    except: print "0"        # pass
    else:
        try: html = urllib2.urlopen(req_url, timeout=60).read()        # 请求网址
        except Exception, x:
            with open(result_file, 'a') as output:
                output.write("http_Error "+str(x)+" "+req_url+"\n")
        except:
            print "1"        # pass
        else:
            coding = str(chardet.detect(html))
            isUTF8 = ["ISO-8859-2", "utf"]
            if isUTF8[0] in coding.lower() or isUTF8[1] in coding.lower():
                htmlIsutf8 = html
                if "百家乐" in htmlIsutf8:
                    with open(result_file, 'a') as output:
                        output.write("违规信息-百家乐"+" "+req_url+"\n")
                elif "太阳城" in htmlIsutf8:
                    with open(result_file, 'a') as output:
                        output.write("违规信息-太阳城"+" "+req_url+"\n")
                # 因为有的标题是多行的，保存起来有问题，所以这边去掉一切换行
                htmlIsutf8 = string.replace(htmlIsutf8, '\r\n', '');
                htmlIsutf8 = string.replace(htmlIsutf8, '\n', '');
                m = re.search(r'<title>(.*?)</title>', htmlIsutf8, flags=re.I)
                if m:        #如果标题不为空 则真，否则为假
                    with open(result_file, 'a') as output:
                        output.write(m.group(1)+" "+req_url+"\n")
                    #print m.group()  # 调试用
                else:  # 特殊标题的标记
                    # <title xmlns=...><title> 个人用
                    m = re.search(r'<title xmlns="">(.*)</title>', htmlIsutf8, flags=re.I)
                    if m:
                        with open(result_file, 'a') as output:
                            output.write(m.group(1)+" "+req_url+"\n")
                    else:
                        with open(result_file, 'a') as output:
                            output.write("error"+" "+req_url+"\n")
            else:
                htmlNoutf8 = html.decode('gbk', 'ignore').encode('utf-8')
                htmlNoutf8 = string.replace(htmlNoutf8, '\r\n', '');
                htmlNoutf8 = string.replace(htmlNoutf8, '\n', '');
                m = re.search(r'<title>(.*?)</title>', htmlNoutf8, flags=re.I)
                if "百家乐" in htmlNoutf8:
                    with open(result_file, 'a') as output:
                        output.write("违规信息-百家乐"+" "+req_url+"\n")
                elif "太阳城" in htmlNoutf8:
                    with open(result_file, 'a') as output:
                        output.write("违规信息-太阳城"+" "+req_url+"\n")
                if m:
                    with open(result_file, 'a') as output:
                        output.write(m.group(1)+" "+req_url+"\n")
                else:
                    m = re.search(r'<title xmlns="">(.*)</title>', htmlNoutf8, flags = re.I)
                    if m:
                        with open(result_file, 'a') as output:
                            output.write(m.group(1)+" "+req_url+"\n")
                    else:
                        with open(result_file, 'a') as output:
                            output.write("error"+" "+req_url+"\n")
                            
    
if __name__=='__main__':
    print 'Parent process %s.' % os.getpid()
    p = Pool(number_of_at_the_same_time_the_process)
    for i in xrange(number_of_tasks):
        if number_of_tasks < 10:
            p.apply_async(open_file, args=("self"+str(i),))
        elif number_of_tasks < 100:
            if i < 10: 
                p.apply_async(open_file, args=("self0"+str(i),))
            else:
                p.apply_async(open_file, args=("self"+str(i),))        # that is 10 < i < 100
        elif number_of_tasks < 1000:
            if i < 10:
                p.apply_async(open_file, args=("self00"+str(i),))
            elif i < 100:
                p.apply_async(open_file, args=("self0"+str(i),))
            else:
                p.apply_async(open_file, args=("self"+str(i),))        # that is 100 < i < 1000
        elif number_of_tasks < 10000:
            if i < 10:
                p.apply_async(open_file, args=("self000"+str(i),))
            elif i < 100:
                p.apply_async(open_file, args=("self00"+str(i),))
            elif i < 1000:
                p.apply_async(open_file, args=("self0"+str(i),))
            else:
                p.apply_async(open_file, args=("self"+str(i),))        # that is 1000 < i < 10000
        else:
            print "tasklist number over 1W! # 队列数目超过1W"
            
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    os.system("amh mysql start")        #怕mysql挂掉
    print 'All subprocesses done.'