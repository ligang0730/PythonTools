import os
import sys
import threading
import time
import paramiko

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from ssh_form import Ui_Form

admin = ""
password = ""
seriveip = ""
clientip = ""
rootpath = ""

ctrlstate = 0

def ssh_link():
    TryConnNum = 0
    ssh = paramiko.SSHClient()  # 创建一个ssh的客户端，用来连接服务器
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    while True:
        try:
            ssh.connect(
                hostname=clientip,
                port=22,
                username=admin,
                password="",
                timeout=5
            )
            break
        except:
            TryConnNum += 1
            print("..." + str(TryConnNum))
            if TryConnNum > 60:
                print("连接失败")
                exit(-1)
    return ssh

def ssh_linkwithpass():
    TryConnNum = 0
    ssh = paramiko.SSHClient()  # 创建一个ssh的客户端，用来连接服务器
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    while True:
        try:
            ssh.connect(
                hostname=clientip,
                port=22,
                username=admin,
                password=password,
                timeout=5
            )
            break
        except:
            TryConnNum += 1
            print("..." + str(TryConnNum))
            if TryConnNum > 60:
                print("连接失败")
                exit(-1)
    return ssh

def check_result(sftp_client, file):
    try:
        result_file = sftp_client.open(file)
        for line in result_file:
            line = str(line[0:1])
        return int(line)
    except:
        return -1


def startBurn(mode, mmcdev, checklink):
    global ctrlstate
    global rootpath
    ctrlstate = 1
    curpath = rootpath + "/firmware/"
    os.chdir(curpath)
    tftp_exe = curpath + "Tftpd32.exe"
    if os.path.exists(tftp_exe):
        os.system(tftp_exe)
    else:
        print("打开tftp.exe失败")
        exit(-1)

    if checklink:
        # ssh登陆
        ssh = ssh_linkwithpass()
        print("登陆成功")
        if not os.path.exists(curpath + "version.dat"):
            print("缺少version.dat文件")
            exit(-1)
        stdin, stdout, stderr = ssh.exec_command("tftp -gr " + "version.dat" + " " + seriveip)
        ret = len(stderr.read().decode())
        if ret > 0:
            print("tftp 上传通道错误，请检查网线")
            ssh.close()
            exit(-1)
        stdin, stdout, stderr = ssh.exec_command("fw_setenv load_mode yes")
        stdin, stdout, stderr = ssh.exec_command("fw_setenv serverip " + seriveip)
        stdin, stdout, stderr = ssh.exec_command("reboot")
        time.sleep(3)
        ssh.close()

    print("重启，等待重新连接")
    ssh = ssh_link()
    # ftp上传
    trans = paramiko.Transport(
        sock=(clientip, 22)
    )
    trans.connect(
        username=admin,
        password=""
    )
    if not os.path.exists("mksdcard.sh") or not os.path.exists("startBurn.sh"):
        print("缺少shell脚本")
        ssh.close()
        exit(0)
    print("上传脚本")
    try:
        sftp = paramiko.SFTPClient.from_transport(trans)
        sftp.put("mksdcard.sh", "/home/root/mksdcard.sh")
        sftp.put("startBurn.sh", "/home/root/startBurn.sh")
    except:
        print("上传失败")

    curpath = rootpath + "/file/"
    os.chdir(curpath)

    str_mode = bin(mode)
    str_mode = str_mode[::-1]
    #print("str_mode : " + str_mode)
    stdin, stdout, stderr = ssh.exec_command("chmod +x /home/root/mksdcard.sh")
    stdin, stdout, stderr = ssh.exec_command("chmod +x /home/root/startBurn.sh")

    if str_mode[0:1] == '1':
        cmd = "sh /home/root/mksdcard.sh 1" + mmcdev + " >> brun.log"
        print(cmd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        time.sleep(3)

        while True:
            if ctrlstate == 0:
                print("停止")
                exit(-1)
            try:
                sftp_client = ssh.open_sftp()
                result_file = sftp_client.open("Fresult.log")
                for line in result_file:
                    line = str(line[0:1])
                result_ret = int(line)
                sftp_client.close()
                if result_ret == 1:
                    print("分区完成")
                    break
            except:
                time.sleep(3)
                print("分区中...")

    print("正在上传烧写包")
    if str_mode[1:2] == '1':
        if not os.path.exists("u-boot.bin"):
            print("缺少u-boot.bin")
            exit(-1)
        else:
            sftp.put("u-boot.bin", "/tmp/cache/u-boot.bin")
    if str_mode[2:3] == '1':
        if not os.path.exists("rootfs.tar.bz2"):
            print("缺少rootfs.tar.bz2")
            exit(-1)
        else:
            sftp.put("rootfs.tar.bz2", "/tmp/cache/rootfs.tar.bz2")
    if str_mode[3:4] == '1':
        if not os.path.exists("platform.tar.bz2") or not os.path.exists("versioninfo.tar.bz2"):
            print("缺少platform.tar.bz2 or versioninfo.tar.bz2")
            exit(-1)
        else:
            sftp.put("platform.tar.bz2", "/tmp/cache/platform.tar.bz2")
            sftp.put("versioninfo.tar.bz2", "/tmp/cache/versioninfo.tar.bz2")
    if str_mode[4:5] == '1':
        if not os.path.exists("config.tar.bz2"):
            print("缺少config.tar.bz2")
            exit(-1)
        else:
            sftp.put("config.tar.bz2", "/tmp/cache/config.tar.bz2")
    cmd = "sh /home/root/startBurn.sh " + str_mode + mmcdev + " >> brun.log"
    print(cmd)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    time.sleep(3)
    while True:
        if ctrlstate == 0:
            print("停止")
            exit(-1)
        try:
            sftp_client = ssh.open_sftp()
            result_file = sftp_client.open("Sresult.log")
            for line in result_file:
                line = str(line[0:1])
            result_ret = int(line)
            sftp_client.close()
            if result_ret == 1:
                print("烧写完成")
                break
            else:
                print("烧写失败")
                exit(-1)
        except:
            time.sleep(3)
            print("烧写中...")

    stdin, stdout, stderr = ssh.exec_command("fw_setenv load_mode no")

    stdin, stdout, stderr = ssh.exec_command("rm -f /home/root/startBurn.sh")
    stdin, stdout, stderr = ssh.exec_command("rm -f /home/root/mksdcard.sh")
    stdin, stdout, stderr = ssh.exec_command("rm -f /home/root/Sresult.log")
    stdin, stdout, stderr = ssh.exec_command("rm -f /home/root/Fresult.log")

    time.sleep(2)
    #sftp.get("brun.log", rootpath)
    print("烧写成功,请重启设备")
    # stdin, stdout, stderr = ssh.exec_command("reboot")
    sftp.close()
    ssh.close()


def ping(ip):
    result = os.system(u'ping ' + ip)
    if result == 0:
        print("网络正常")
    else:
        print("网络故障")
    return result

def reboot():
    ssh = ssh_link()
    stdin, stdout, stderr = ssh.exec_command("reboot")
    time.sleep(3)
    ssh.close()

class EmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))
        loop = QEventLoop()
        QTimer.singleShot(1000, loop.quit)
        loop.exec_()


