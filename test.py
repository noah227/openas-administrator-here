# -*- coding: utf-8 -*-
# CREATED: 2023/7/17
# AUTHOR : NOAH YOUNG
# EMAIL  : noah227@foxmail.com

import argparse
from configparser import ConfigParser


def configTest():
    cp = ConfigParser()
    cp.read("./run.ini", encoding="utf8")
    extended = cp["cmd"]["extended"]
    if extended:
        print(999)
    print(extended, type(extended))
    print(cp)
    pass


if __name__ == '__main__':
    # parser = argparse.ArgumentParser("*.exe")
    # parser.add_subparsers(title="hhh")
    # # run / reg 执行动作，注册/反注册或者运行，程序内部使用
    # parser.add_argument("-a", "--action", default="run")
    # # 当前程序执行路径，程序内部使用
    # parser.add_argument("-p", "--path", default="")
    # # 执行程序时的具体配置对象，可以是cmd/wt/..
    # parser.add_argument("-e", "--execute", default="cmd")
    # args = parser.parse_args().__dict__
    # print(args)
    # configTest()
    print(int("true"))
    pass
