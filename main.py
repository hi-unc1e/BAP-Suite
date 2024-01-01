# encoding:utf-8
import argparse
from argparse import RawTextHelpFormatter
from core import Brute, Bro_Brute

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
    parser.add_argument('target', dest='url', type=str, help='Target URL for the operation')

    parser.add_argument('-u', '--user', dest='user', type=str, help='[UserName] admin by default')
    parser.add_argument('-U', '--username-file', dest='username_file', type=str, help='[UserName] wordlist filepath')

    parser.add_argument('-p', '--pass', dest='user', type=str, help='[Password]')
    parser.add_argument('-P', '--password-file', dest='password_file', type=str, help='[Password] wordlist filepath, top_100_list by_default')

    parser.add_argument('-n', '--num-of-threads', dest='threads_number', type=int, default=1, help='[Threads] of Brute Force')

    #TODO 添加自定义字典功能 -w
    args = parser.parse_args() # 通过args.request来引用变量
    url = args.target
    if url and url != "":
        # u + p
        Bro_Brute.b(args)

    else:
        parser.print_help()