class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        global rootpath
        rootpath = os.getcwd()

    def outputWritten(self, text):
        # self.textEdit.clear()
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

    def d_printf(self, msg):
        self.textEdit.moveCursor(QTextCursor.End)
        self.textEdit.append(msg)

    def push_close(self):
        global ctrlstate
        ctrlstate = 0

    def push(self):
        global admin
        global password
        global seriveip
        global clientip
        admin = self.lineEdit_1.text()
        password = self.lineEdit_2.text()
        seriveip = self.lineEdit_3.text()
        clientip = self.lineEdit_4.text()
        t2 = threading.Thread(target=reboot, args=())
        t2.setDaemon(True)
        t2.start()

    def push1(self):
        print("测试网络")
        seriveip = self.lineEdit_4.text()
        ping(seriveip)

    def push2(self):
        global ctrlstate
        ctrlstate = 0

    def push3(self):
        global admin
        global password
        global seriveip
        global clientip
        admin = self.lineEdit_1.text()
        password = self.lineEdit_2.text()
        seriveip = self.lineEdit_3.text()
        clientip = self.lineEdit_4.text()

        if len(admin) == 0:
            print('请填写用户名')
            return
        if len(seriveip) == 0:
            print('请填写服务器ip')
            return
        if len(clientip) == 0:
            print('请填写设备ip')
            return
        mode = 0
        if self.checkBox.isChecked():
            mode = 1
        if self.checkBox_2.isChecked():
            mode |= (1 << 1)
        if self.checkBox_3.isChecked():
            mode |= (1 << 2)
        if self.checkBox_4.isChecked():
            mode |= (1 << 3)
        if self.checkBox_5.isChecked():
            mode |= (1 << 4)
        if mode == 0:
            print("未选择功能")

        mmcdev = " " + str(self.lineEdit.text())
        checknetlink = self.checkBox_6.isChecked()

        t1 = threading.Thread(target=startBurn, args=(mode, mmcdev, checknetlink, ))
        t1.setDaemon(True)
        t1.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
