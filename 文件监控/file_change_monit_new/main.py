#-*-coding:utf-8 -*-

from conf import monit_dir
from lib.monit_file_wy import do_monit
import os

def main():
    # facter用来获取本机ip地址
    if os.popen('rpm -q facter').read().find('not installed') != -1:
        os.system('yum install epel-release -y')
        os.system('yum install facter -y')

    if os.path.isdir(monit_dir):
        do_monit(monit_dir) 
    else:
        print "目录不存在"


if __name__ == '__main__':
    main()
