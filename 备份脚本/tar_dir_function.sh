#!/bin/sh
# 压缩备份指定目录下所有目录文件
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
. ~/.bashrc
export LANG=C
    #第一个参数传递需要备份的目录路径
    #第二个参数传递需要备份到的给分路径
tar_dir_function(){
if [ $# != 2 ] ; then    #判断参数个数是否为两个
        echo 'please input like tar_dir_function(/path,/backup/path)';
        exit 1;
else
        source_path=$0
        backup_path=$1
        cd $source_path
        tardirlist=`ls -l|grep ^d|awk '{print $NF}'`
        Time=`date +%Y-%m-%d`
        #备份目录不存在就创建一个
        backupdir=$backup_path/$Time
        if [ !  -d  $backupdir ]; then
                mkdir -p $backupdir
        fi
        for tdir in $tardirlist
        do
            echo "begin  tar.gz   $backupdir/$tdir$Time" 
            #tar -czf  $backupdir/$tdir$Time.tar.gz  $tdir
            echo "$backupdir/$tdir$Time.tar.gz"
            echo "$tdir"
        done
fi
}
exit 0；

