#/bin/bash
# kill tomcat process
serverpath=$1
echo tomcat server $serverpath is restarting
serverid=`ps -ef | grep "$serverpath" | grep -v grep | grep -v ONEAPM_COLLECTOR | awk '{print $2}'`
if [ "$serverid" != "" ]; then
  kill -9 $serverid
fi
sleep 5
cd /usr/local/$serverpath/bin
bash startup.sh
