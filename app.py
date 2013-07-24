#!/usr/bin/env python
#encoding=utf-8

import time, json

from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.web.static import File
from twisted.internet import reactor
from mako.template import Template
from mako.lookup import TemplateLookup
# 导入本应用的配置参数
import cfg
# 创建并加载模板
lookup = TemplateLookup(directories=[cfg.template_dir], input_encoding='utf-8', output_encoding='utf-8')
tpl_login = lookup.get_template('login.html')
tpl_runstat = lookup.get_template('runstat.html')
# 导入model包定义的业务函数
from models.auth import Auth
from models.runstat import getRunstat

# 创建导航栏信息
navi = [(u'runstat', u'运行状态'), (u'parameter', u'参数配置'), (u'loginfo', u'日志信息'),]
# 创建页面公共信息
page_share = {'app_title':cfg.app_title, 'navi':navi}

class Runstat(Resource):
    ''' 运行状态 '''
    isLeaf = True
    page = {'page_title' : u'运行状态'}; page.update(page_share)
    def render_POST(self, request):
        request.setHeader("content-type", "text/plain")
        return 'POST data: ' + request.content.getvalue()
    def render_GET(self, request):
        request.setHeader("content-type", "text/html")
        self.page['stat'] = getRunstat()
        return tpl_runstat.render(page=self.page)
    

class Parameter(Resource):
    ''' 参数配置 '''
    isLeaf = True
    def render_POST(self, request):
        request.setHeader("content-type", "text/plain")
        return 'POST data: ' + request.content.getvalue()
    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        return 'GET Request'
    

class Loginfo(Resource):
    ''' 日志信息 '''
    isLeaf = True
    def render_POST(self, request):
        request.setHeader("content-type", "text/plain")
        return 'POST data: ' + request.content.getvalue()
    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        return 'GET Request'
    

class LoginPage(Resource):
    isLeaf = True
    page = {'page_title' : u'用户登录'}; page.update(page_share)
    def render_POST(self, request):
        session = request.getSession()
        # print request.args
        if Auth(request.args['inputPassword'][0]):
            session.isLogin = True
            request.redirect("runstat")
        else:
            session.isLogin = False
            request.redirect("loginpage?failed=1")
        return ''
    def render_GET(self, request):
        request.getSession().expire()
        request.setHeader("content-type", "text/html")
        self.page['isFailed'] = request.args.get('failed')
        return tpl_login.render(page=self.page)

class GetTime(Resource):
    isLeaf = True
    def render_GET(self, request):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

class GetRunstat(Resource):
    isLeaf = True
    def render_GET(self, request):
        request.setHeader("content-type", "application/json")
        return json.dumps(getRunstat())

class Root(Resource):
    ''' 首页，同时第一级URL路由 '''
    url = {'static':File(cfg.static_dir), 'loginpage':LoginPage(), 'runstat':Runstat(), 'parameter':Parameter(), 'loginfo':Loginfo()}
    url.update({'gettime':GetTime(), 'getrunstat':GetRunstat()})
    def getChild(self, name, request):
        if name in ('static', 'gettime'):
            return self.url.get(name)
        session = request.getSession()
        if not getattr(session, 'isLogin', False):
            return self.url.get('loginpage')
        else:
            return self.url.get(name, self)
    def render_GET(self, request):
        request.redirect("runstat")
        return ''

root = Root()
factory = Site(root)
reactor.listenTCP(8880, factory)
reactor.run()
