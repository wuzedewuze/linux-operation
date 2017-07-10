# coding:utf-8
# 备份策略： 
# 1、每月同步sftp目录到backup目录中
# 2、删除sftp目录中 30天前的文件
# 3、根据日期压缩备份backup目录、不保留当前目录文件
import subprocess
# rsync需要备份的目录
# 用check_call方法，返回值不为0的时候 会抛出异常，下面代码不会执行。
print "同步到备份目录"
subprocess.check_call("rsync -ave 'ssh -p 22' /home/dir /home/dir-backup -b", shell=True)
print "完成同步，开始删除30天以前的文件开始"
# 删除30天以前的文件
subprocess.check_call("find /home/dir -type f -mtime +30|xargs rm -f", shell=True)
print "删除30天以前的文件结束 开始压缩备份sftp目录"
# 压缩备份sftp目录
subprocess.check_call("date=`date +%Y%m%d`&&cd /home/dir-backup&&tar -czf  dir${date}.tar.gz dir --remove-files", shell=True)
print "压缩备份sftp目录结束"
