#!/bin/bash
if [ $1 ]; then
  git add .
  git commit -m $1
  git push
  git push mgenius master
else
  git add .
  git commit -m "update - `date '+%Y-%m-%d %T'`"
  git push
  git push mgenius master
fi
