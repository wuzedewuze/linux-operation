#-*-coding:utf-8-*-

import redis
import time
import urllib2
import json
import datetime
import os
import re

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


def send_sms(mobile,message):
    data = {
         "smsID": "5398f0d7be164a3a8d51875055cc6756",
         "smsContent": message,
         "sMobile": mobile,
         "serviceType": "1"}
    headers = {'Content-Type':'application/json'}
    url = 'http://192.1.1.10:9103/send/sendSMS'
    request = urllib2.Request(url=url,headers=headers,data=json.dumps(data))
    urllib2.urlopen(request)


def send_mail(mail_list,mail_content):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    mail_host = "smtp.163.com"
    mail_user = "_mail"
    mail_pass = "2016"

    sender = 'mail@163.com'
    receivers = mail_list
    # message = MIMEText('', 'plain', 'utf-8')
    message = MIMEText(mail_content, 'plain', 'utf-8')
    message['From'] = "mail@163.com"
    message['To'] = "0961@qq.com"

    subject = '系统文件变化'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
    except Exception, e:
        print e



def main():
    redis_conn = redis.Redis('1.168.250.221',db=0,port=6379)
    data = []
    mail_data = []
    mobile_list = [19295757216]
    mail_list = ['2851520574@qq.com']
    local_ip = os.popen('facter ipaddress').read().strip()

    while True:
        try:
            change_file_data = redis_conn.blpop('omp_file_monit',timeout=1)[1]
            data.append(json.loads(change_file_data))
            mail_data.append(re.sub('{|\"|}','',change_file_data))

        except TypeError as e:
            if len(data) != 0:
                ip_list = []
                log_obj = open('/var/log/file_monit.log','a')
                for item in data:
                    if not item['ip'] in ip_list:
                        ip_list.append(item['ip'])
                    date = item['date']
                    ip = item['ip']
                    file = item['file']
                    op = item['op']
                    log = u'时间:%s , 服务器:%s , 操作:%s , 文件:%s\n' % (date,ip,op,file)
                    log_obj.write(log.encode('utf-8'))
                log_obj.close()

                date =  datetime.datetime.now()
                date = date.strftime("%Y-%m-%d %H:%M:%S")
                send_message = u"\n时间:%s\nip:%s\n内容:有文件发生添加/删除/修改/权限变更操作,请查收公司邮箱.或查看%s /var/log/file_monit.log!" % (date,";".join(ip_list),local_ip)
                for mobile in mobile_list:
                    send_sms(mobile=mobile,message=send_message)
                send_mail(mail_list,"\n".join(mail_data))

            mail_data = []
            data = []
            time.sleep(1)

if __name__ == '__main__':
    main()

