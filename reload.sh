#!/bin/bash

currpath=$(dirname $(readlink -f $0))                                          #取当前所在位置
ps -ef|grep $currpath/http_web.py|grep -v grep|awk '{print $2}'|xargs kill -9
cd $currpath
nohup /home/wangy/anaconda3/bin/python $currpath/http_web.py >/dev/null 2>&1 &
