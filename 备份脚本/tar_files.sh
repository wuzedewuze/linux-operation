#!/bin/sh
# shell name:  tar_files.sh
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
. ~/.bashrc
export LANG=C

log_path=/var/project_log

find $log_path  -type f -mtime +7 ! -name "*.tar.gz"|xargs  -I {}  tar czvfP {}.tar.gz {} --remove-files 


exit 0;

