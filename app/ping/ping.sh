#!/bin/sh


do
ping=`ping -c 1 $i|grep loss|awk '{print $6}'|awk -F "%" '{print $1}'`
if [ $ping -eq 100  ];then
echo ping $i fail
else
echo ping $i ok
fi

x=$(ping -W 1 -c baidu.com 2>/dev/null | grep -E "(PING)|(loss)")
loss=$(echo "$x" | grep "loss" | awk '{printf "%s", substr($6, 1, length($6)-1)}')
if [[ $loss -eq 100 ]]; then
  echo "$x" | grep "PING" | awk '{printf "%s no ping\n", $2}'
else
  echo "$x" | grep "PING" | awk '{printf "%s %s\n", $2, substr($3, 2, length($3)-2)}'
fi


# ping www.baidu.com -c 1 | awk '{print $3}'|grep \(
