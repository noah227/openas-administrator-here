# -*- coding: utf-8 -*-
# CREATED: 2023/7/17
# AUTHOR : NOAH YOUNG
# EMAIL  : noah227@foxmail.com

import argparse
import ctypes
import os
import subprocess
import sys
from configparser import ConfigParser


class Runner:
    def __init__(self, cwd=r"E:\Downloads", exe=None):
        """
        :param cwd: 执行路径
        :param exe: 执行程序cmd/wt
        """
        self.cwd = cwd
        self.exe = exe
        pass

    @staticmethod
    def ensureAdmin():
        if ctypes.windll.shell32.IsUserAnAdmin():
            return True
        else:
            args = " ".join([*sys.argv[1:], "-rp", os.path.dirname(__file__)])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, args, None, 1)
            return False
        pass

    @staticmethod
    def __loadConfig():
        cp = ConfigParser()
        cp.read("run.ini", encoding="utf8")
        return cp
        pass

    def run(self):
        cp = ConfigParser()
        cp.read(os.path.join(_args.get("rawPath"), "run.ini"), encoding="utf8")
        executable = cp[self.exe]["executable"]
        if executable:
            subprocess.Popen(executable, shell=True, cwd=self.cwd)
        else:
            print("可执行程序路径不存在，请检查配置文件")
            os.system("pause")


def initArgs():
    parser = argparse.ArgumentParser("oaah")
    # run / reg 执行动作，注册/反注册或者运行，程序内部使用
    parser.add_argument("-a", "--action", default="run", choices=("run", "reg",))
    # 当前程序执行路径，程序内部使用
    parser.add_argument("-p", "--path", default="", help="cwd")
    # 执行程序时的具体配置对象，可以是cmd/wt/..
    parser.add_argument("-e", "--execute", default="cmd", choices=("cmd", "wt"))
    # 执行注册/反注册 reg/unreg
    parser.add_argument("-rt", "--regType", default="", choices=("reg", "unreg",))
    # 用来作为本程序路径的中间传递的（因为开subprogress会丢失当前路径）
    parser.add_argument("-rp", "--rawPath", default="")
    return parser.parse_args().__dict__
    pass


def __start(args):
    action = args.get("action")
    if action == "run":
        path = args.get("path")
        execute = args.get("execute")
        Runner(path, execute).run()
    elif action == "reg":
        from utils import RegUtils
        rt = args.get("regType")
        if rt == "reg":
            executable = os.path.join(os.path.dirname(__file__), "oaah.exe")
            RegUtils().reg(executable)
        elif rt == "unreg":
            RegUtils().unReg()
        pass
    pass


if __name__ == '__main__':
    # print("___________________")
    # print(sys.argv)
    # os.system("pause")
    _args = initArgs()
    if Runner().ensureAdmin():
        __start(_args)
