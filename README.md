# BAP-Suite
HTTP Basic Auth brute-force Suite

- Based on Python 3
- Parallel Working

## Senario(ZH-CN)
李泽言，一名在996公司上班的网络安全工程师，平时的工作职责之一，就是从外网对自己所在的公司做渗透测试。他渗透的工具很简单：Burp是白嫖的、Xray是社区的、连爆破工具都是用的“超级弱口令检查工具”，屡试不爽——直到有一天，他发现外网不时会出现一些Tomcat、或是其它需要HTTP Basic401认证的web服务，网上有人说可以用Burp的“入侵者模式”来爆破...
看不懂英文的李工，没有耐心去一个一个核对英语名词，他只想快些回去，好上到王者13星，于是随手输了几个弱口令，admin/admin、admin/123456，页面反复弹出认证窗口，“害，无事发生。也是，都0202年了，谁还用HTTP Basic401认证啊。溜了！”于是，李工跟同样是弱口令的admin/admin123失之交臂。
他心想，要是有一款只需要输入漏洞点的工具就好了，于是他告诉新来的实习生，让他在一周内实现一款这样的爆破工具，名字就叫：（`BAP Suite`）`Basic Auth Parallelled brute-force Suite`，要求必足够的好用，对单个目标的爆破要足够快，并且支持自动加载最有🐂🍺的字典，例如：tomcat就用tomcat的专用字典，nagios就用nagios的字典，还有默认的top1w国人专用字典。。。


## Featrue
- ommited


---------
## Progress List
CLI
[X] 读取账号密码字典
[X] `-u`对URL进行401认证的爆破
[ ] 爆破过程支持超时重新爆破
[ ] `-r`对HTTP请求包中的401认证进行爆破

