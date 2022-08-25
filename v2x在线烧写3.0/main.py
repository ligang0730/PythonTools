# -*- coding: utf-8 -*-
import os
import sys
import threading
import time
import paramiko
import json
import struct
import random
import tarfile
import libconf

from socket import *
from pynng import Pair0, Pair1
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QEventLoop, QTimer, QStringListModel
from main_form import Ui_Form
from icon import *

class itemfileinfo:
    def __init__(self, macaddr, ipaddr):
        self.macaddr = macaddr
        self.ipaddr = ipaddr
    def __repr__(self):
        return "%17s    %15s" % (self.macaddr, self.ipaddr)

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
        self.rootpath = os.getcwd()
        curpath = self.rootpath + "/file/"
        os.chdir(curpath)
        self.textEdit.setStyleSheet("background:#ffffff")
        self.listView.setStyleSheet("background:#ffffff")
        self.setWindowIcon(QtGui.QIcon(':/logo.ico'))
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        showlist = []
        self.fileinfo = itemfileinfo('', '')
        self.listmodel = QStringListModel(self)
        self.listmodel.setStringList(showlist)
        self.listView.setModel(self.listmodel)
        self.t5_RunStatus = True
        self.firmVer = self.platver = self.curfirmVer = self.curplatver = ''
        self.curfirmId = self.curplatId = 0
        self.platverNum = 0
        #self.progressBar.setValue(0)

    def outputWritten(self, text):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

    def getBaseInfo(self):
        name = self.lineEdit_name.text()
        passwd = self.lineEdit_pass.text()
        devip = self.lineEdit_devip.text()
        return name, passwd, devip

    def ssh_link(self):
        name = self.lineEdit_name.text()
        passwd = self.lineEdit_pass.text()
        devip = self.lineEdit_devip.text()
        TryConnNum = 0
        ssh = paramiko.SSHClient()  # 创建一个ssh的客户端，用来连接服务器
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.label_stepshow.setText("设备连接中")
        while True:
            try:
                ssh.connect(hostname=devip ,port=22 ,username=name ,password=passwd ,timeout=5)
                self.label_stepshow.setText("设备连接成功")
                return ssh, passwd
            except:
                try:
                    ssh.connect(hostname=devip, port=22, username=name, password="", timeout=5)
                    self.label_stepshow.setText("设备连接成功")
                    return ssh, ""
                except:
                    TryConnNum += 1
                    if TryConnNum > 60:
                        self.label_stepshow.setText("设备连接失败")
                    time.sleep(1)

    def push_checknet(self):
        self.label_stepshow.setText("开始测试网络")
        devip = self.lineEdit_devip.text()
        if 0 == os.system(u'ping ' + devip):
            self.label_stepshow.setText("网络正常")
        else:
            self.label_stepshow.setText("网络故障")

    def ssh_reboot(self):
        ssh, pwd = self.ssh_link()
        stdin, stdout, stderr = ssh.exec_command("reboot")
        self.label_stepshow.setText("开始重启设备")
        time.sleep(3)
        self.label_stepshow.setText("重启设备成功")
        ssh.close()

    def push_reset(self):
        self.t2 = threading.Thread(target=self.ssh_reboot, args=())
        self.t2.setDaemon(True)
        self.t2.start()

    def push_inquever(self):
        if self.checkBox_sendTool.isChecked() and os.path.exists("upgrade.bin"):
            self.sendAndBootUpgrade()
        nn_hostip = 'tcp://' + str(self.lineEdit_devip.text()) + ':' + str(6620)
        self.nn_pairA = Pair0(dial=nn_hostip, recv_timeout=3000)
        self.getCurVersion()
        self.nn_pairA.close()
        self.getTarVersion()

    def sendJsonTo(self, mode, type, keeplic, valuelist, firmVerName, platVerName):
        inquestDict = {"data": {"mode": mode, "type": type, "keepLicense": keeplic, "value": valuelist,
                                "firmwareVerName": firmVerName, "platformVerName": platVerName}}
        sendmsgjson = json.dumps(inquestDict)
        sendmsg = sendmsgjson.encode('ascii')
        self.nn_pairA.send(sendmsg)

    def recvJsonForm(self):
        try:
            data = self.nn_pairA.recv()
            msg_data = bytes.decode(data)
            tindex = msg_data.rfind('}')
            msg_json = msg_data[:tindex + 1]
            msgdict = json.loads(msg_json)
            #print(msgdict)
            return msgdict
        except:
            return {}

    def getTarVersion(self):
        tar = tarfile.open("versioninfo.tar.bz2", "r:bz2")
        for member in tar.getmembers():
            f = tar.extractfile(member)
            content = f.read()
            data = bytes.decode(content)
            try:
                config = libconf.loads(data)
                self.platver = config['curl']['VersionString']
                self.platverNum = config['curl']['VersionNum']
                break
            except:
                print("目标plarform的版本号读取错误")
        print("目标plarform的版本号: " + self.platver)

    def getCurVersion(self):
        # 检查当前的分区号
        self.sendJsonTo(1, 1, 0, [], self.firmVer, self.platver)
        msgdict = self.recvJsonForm()
        if msgdict['report']['type'] == 1:
            self.curfirmId = msgdict['report']['valueInt']
            self.curfirmVer = str(msgdict['report']['valueString'])
            firmId = str(self.curfirmId) + ' - ' + self.curfirmVer
            self.label_firmid.setText(firmId)
        self.sendJsonTo(1, 2, 0, [], self.firmVer, self.platver)
        msgdict = self.recvJsonForm()
        if msgdict['report']['type'] == 2:
            self.curplatId = msgdict['report']['valueInt']
            self.curplatver = str(msgdict['report']['valueString'])
            platId = str(self.curplatId) + ' - ' + self.curplatver
            self.label_platid.setText(platId)

    #def bootUpgrade(self):
    def sendAndBootUpgrade(self):
        name = self.lineEdit_name.text()
        devip = self.lineEdit_devip.text()
        ssh, pwd = self.ssh_link()

        sshCmd = "ps | grep upgrade | grep -v grep | awk '{print $1}' | xargs kill -9"
        stdin, stdout, stderr = ssh.exec_command(sshCmd)

        trans = paramiko.Transport(sock=(devip, 22))
        trans.connect(username=name, password=pwd)
        sftp = paramiko.SFTPClient.from_transport(trans)
        sftp.put("upgrade.bin", "/opt/platform/bin/upgrade.bin")

        cmd_path = "export LD_LIBRARY_PATH=/lib:/usr/lib:/usr/exlib:/opt/platform/lib:/opt/v2x/lib"
        cmd_upgrade = "cd /opt/platform/bin/ && chmod +x upgrade.bin && ./upgrade.bin &"
        stdin, stdout, stderr = ssh.exec_command(cmd_path + ' && ' + cmd_upgrade)
        sftp.close()

    # def sendAndBootUpgrade(self):
    #     self.t7 = threading.Thread(target=self.bootUpgrade, args=())
    #     self.t7.setDaemon(True)
    #     self.t7.start()

    def ftpUpFile(self, vlist):
        name = self.lineEdit_name.text()
        devip = self.lineEdit_devip.text()
        ssh, pwd = self.ssh_link()
        trans = paramiko.Transport(sock=(devip, 22))
        trans.connect(username=name, password=pwd)
        try:
            sftp = paramiko.SFTPClient.from_transport(trans)
        except:
            print("ftp连接失败")
            return
        print("等待ftp文件上传完成")
        for v in vlist:
            if v == 11:
                self.label_stepshow.setText("开始上传rootfs.tar.bz2")
                sftp.put("rootfs.tar.bz2", "/tmp/cache/rootfs.tar.bz2")
                print("上传rootfs.tar.bz2完成")
            if v == 12:
                self.label_stepshow.setText("开始上传platform.tar.bz2")
                sftp.put("platform.tar.bz2", "/tmp/cache/platform.tar.bz2")
                print("上传platform.tar.bz2完成")
            if v == 13:
                self.label_stepshow.setText("开始上传config.tar.bz2")
                sftp.put("config.tar.bz2", "/tmp/cache/config.tar.bz2")
                print("上传config.tar.bz2完成")
        ssh.close()
        sftp.close()

    def readFtpProgress(self, vlist, fileSizeList):
        i = 0
        while self.t5_RunStatus:
            time.sleep(1)
            self.sendJsonTo(2, vlist[i], 0, fileSizeList, self.firmVer, self.platver)
            msgDict = self.recvJsonForm()
            #self.progressBar.setValue(int(msgDict['report']['valueInt']))
            print("已上传 : " + str(msgDict['report']['valueInt']) + "%")
            if msgDict['report']['type'] == vlist[i] and msgDict['report']['valueInt'] == 100:
                #self.progressBar.setValue(0)
                i += 1
                if i > (len(vlist)-1):
                    self.t5_RunStatus = False
                    return

    def sendStartFtpCmd(self):
        fileSizeList = [0, 0, 0]
        vlist = []

        if self.checkBox_firm.isChecked():
            if os.path.exists("rootfs.tar.bz2"):
                fileSizeList[0] = os.path.getsize("rootfs.tar.bz2")
                vlist.append(11)
            else:
                return
        if self.checkBox_plat.isChecked():
            if os.path.exists("platform.tar.bz2"):
                fileSizeList[1] = os.path.getsize("platform.tar.bz2")
                vlist.append(12)
            else:
                return
        if self.checkBox_conf.isChecked():
            if os.path.exists("config.tar.bz2"):
                fileSizeList[2] = os.path.getsize("config.tar.bz2")
                vlist.append(13)
            else:
                return
        self.sendJsonTo(2, 10, 0, fileSizeList, self.firmVer, self.platver)
        msgdict = self.recvJsonForm()
        if msgdict['report']['type'] == 10 and msgdict['report']['valueInt'] == 1:
            self.t5 = threading.Thread(target=self.readFtpProgress, args=(vlist, fileSizeList, ))
            self.t5.setDaemon(True)
            self.t5.start()
            self.t5_RunStatus = True
            self.ftpUpFile(vlist)

    def readBurnProgress(self, keepLic, burnList):
        for i in range(len(burnList)):
            if burnList[i] == 21:
                name = "firmware"
            if burnList[i] == 22:
                name = "platform"
            if burnList[i] == 23:
                name = "config"
            #self.progressBar.setValue(0)
            self.label_stepshow.setText("正在升级" + name)
            progress = 0
            while True:
                self.sendJsonTo(3, burnList[i], keepLic, [0, self.platverNum, 0], self.firmVer, self.platver)
                msgDict = self.recvJsonForm()
                progress = msgDict['report']['valueInt']
                if progress == 100:
                    #self.progressBar.setValue(0)
                    print("升级" + name + "完成")
                    time.sleep(1)
                    break
                else:
                    #self.progressBar.setValue(progress)
                    print("正在升级" + name + " : " + str(progress) + "%")
                    time.sleep(3)

        if self.checkBox_autoSwitch.isChecked():
            if self.checkBox_firm.isChecked():
                self.sendJsonTo(4, 1, keepLic, [0], self.firmVer, self.platver)
            if self.checkBox_plat.isChecked():
                self.sendJsonTo(4, 2, keepLic, [1], self.firmVer, self.platver)
            if self.checkBox_autoReset.isChecked():
                self.push_reset()

    def sendStartBurnCmd(self):
        keepLic = 1 if self.checkBox_keepLic.isChecked() else 0
        burnList = []
        numList = [0, 0, 0]
        if self.checkBox_firm.isChecked():
            numList[0] = 1
            burnList.append(21)
        if self.checkBox_plat.isChecked():
            numList[1] = 1
            burnList.append(22)
        if self.checkBox_conf.isChecked():
            numList[2] = 1
            burnList.append(23)

        self.sendJsonTo(3, 20, keepLic, numList, self.firmVer, self.platver)
        msgDict = self.recvJsonForm()
        if msgDict['report']['mode'] == 3 \
            and msgDict['report']['type'] == 20 \
            and msgDict['report']['valueInt'] == 1:
            self.readBurnProgress(keepLic, burnList)
        else:
            print("升级失败")

    def startUpgrade(self):
        if self.checkBox_sendTool.isChecked():
            time.sleep(2)
        self.t5_RunStatus = True
        self.firmVer = self.platver = self.curfirmVer = self.curplatver = ''
        self.curfirmId = self.curplatId = 0
        #self.progressBar.setValue(0)

        self.getCurVersion()
        self.getTarVersion()
        self.sendStartFtpCmd()
        while True:
            time.sleep(3)
            if self.t5_RunStatus == False:
                self.sendStartBurnCmd()
                self.nn_pairA.close()
                self.pushButton_start.setEnabled(True)
                return

    def push_start(self):
        self.pushButton_start.setEnabled(False)
        if self.checkBox_sendTool.isChecked() and os.path.exists("upgrade.bin"):
            self.sendAndBootUpgrade()

        nn_hostip = 'tcp://' + str(self.lineEdit_devip.text()) + ':' + str(6620)
        self.nn_pairA = Pair0(dial=nn_hostip, recv_timeout=60000)

        self.t1 = threading.Thread(target=self.startUpgrade, args=())
        self.t1.setDaemon(True)
        self.t1.start()

    def push_firmswitch(self):
        autoSwitch = 1
        nn_hostip = 'tcp://' + str(self.lineEdit_devip.text()) + ':' + str(6620)
        self.nn_pairA = Pair0(dial=nn_hostip, recv_timeout=3000)
        if self.checkBox_autoSwitch.isChecked():
            autoSwitch = 0
        self.sendJsonTo(4, 1, 0, [autoSwitch], self.firmVer, self.platver)
        msgDict = self.recvJsonForm()
        if msgDict['report']['mode'] == 4 and msgDict['report']['type'] == 1:
            if msgDict['report']['valueInt'] == 1:
                tarNum = 1 if (self.curfirmId == 2) else 2
                firmId = str(tarNum) + ' - ' + 'V0.00.00B0'
                self.label_firmid.setText(firmId)
            else:
                firmId = str(self.curfirmId) + ' - ' + self.curfirmVer
                self.label_firmid.setText(firmId)
        self.nn_pairA.close()

    def push_platswitch(self):
        autoSwitch = 0
        nn_hostip = 'tcp://' + str(self.lineEdit_devip.text()) + ':' + str(6620)
        self.nn_pairA = Pair0(dial=nn_hostip, recv_timeout=3000)
        if self.checkBox_autoSwitch.isChecked():
            autoSwitch = 1
        self.sendJsonTo(4, 2, 0, [autoSwitch], self.firmVer, self.platver)
        msgDict= self.recvJsonForm()
        if msgDict['report']['mode'] == 4 and msgDict['report']['type'] == 2:
            if msgDict['report']['valueInt'] == 1:
                tarNum = 1 if (self.curplatId == 2) else 2
                platId = str(tarNum) + ' - ' + self.platver
                self.label_platid.setText(platId)
            else:
                platId = str(self.curplatId) + ' - ' + self.curplatver
                self.label_platid.setText(platId)
        self.nn_pairA.close()

    def startFindIp(self):
        mcast_group_ip = '239.255.255.250'
        mcast_group_port = 37020
        zb_sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        zb_sock.settimeout(3)
        zb_sock.bind(("", 7788))
        msg_dist = {"id": "", "deviceName": "", "serialNumber": "", "macAddress": "", "ipAddress": ""}
        sendmsgjson = json.dumps(msg_dist)
        zb_sock.sendto(sendmsgjson.encode('ascii'), (mcast_group_ip, mcast_group_port))

    def startRecvFindIp(self):
        mcast_group_ip = '239.255.255.250'
        mcast_group_port = 7789
        zb_sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        zb_sock.bind(("", mcast_group_port))
        mreq = struct.pack("=4sl", inet_aton(mcast_group_ip), INADDR_ANY)
        zb_sock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)
        zb_sock.settimeout(2)
        self.listmodel.removeRows(0, self.listmodel.rowCount())
        while True:
            try:
                message, addr = zb_sock.recvfrom(1024)
                msg_data = bytes.decode(message)
                tindex = msg_data.rfind('}')
                msg_json = msg_data[:tindex + 1]
                dict_json = json.loads(msg_json)
                self.fileinfo.macaddr = dict_json['macAddress']
                self.fileinfo.ipaddr = dict_json['ipAddress']
                if self.fileinfo.ipaddr.find('192.168.42.10') >= 0:
                    pass
                else:
                    row = self.listmodel.rowCount()
                    self.listmodel.insertRow(row)
                    self.listmodel.setData(self.listmodel.index(row), str(self.fileinfo))
            except:
                self.pushButton_findip.setText("搜索IP")
                self.pushButton_findip.setEnabled(True)
                break

    def push_findip(self):
        self.t3 = threading.Thread(target=self.startFindIp, args=())
        self.t3.setDaemon(True)
        self.t3.start()

        self.t4 = threading.Thread(target=self.startRecvFindIp, args=())
        self.t4.setDaemon(True)
        self.t4.start()

        self.pushButton_findip.setText("正在搜索...")
        self.pushButton_findip.setEnabled(False)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
