#/bin/bash
nohup python -u health_check.py > output.log 2>&1 </dev/null  &
