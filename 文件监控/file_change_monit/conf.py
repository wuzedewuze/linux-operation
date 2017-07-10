#-*-coding:utf-8-*-

tomcat_dir = '/usr/local/tomcat'
error_log = '/var/log/tomcat_file_change_monit.error'
filter_file = ['tomcat_log']
redis_queue_conf = {
    'host'  :   '192.168.0.201',
    'port'  :   6379,
    'db'    :   0,
    'password': ''
}
