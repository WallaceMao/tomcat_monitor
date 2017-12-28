#coding=utf-8
import subprocess
import time
import logging
import requests
import ConfigParser

# 对tomcat应用进行健康检查，连续三次健康url检查失败，则执行重启操作

# 读取配置文件，设置全局基本配置
cf = ConfigParser.ConfigParser()
cf.read('./config')

# global variables
# log日志文件所在的位置
log_file = cf.get('log', 'log_file')
# log日志的输出level
log_level = getattr(logging, cf.get('log', 'log_level'), 'INFO')
# 健康度检查的url
check_url = cf.get('base', 'check_url')
#check_url = 'http://localhost:8080/task/login/authAjax'
# 最大重试次数，当健康度检查的url连续不成功达到最大重试次数时，执行重启等操作
retry_times = cf.getint('base', 'retry_times')
# 每次健康度检查之间的间隔
delay_sec = cf.getint('base', 'delay_sec')
# 服务重启后，重新开始健康度检查的时间间隔
delay_sec_restart = cf.getint('base', 'delay_sec_restart')
# http请求的超时时间，请求响应的时长超过该事件，即认定健康度检查失败
timeout = cf.getint('base', 'timeout')
# 健康度检查失败时所需要执行的脚本
fail_command = cf.get('base', 'fail_command')

# basic config
logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# local variables
fail_times = 0

# monitor script
while 1:
  hasError = False
  r = None 
  try:
    logging.debug('health checking: ' + check_url)
    r = requests.get(check_url, timeout=timeout)
    if r.status_code != 200:
      logging.warning('request is not 200: %d' % (r.status_code))
      hasError = True
  except requests.exceptions.RequestException as e:
    logging.warning(e)
    hasError = True 
  
  if hasError:
    logging.debug('check url error: ' +  check_url)
    fail_times += 1
    if fail_times >= retry_times:
      logging.error('reach max try times, trying to restart application...')
      # restart server
      logging.debug('trying to restart server')
      resp = subprocess.call(['bash', fail_command])
      logging.info('=================')
      logging.debug('command response after restart server: %s' % resp)
      fail_times = 0
      time.sleep(delay_sec_restart) 
    else:
      logging.debug('not reach max retry times, try again later...')
      time.sleep(delay_sec)
  else:
    logging.debug('check url success:' + check_url)
    fail_times = 0
    time.sleep(delay_sec)
