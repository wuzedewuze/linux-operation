#-*- coding:utf-8-*-

import os
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY, IN_ATTRIB
import pyinotify
import sys

#from conf import redis_queue_conf
from conf import redis_queue_conf

from lib.log_out import log_init

import datetime
import re
import redis
import json


class EventHandler(ProcessEvent):
    def __init__(self):

        # 获取本地ip地址
        self._ip = os.popen('facter ipaddress').read().strip()

        # 初始化redis连接
        if redis_queue_conf['password']:
            self._redis_conn = redis.Redis(host=redis_queue_conf['host'],port=redis_queue_conf['port'],
                                           db=redis_queue_conf['db'],password=redis_queue_conf['password'])
        else:
            self._redis_conn = redis.Redis(host=redis_queue_conf['host'], port=redis_queue_conf['port'],
                                           db=redis_queue_conf['db'])
        # 排除不监控目录的正则表达式
        self._regex = re.compile('\.(log|out|txt|tmp|pdf|png|swp|swx)$|^/usr/local/tomcat/tomcat_log|server/work')



    # 写入redis的装饰器
    def add_redis(function):
        def add_message(self,event):
            function(self,event) # 执行引用函数
            file = os.path.join(event.path, event.name)
            # 判断是否在不监控的正则中
            if not re.search(self._regex, file):
                date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_init().info(file)
                try:
                    data = {'op': event.maskname, 'date': date, 'ip': self._ip, 'file': file}
                    self._redis_conn.lpush('file_monit', json.dumps(data))
                except Exception as e:
                    log_init().error(e)
                    
        return add_message


    @add_redis
    def process_IN_CREATE(self, event):
        pass


#主方法，执行调用监控
def do_monit(monit_path='./'):
    wm = WatchManager()  #create a watchmanager()
    mask = pyinotify.IN_DELETE | pyinotify.IN_MODIFY | pyinotify.IN_CREATE  # 需要监控的事件 
    notifier = Notifier(wm, EventHandler())
    wdd = wm.add_watch(monit_path, mask, rec=True)  # 加入监控，mask，rec递归
    try:
        #防止启动多个的命令 设置进程号文件就可以防止启动多个
        notifier.loop(daemonize=True, pid_file='/tmp/pyinotify2.pid')
    except pyinotify.NotifierError, err:
        print >> sys.stderr, err

if __name__ == "__main__":
    monit_path = "/usr/local/tomcat"
    do_monit(monit_path)
