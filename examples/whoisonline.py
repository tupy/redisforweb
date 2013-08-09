#!/usr/env/python
# Original: http://www.lukemelia.com/blog/archives/2010/01/17/redis-in-practice-whos-online/

import time
import redis

from datetime import datetime, timedelta

redis = redis.StrictRedis()

def keys_in_last_5_minutes():
  now = datetime.now()
  times = [now + timedelta(minutes=-n) for n in range(0, 5)]
  return [key(t) for t in times]

def key(dt=None):
  dt = dt or datetime.now()
  return "online:%s" % dt.strftime('%Hh%M')


def track_user_id(id):
  redis.sadd(key(), id)


def online_user_ids():
  return redis.sunion(*keys_in_last_5_minutes())


def online_friend_ids(interested_user_id):
  redis.sunionstore("online_users", *keys_in_last_5_minutes())
  return redis.sinter("online_users", "user:%d:friends" % interested_user_id)


if __name__ == '__main__':

  # setup
  uid = 10
  redis.sadd("user:%d:friends" % uid, 11, 12, 15)
  
  # tracking
  track_user_id(11)
  track_user_id(13)
  
  print "Online users: %s" % ','.join(online_user_ids())
  print "Online friends of %d: %s" % (uid, ','.join(online_friend_ids(uid)))



