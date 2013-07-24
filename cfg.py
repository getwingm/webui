#!/usr/bin/env python
#encoding=utf-8

''' 本模块包含app的配置参数 '''

import os

app_dir = os.path.dirname(__file__)
static_dir = os.path.join(app_dir, 'static')
template_dir = os.path.join(app_dir, 'templates')

app_title = u'XHK-II(61850-XX)装置参数配置工具'
