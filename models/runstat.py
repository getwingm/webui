#!/usr/bin/env python
#encoding=utf-8

import time

def getRunstat():
    ''' 返回运行状态 '''
    tm = time.localtime()
    return {'active':True, 'update_time':tm.tm_sec}
    
