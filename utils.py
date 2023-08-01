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
        self.supportedExecutableList = ["cmd", "wt"]
        self.config = self.loadConfig()
        self.keyBase = "oaah"
        self.shellBase = "Directory\\Background\\shell"
        pass

    def loadConfig(self):
        cp = ConfigParser()
        cp.read("./run.ini", encoding="utf8")
        config = {
            "default": {
                "use": cp["default"]["use"],
            }
        }
        for item in self.supportedExecutableList:
            config[item] = RegUtils.getItemConfig(cp, item)

        print(config)
        return config

    @staticmethod
    def getItemConfig(cp: ConfigParser, key: str):
        """
        获取单个配置项的配置数据
        """
        # ["attrName", "getBoolValue"]
        items = [
            ["enabled", True],
            ["name", False],
            ["executable", False],
            ["extended", True]
        ]
        config = {}
        for attrName, getBooleanValue in items:
            v = cp[key][attrName]
            config[attrName] = RegUtils.getBooleanValue(v) if getBooleanValue else v
        return config

    @staticmethod
    def getBooleanValue(v: str):
        try:
            return int(v) > 0
        except ValueError as e:
            print(e)
            return False
        pass

    # 注册
    def reg(self, executable):
        print("开始注册")
        os.system("pause")
        config = self.config

        for k, v in config.items():
            # 禁用项需要检查清除无用的注册项
            if not v.get("enabled"):
                error = self.__unReg(k, showError=False)
                if not error:
                    print(f"已解除未启用的注册项：{k}")
                continue
            # 跳过不支持的配置
            if k not in self.supportedExecutableList:
                continue
            # 注册配置
            if exe := v.get("executable"):
                self.__reg(k, v, exe, executable)
        print(f"已完成右键注册！注册路径为：{self.keyBase}.*")
        print("双击unreg.bat可取消注册")
        os.system("pause")
        pass

    def __reg(self, k, v, exe, executable):
        key = f"{self.keyBase}.{k}"
        valueExList = [
            ["Icon", v.get("icon") or executable or exe]
        ]
        # Extended Verbs标记
        if v.get("extended"):
            valueExList.append(["extended", ""])

        self.regKey(
            (winreg.HKEY_CLASSES_ROOT, f"{self.shellBase}\\{key}"),
            v.get("name"), valueExList=valueExList
        )
        self.regKey(
            (winreg.HKEY_CLASSES_ROOT, f"{self.shellBase}\\{key}\\command"),
            f"{executable} -a run -p %V -e {k}",
        )
        pass

    # 反注册
    def unReg(self):
        config = self.config
        unRegAllPassed = True
        for k, v in config.items():
            if k in self.supportedExecutableList:
                error = self.__unReg(k)
                if error and unRegAllPassed:
                    unRegAllPassed = False
        print("已解除注册！" if unRegAllPassed else "解除过程中出现了错误！")
        os.system("pause")
        pass

    def __unReg(self, k, showError=True):
        """
        解除单个注册表配置项
        :return: 是否出现了错误
        """
        try:
            key = f"{self.keyBase}.{k}"
            # 要先移除subKeys才能移除父级key
            self.unRegKey((winreg.HKEY_CLASSES_ROOT, f"{self.shellBase}\\{key}\\command"))
            self.unRegKey((winreg.HKEY_CLASSES_ROOT, f"{self.shellBase}\\{key}"))
            return False

        except Exception as e:
            if showError:
                print(f"解除注册时失败，解除项为：HKEY_CLASSES_ROOT\\{self.shellBase}\\{self.keyBase}.{k}")
                print("删除失败的原因为：", e)
                print("如有需要，请检查后手动进行删除")
            return True
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
    def unRegKey(key):
        winreg.DeleteKey(*key)
        pass


if __name__ == '__main__':
    # if ensureAdmin():
    #     RegUtils().reg()
    pass
