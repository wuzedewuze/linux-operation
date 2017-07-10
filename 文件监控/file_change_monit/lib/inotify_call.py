#-*- coding:utf-8-*-

import os
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY, IN_ATTRIB
from conf import redis_queue_conf
from lib.logOut import logOut
import datetime
import re
import redis
import json

class EventHandler(ProcessEvent):
    def __init__(self):
        self._ip = os.popen('facter ipaddress').read().strip()
        if redis_queue_conf['password']:
            self._redis_conn = redis.Redis(host=redis_queue_conf['host'],port=redis_queue_conf['port'],
                                           db=redis_queue_conf['db'],password=redis_queue_conf['password'])
        else:
            self._redis_conn = redis.Redis(host=redis_queue_conf['host'], port=redis_queue_conf['port'],
                                           db=redis_queue_conf['db'])

        self._regex = re.compile('\.(log|out|txt|tmp|pdf|png|swp|swx)$|^/usr/local/tomcat/tomcat_log|server/work')

    def process_IN_CREATE(self, event):
        file = os.path.join(event.path, event.name)
        if not re.search(self._regex, file):
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                data = {'op': 'create', 'date': date, 'ip': self._ip, 'file': file}
                self._redis_conn.lpush('omp_file_monit', json.dumps(data))
            except Exception as e:
                logOut().error(e)

    def process_IN_DELETE(self, event):
        file = os.path.join(event.path, event.name)
        if not re.search(self._regex, file):
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                data = {'op': 'delete', 'date': date, 'ip': self._ip, 'file': file}
                self._redis_conn.lpush('omp_file_monit', json.dumps(data))
            except Exception as e:
                logOut().error(e)

    def process_IN_MODIFY(self, event):
        file = os.path.join(event.path, event.name)
        if not re.search(self._regex, file):
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                data = {'op': 'modify', 'date': date, 'ip': self._ip, 'file': file}
                self._redis_conn.lpush('omp_file_monit', json.dumps(data))
            except Exception as e:
                logOut().error(e)

    def process_IN_ATTRIB(self, event):
        file = os.path.join(event.path, event.name)
        if not re.search(self._regex, file):
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                data = {'op': 'attrib', 'date': date, 'ip': self._ip, 'file': file}
                self._redis_conn.lpush('omp_file_monit', json.dumps(data))
            except Exception as e:
                logOut().error(e)


def FsMonitor(path='.'):
    wm = WatchManager()
    mask = IN_DELETE | IN_CREATE | IN_MODIFY | IN_ATTRIB
    notifier = Notifier(wm, EventHandler())
    wm.add_watch(path, mask, auto_add= True, rec=True)


    while True:
        try:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
        except KeyboardInterrupt:
            notifier.stop()
            break

