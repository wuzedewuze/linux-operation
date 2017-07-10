#!/bin/sh
# shell name:  cut_tomcatLog.sh
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
. ~/.bashrc
export LANG=C

time=$(date +%Y-%m-%d)
find /var/project_log -name catalina.out|xargs -t -I {} sh -c "cp {} {}.$time && >{}"

exit 0;
