#!/bin/bash
# check if process exists
if [ "`ps aux|grep activemq|grep -v grep|wc -l`" -eq 0  ];then
  echo "check activemq failed"
  exit 1
fi

# check memory reach limit
MEMORY_RESTART_LIMIT=90
usage=`cat /sys/fs/cgroup/memory/memory.usage_in_bytes`
total=`cat /sys/fs/cgroup/memory/memory.limit_in_bytes`
percentage=`python -c "print int(round(${usage}.0/${total}*100))"`

if [ $percentage -ge $MEMORY_RESTART_LIMIT ]; then
  echo "check memory fail"
  exit 1
else
  echo "success"
  exit 0
fi

