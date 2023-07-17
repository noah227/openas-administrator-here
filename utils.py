# -*- coding: utf-8 -*-
# CREATED: 2023/7/17
# AUTHOR : NOAH YOUNG
# EMAIL  : noah227@foxmail.com
import ctypes
import os
import sys
import winreg
from configparser import ConfigParser


def ensureAdmin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        return False


class RegUtils:
    def __init__(self):
        self.config = self.loadConfig()
        pass

    @staticmethod
    def loadConfig():
        cp = ConfigParser()
        cp.read("./run.ini", encoding="utf8")
        config = {
            "default": {
                "use": cp["default"]["use"],
            },
            "cmd": {
                "name": cp["cmd"]["name"],
                "executable": cp["cmd"]["executable"]
            },
            "wt": {
                "name": cp["wt"]["name"],
                "executable": cp["wt"]["executable"]
            },
        }
        return config

    # 注册
    def reg(self, executable):
        print("开始注册")
        os.system("pause")
        config = self.config
        keyBase = "openas-administrator-here"
        for k, v in config.items():
            if exe := v.get("executable"):
                key = f"{keyBase}--{k}"
                self.regKey(
                    (winreg.HKEY_CLASSES_ROOT, f"directory\\background\\shell\\{key}"),
                    v.get("name"), valueExList=[
                        ["Icon", v.get("icon") or executable or exe]
                    ]
                )
                self.regKey(
                    (winreg.HKEY_CLASSES_ROOT, f"directory\\background\\shell\\{key}\\command"),
                    f"{executable} -a run -p %V -e {k}",
                )
        print(f"已完成右键注册！注册路径为：{keyBase}--*")
        print("执行main unreg可取消注册")
        os.system("pause")
        pass

    # 反注册
    def unReg(self):
        config = self.config
        for k, v in config.items():
            try:
                key = f"openas-administrator-here--{k}"
                self.unRegKey((
                    winreg.HKEY_CLASSES_ROOT, f"directory\\background\\shell\\{key}"
                ), keyExList=["Icon"])
            except Exception as e:
                print(e)
                pass
        pass

    @staticmethod
    def regKey(key, value, subKey="", regType=winreg.REG_SZ, valueExList=None):
        key = winreg.CreateKey(*key)
        winreg.SetValue(key, subKey, regType, value)
        if valueExList:
            for k, v in valueExList:
                winreg.SetValueEx(key, k, 0, winreg.REG_SZ, v)
        winreg.CloseKey(key)
        pass

    @staticmethod
    def unRegKey(key, keyExList=None):
        key = winreg.CreateKey(*key)
        winreg.DeleteKey(key, "")
        # for k in keyExList:
        #     winreg.DeleteKeyEx(k)
        print("已解除注册！")
        os.system("pause")
        pass


if __name__ == '__main__':
    # if ensureAdmin():
    #     RegUtils().reg()
    pass
