#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0, max_connections=80)
r = redis.Redis(connection_pool=pool)
