#!/usr/bin/env python
#encoding=utf-8

import time

def Auth(password):
    ''' 默认认证模式：当前月日+1，如8月20日 --> 0821 '''
    tm = time.localtime()
    tm_pw = '%02d%02d' % (tm.tm_mon, tm.tm_mday+1)
    if tm_pw == password:
        return True
    else:
        return False
