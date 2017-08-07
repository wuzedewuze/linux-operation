#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Filename : exceptionPython.py
import urllib2
import json

# test a  baner
# 输入url和json格式的文件就可以进行POST操作。
def getresult(url, values):
    try:
        data = json.dumps(values)
        req = urllib2.Request(url=url, data=data)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req)
        the_page = response.read()
        pagelast = json.loads(the_page)
        print pagelast
        result = pagelast['status']
        return result
    except Exception, e:
        print 'error', e
        return 2
