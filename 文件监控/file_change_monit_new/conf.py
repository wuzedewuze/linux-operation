#-*-coding:utf-8-*-

# 需要监控的路径
monit_dir = '/usr/local/tomcat'
# 日志路径配置
error_log_file = '/var/log/tomcat_file_change_monit.error'
info_log_file = '/var/log/tomcat_file_change_monit.access'

# 需要排除的目录
#filter_file = ['tomcat_log']

# 发送到指定redis配置
redis_queue_conf = {
    'host'  :   '192.168.0.201',
    'port'  :   6379,
    'db'    :   0,
    'password': ''
}
