#!/bin/sh

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin

export PATH

. ~/.bashrc

export LANG=C


find /usr/local/nginx/logs -type f  -name "*access*.log"|xargs -t -i mv {}  /usr/local/nginx/logs/historylog;

/etc/init.d/nginx  reload

sleep 5s;
cd  /usr/local/nginx/logs/historylog  &&  find ./ -type f  -name "*.log"|xargs -I {}  tar czvfP {}`date +%Y-%m-%d`.tar.gz {} --remove-files ;

echo "0" > /tmp/mobile_tmp

exit 0
