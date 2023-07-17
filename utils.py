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
        self.keyBase = "oaah"
        self.shellBase = "Directory\\Background\\shell"
        self.supportedExecutableList = ["cmd", "wt"]
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

        for k, v in config.items():
            if k not in self.supportedExecutableList:
                continue
            if exe := v.get("executable"):
                key = f"{self.keyBase}.{k}"
                self.regKey(
                    (winreg.HKEY_CLASSES_ROOT, f"{self.shellBase}\\{key}"),
                    v.get("name"), valueExList=[
                        ["Icon", v.get("icon") or executable or exe]
                    ]
                )
                self.regKey(
                    (winreg.HKEY_CLASSES_ROOT, f"{self.shellBase}\\{key}\\command"),
                    f"{executable} -a run -p %V -e {k}",
                )
        print(f"已完成右键注册！注册路径为：{self.keyBase}.*")
        print("执行main unreg可取消注册")
        os.system("pause")
        pass

    # 反注册
    def unReg(self):
        config = self.config
        for k, v in config.items():
            if k in self.supportedExecutableList:
                try:
                    key = f"{self.keyBase}.{k}"
                    # 要先移除subKeys才能移除父级key
                    self.unRegKey((winreg.HKEY_CLASSES_ROOT, f"{self.shellBase}\\{key}\\command"))
                    self.unRegKey((winreg.HKEY_CLASSES_ROOT, f"{self.shellBase}\\{key}"))

                except Exception as e:
                    print(f"解除注册时失败，解除项为：HKEY_CLASSES_ROOT\\{self.shellBase}\\{self.keyBase}.{k}")
                    print("删除失败的原因为：", e)
                    print("如有需要，请检查后手动进行删除")
                    pass
        print("已解除注册！")
        os.system("pause")
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
    def unRegKey(key):
        winreg.DeleteKey(*key)
        pass


if __name__ == '__main__':
    # if ensureAdmin():
    #     RegUtils().reg()
    pass
