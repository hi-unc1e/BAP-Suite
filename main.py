# encoding:utf-8
import argparse
from argparse import RawTextHelpFormatter
from core import Brute

if __name__ == '__main__':
    BANNER = """    Basic Auth Parallelled brute-force Suite. 
    For Legal Use Only!
    ____  ___    ____     _____       _ __                   
   / __ )/   |  / __ \   / ___/__  __(_) /____   
  / __  / /| | / /_/ /   \__ \/ / / / / __/ _ \  
 / /_/ / ___ |/ ____/   ___/ / /_/ / / /_/  __/  
/_____/_/  |_/_/       /____/\__,_/_/\__/\___/   
Author: Unc1e   http://unc1e.cn
Repo: https://github.com/hi-unc1e
"""
    parser = argparse.ArgumentParser(description=BANNER, formatter_class=RawTextHelpFormatter) # 支持换行的banner
    parser.add_argument('-u', '--url', dest='url', type=str, help='[Target URL] of your HTTP Basic Auth')
    parser.add_argument('-r', dest='req_filepath', type=str, help='[Path of your HTTP Request File] of your HTTP Basic Auth, .txt in common')
    parser.add_argument('-t', '--threads', dest='threads_number', type=int, default=5, help='[Threads] of Brute Force')
    #TODO 添加自定义字典功能 -w
    args = parser.parse_args() # 通过args.request来引用变量
    if args.url != None:
        b = Brute.Brute(args.url, args.threads_number)
        b.run()
    else:
        parser.print_help()
    # 参数初始化





