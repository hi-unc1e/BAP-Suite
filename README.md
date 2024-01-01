# BAP-Suite
HTTP Basic Auth brute-force Suite

- Based on Python 3
- Parallel Working


## Install
- 安装chromedriver: https://sites.google.com/chromium.org/driver/downloads
- 

## Senario(ZH-CN)
李泽言，一名在996公司上班的网络安全工程师，平时的工作职责之一，就是从外网对自己所在的公司做渗透测试。他渗透的工具很简单：Burp是白嫖的、Xray是社区的、连爆破工具都是用的“超级弱口令检查工具”，屡试不爽——直到有一天，他发现外网不时会出现一些Tomcat、或是其它需要HTTP Basic401认证的web服务，网上有人说可以用Burp的“入侵者模式”来爆破...
看不懂英文的李工，没有耐心去一个一个核对英语名词，他只想快些回去，好上到王者13星，于是随手输了几个弱口令，admin/admin、admin/123456，页面反复弹出认证窗口，“害，无事发生。也是，都0202年了，谁还用HTTP Basic401认证啊。溜了！”于是，李工跟同样是弱口令的admin/admin123失之交臂。
他心想，要是有一款只需要输入漏洞点的工具就好了，于是他告诉新来的实习生，让他在一周内实现一款这样的爆破工具，名字就叫：（`BAP Suite`）`Basic Auth Parallelled brute-force Suite`，要求必足够的好用，对单个目标的爆破要足够快，并且支持自动加载最有🐂🍺的字典，例如：tomcat就用tomcat的专用字典，nagios就用nagios的字典，还有默认的top1w国人专用字典。。。

### Supported Situation
☑️ 若依：https://vue.ruoyi.vip/login


### 原理
- 识别账号密码的输入框
  - 账户名: (`type="text"`OR `first_input_text`) AND `placeholder=账号|用户名|用户|user|username` 
  - 密码: `type="password"` OR `placeholder=密码|password|pass` OR

- 识别验证码
  - [ddddocr](https://github.com/sml2h3/ddddocr)

## Featrue
- ommited


Usage:
<img width="1064" alt="image" src="https://user-images.githubusercontent.com/67778054/164774911-5953e688-163b-4e0f-8e0b-91f89d60690e.png">


---------
## Progress List
CLI

☑️ 读取账号密码字典

☑️ `-u`对URL进行401认证的爆破

☑️ 增加摘要（Digest）认证

❌ 爆破过程支持超时重新爆破

❌ `-r`对HTTP请求包中的401认证进行爆破

-


我希望定位：（1）用户名、（2）密码、（3）验证码的输入框元素、（4）验证码图片的元素、（5）登录框的按钮元素
- 请你寻找最合适的选择器，可以是XPATH，也可以是CSS。
要求：以JSON格式返回，例如
{
"usernameInput": ("<选择器>", "XPATH"),
"passwordInput": ("<选择器>", "CSS"),
"captchaInput": ("<选择器>", "CSS"),
"captchaImg": ("<选择器>", "XPATH"),
"loginBtn": ("<选择器>", "XPATH"),
}
----HTML源代码-----
<div class="boxLogin">
        <dl>
            <dd>
                <div class="s1">
                    账&nbsp;&nbsp;&nbsp;户：</div>
                <div class="s2">
                    <input type="text" id="txtUserName" value="system" class="txt" style="width: 122px;">
                    <span id="errorMsg0" class="errorMsg"></span>
                </div>
            </dd>
            <dd>
                <div class="s3">
                    密&nbsp;&nbsp;&nbsp;码：</div>
                <div class="s4">
                    <input type="password" onpaste="return false;" id="txtUserPwd" value="system" class="txt" style="width: 122px;">&nbsp;<span id="errorMsg1" class="errorMsg"></span>
                </div>
            </dd>
            <dd>
                <div class="s5">
                    验证码：</div>
                <div class="s6">
                    <input type="text" id="txtCode" maxlength="4" class="txt" style="ime-mode: disabled;
                        width: 48px;">
                    <img src="../Ajax/Verify_code.ashx" id="Verify_codeImag" width="70" height="22" alt="点击切换验证码" title="点击切换验证码" style="margin-top: 0px; vertical-align: top; cursor: pointer;" onclick="ToggleCode(this.id, '/Ajax/Verify_code.ashx');return false;">
                    <span id="errorMsg2" class="errorMsg"></span>
                </div>
            </dd>
            <dd>
                <div class="load">
                    <img src="../Themes/Images/Login/loading.gif"></div>
            </dd>
        </dl>
        <div class="s8">
            <input id="Log_Submit" type="button" class="sign" onclick="return CheckUserDataValid();">
        </div>
    </div>

