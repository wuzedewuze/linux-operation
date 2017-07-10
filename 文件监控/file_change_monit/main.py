#-*-coding:utf-8 -*-

from conf import tomcat_dir , filter_file
from lib.inotify_call import FsMonitor
from threading import Thread
import os

def main():
    if os.popen('rpm -q facter').read().find('not installed') != -1:
        os.system('yum install epel-release -y')
        os.system('yum install facter -y')

    if os.path.isdir(tomcat_dir):
        dir_list = os.listdir(tomcat_dir)
        if filter_file in dir_list:
            dir_list.remove(filter_file)
        for dir in dir_list:
            path = os.path.join(tomcat_dir,dir)
            t1 = Thread(target=FsMonitor,args=(path,))
            t1.start()
    else:
        print tomcat_dir,"目录不存在"


if __name__ == '__main__':
    main()
