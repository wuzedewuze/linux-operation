wget https://www.python.org/ftp/python/2.7/Python-2.7.tgz
tar -xzvf Python-2.7.tgz
cd  Python-2.7
./configure --prefix=/usr/local/wyproject/github/temp/python2.7
make && make install 

cd /usr/local/wyproject/github/temp/python2.7
wget https://bootstrap.pypa.io/get-pip.py
./python get-pip.py


/etc/supervisord.conf 
vim supervisor.conf                       # 修改 supervisor 配置文件，添加 gunicorn管理 

[program:tomcat_file_monit]
command=/usr/bin/python /opt/python_project/file_change_monit/main.py
autostart=true
startsecs=10
startretries=3
user=root
log_stdout=true
log_stderr=true
logfile=/var/log/file_change_monit.log
logfile_maxbytes=1MB
logfile_backups=10



