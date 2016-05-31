#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-30 20:25:14
# @Author  : vsoy
# @Link    :
# @Version : beta

import sys
import urlparse
import requests
import multiprocessing


scanDict = './dict/PHP.txt'  # 字典
proNum = 20 #进程数
headers = {  # HTTP 头设置
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}


try:
    url = sys.argv[1].strip()
    check = urlparse.urlparse(url)
    if check.scheme == 'http':
        url = check.netloc
except Exception, e:
    print 'Usage: python phpscan.py www.baidu.com'
    exit()


def scan(payload):
    try:
        taskurl = 'http://%s%s' % (url, payload)
        taskurl = taskurl.strip()
        task = requests.get(taskurl, headers=headers,timeout=5)
        print "%s:%s" % (taskurl,str(task.status_code))

            if task.status_code == 200:
                return taskurl
    except Exception, err:
        print err


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=proNum)
    result = []
    for payload in file(scanDict):
        result.append(pool.apply_async(scan, (payload,)))
    pool.close()
    pool.join()

    print '-' * 20
    for i in result:
        try:
            if i.get() != None:
                print i.get()
        except:
            continue
    print '-' * 20
    print 'End!'
