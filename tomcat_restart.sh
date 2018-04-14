#/bin/bash
# kill tomcat process
serverpath=$1
echo tomcat server $serverpath is restarting
serverid=`ps -ef | grep "$serverpath" | grep "org.apache.catalina.startup.Bootstrap" | awk '{print $2}'`
echo server PID is $serverid
if [ "$serverid" != "" ]; then
  echo begin to kill $serverid
  kill -9 $serverid
fi
sleep 5
echo begin to start
cd /usr/local/$serverpath/bin
bash startup.sh
