# -*- coding: utf-8 -*-

import time, os

# execute times
execcount = 2
# execute interval, (seconds)
execinterval = 30

monkeyclickcount = 100

WORKSPACE = os.path.abspath(".")

def getWorkConfig():
    f = open("./.config", "r")
    config = {"phone":'8b639a12',"monkeyclickcount": monkeyclickcount, "execcount": execcount}
    try:
        while True:
            line = f.readline()
            if line:
                line = line.strip()
                linesplit = line.split("：")
                if linesplit.__sizeof__() > 1:
                    if linesplit[0] == 'phone':
                        config['phone'] = linesplit[1]
                    elif linesplit[0] == 'monkeyclickcount':
                        config["monkeyclickcount"] = linesplit[1]
                    elif linesplit[0] == 'execcount':
                        config["execcount"] = linesplit[1]
            else:
                break
    finally:
        f.close()
        print("config : %s" % config)
        return config

def installApk(config):

    phoneAddr = config.get("phone")
    print('准备安装待测试APK')

    if phoneAddr:
        installPhoneApk = "adb -s %s install -r %s\\apk\\app-release.apk" % (phoneAddr, WORKSPACE)
        os.popen(installPhoneApk)
        print("安装成功")


def killTestApp():
    forceStopApp = "adb -s %s shell am force-stop com.fangmi.weilan" % workConfig.get('phone')
    os.popen(forceStopApp)

def fullmonkey(workconfig):
    killTestApp()

    monkeycmd = "adb -s %s shell monkey -p com.fangmi.weilan " \
                "--ignore-timeouts --ignore-crashes --kill-process-after-error " \
                "--pct-touch 35 --pct-syskeys 30 --pct-appswitch 35 --hprof  " \
                "--throttle 100 -v -v -v %s" \
                % (workconfig.get("phone"), workConfig.get("monkeyclickcount"))
    os.popen(monkeycmd)

def createBugreport():
    print("正在生成测试报告")
    bugreport = "adb -s %s shell bugreport > %s\\bugreport.txt" % (workConfig.get("phone"), WORKSPACE)
    os.popen(bugreport)

    print("测试报告已生成")

    '''chkbugreport = "java -jar %s\\chkbugreport.jar %s\\bugreport.txt" % (WORKSPACE, WORKSPACE)
    os.popen(chkbugreport)
    '''

workConfig = getWorkConfig()
installApk(workConfig)
forcount = int(workConfig.get("execcount"))


for i in range(forcount):
    print("执行monkey测试 ,轮数 = %s" % (i + 1))
    fullmonkey(workConfig)
    time.sleep(execinterval)

createBugreport()

print("已完成本轮测试")
input("点击任意键结束")