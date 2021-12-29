# -*- coding: utf-8 -*-

import os
import sys
import threading
import time
import paramiko
import hashlib
import shutil
import win32api,win32con
import json
import difflib
import select
import struct

from pynng import Pair0, Pair1
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QEventLoop, QTimer, QStringListModel
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from ssh_form import Ui_Form
from socket import *

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

        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        #self.rootpath = os.getcwd()
        self.pushButton_relog.setEnabled(False)
        self.pushButton_closeconnect.setEnabled(False)
        self.textEdit.setStyleSheet("background:#ffffff")
        self.listView.setStyleSheet("background:#ffffff")
        self.t1_running = True
        self.t2_running = True

        self.showlist = []
        self.fileinfo = itemfileinfo('', '')
        self.listmodel = QStringListModel(self)
        self.listmodel.setStringList(self.showlist)
        self.listView.setModel(self.listmodel)

    def outputWritten(self, text):
        # self.textEdit.clear()
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

    def showResult(self):
        self.label_bid.setText(self.dict_json['id'])
        list_msg = self.dict_json['msgData']
        #print(list_msg)
        try:
            if int(list_msg[0]['islock']) > 0:
                self.label_status.setText("已锁定")
            else:
                self.label_status.setText("未锁定")
        except:
            pass
        try:
            self.label_deviceId.setText(list_msg[0]['deviceId'])
            self.label_deviceDist.setText(str(list_msg[0]['dist']))
            self.label_lostLv.setText(str(list_msg[0]['diuBaoLv']))
            self.label_long.setText(str(list_msg[0]['longg']))
            self.label_power.setText(str(list_msg[0]['powerr']))
            self.label_delay.setText(str(list_msg[0]['delayy']))
            self.label_index.setText(str(list_msg[0]['recvCnt']))
            self.label_lostCnt.setText(str(list_msg[0]['diuBaoCnt']))
            self.label_sendInt.setText(str(list_msg[0]['hzz']))
        except:
            pass

        try:
            if int(list_msg[1]['islock']) > 0:
                self.label_status_2.setText("已锁定")
            else:
                self.label_status_2.setText("未锁定")
        except:
            pass
        try:
            self.label_deviceId_2.setText(list_msg[1]['deviceId'])
            self.label_deviceDist_2.setText(str(list_msg[1]['dist']))
            self.label_lostLv_2.setText(str(list_msg[1]['diuBaoLv']))
            self.label_long_2.setText(str(list_msg[1]['longg']))
            self.label_power_2.setText(str(list_msg[1]['powerr']))
            self.label_delay_2.setText(str(list_msg[1]['delayy']))
            self.label_index_2.setText(str(list_msg[1]['recvCnt']))
            self.label_lostCnt_2.setText(str(list_msg[1]['diuBaoCnt']))
            self.label_sendInt_2.setText(str(list_msg[1]['hzz']))
        except:
            pass
        try:
            if int(list_msg[2]['islock']) > 0:
                self.label_status_3.setText("已锁定")
            else:
                self.label_status_3.setText("未锁定")
        except:
            pass
        try:
            self.label_deviceId_3.setText(list_msg[2]['deviceId'])
            self.label_deviceDist_3.setText(str(list_msg[1]['dist']))
            self.label_lostLv_3.setText(str(list_msg[2]['diuBaoLv']))
            self.label_long_3.setText(str(list_msg[2]['longg']))
            self.label_power_3.setText(str(list_msg[2]['powerr']))
            self.label_delay_3.setText(str(list_msg[2]['delayy']))
            self.label_index_3.setText(str(list_msg[2]['recvCnt']))
            self.label_lostCnt_3.setText(str(list_msg[2]['diuBaoCnt']))
            self.label_sendInt_3.setText(str(list_msg[2]['hzz']))
        except:
            pass

    def startVxtest(self):
        self.firstxh = self.lineEdit_xh.text()

        TryConnNum = 0
        self.sshSock = paramiko.SSHClient()  # 创建一个ssh的客户端，用来连接服务器
        self.sshSock.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        while self.t1_running:
            try:
                self.sshSock.connect(
                    hostname=self.HOST_IP,
                    port=22,
                    username="root",
                    password="*Ctfo002314*",
                    timeout=5
                )
                print("ssh登录成功")
                break
            except:
                TryConnNum += 1
                print("dengluzhong..." + str(TryConnNum))
                if TryConnNum > 9:
                    print("ssh登录失败")
                    exit(-1)
        cmd_path = "export LD_LIBRARY_PATH=/lib:/usr/lib:/usr/exlib:/opt/platform/lib:/opt/v2x/lib"
        cmd_vxtest = "cd /opt/platform/bin/ && ./vxtest.bin tst"
        stdin, stdout, stderr = self.sshSock.exec_command(cmd_path + " && " + cmd_vxtest)

        while self.t1_running:
            time.sleep(1)

    def killtest(self):
        cmd_psvxtest = "ps | grep vxtest.bin | grep -v grep | awk '{print $1}'"
        cmd_killvxtest = "ps | grep vxtest.bin | grep -v grep | awk '{print $1}' | xargs kill -9"
        while True:
            stdin, stdout, stderr = self.sshSock.exec_command(cmd_psvxtest)
            if len(stdout.read()) == 0:
                break
            else:
                stdin, stdout, stderr = self.sshSock.exec_command(cmd_killvxtest)

    def runtest(self):
        cmd_path = "export LD_LIBRARY_PATH=/lib:/usr/lib:/usr/exlib:/opt/platform/lib:/opt/v2x/lib"
        #cmd_vxtest = "cd /opt/platform/bin/ && ./vxtest.bin tst" + str(self.firstxh)
        cmd_psvxtest = "ps | grep vxtest.bin | grep -v grep | awk '{print $1}'"
        while True:
            stdin, stdout, stderr = self.sshSock.exec_command(cmd_psvxtest)
            if len(stdout.read()) > 0:
                time.sleep(2)
            else:
                stdin, stdout, stderr = self.sshSock.exec_command(cmd_path + " && " + cmd_vxtest)

    def msgRecv(self):
        time.sleep(3)
        self.dict_json = ""
        PORT = 6610
        message = "irqmsg"
        timeout1 = 0
        #self.nn_pairA = nnpy.Socket(nnpy.AF_SP, nnpy.PAIR)
        self.nn_pairA = Pair0()
        nn_hostip = 'tcp://' + str(self.HOST_IP) + ':' + str(PORT)
        #print(nn_hostip)
        #self.nn_pairA.connect(nn_hostip)
        self.nn_pairA.dial(nn_hostip)
        print("nn_pairA connect")
        while self.t2_running:
            data = self.nn_pairA.recv()
            msg_data = bytes.decode(data)
            if (msg_data.find('repond') >= 0):
                print(msg_data)
            else:
                tindex = msg_data.rfind('}')
                msg_json = msg_data[:tindex+1]
                self.dict_json = json.loads(msg_json)
                #print(self.dict_json)
                self.showResult()

    def push_udpconnect(self):
        self.t5_running = False
        self.t6_running = False
        self.HOST_IP = self.lineEdit_ip.text()

        self.t1_running = True
        self.t1 = threading.Thread(target=self.startVxtest, args=())
        self.t1.setDaemon(True)
        self.t1.start()

        self.t2_running = True
        self.t2 = threading.Thread(target=self.msgRecv, args=())
        self.t2.setDaemon(True)
        self.t2.start()

        self.pushButton_connect.setEnabled(False)
        self.pushButton_relog.setEnabled(True)
        self.pushButton_closeconnect.setEnabled(True)

    def push_lenset(self):
        message = "l " + str(self.lineEdit_len.text()) + '\0'
        self.nn_pairA.send(message.encode('ascii'))

    def push_powset(self):
        message = "p " + str(self.lineEdit_pow.text()) + '\0'
        self.nn_pairA.send(message.encode('ascii'))

    def push_hzset(self):
        message = "h " + str(self.lineEdit_hz.text()) + '\0'
        self.nn_pairA.send(message.encode('ascii'))

    def push_relog(self):
        message = "r " + str(self.lineEdit_xh.text()) + '\0'
        self.nn_pairA.send(message.encode('ascii'))

    def push_udpclose(self):
        self.killtest()
        self.t1_running = False
        self.t2_running = False
        self.pushButton_connect.setEnabled(True)
        self.pushButton_relog.setEnabled(False)
        self.pushButton_closeconnect.setEnabled(False)

    def startFindIp(self):
        mcast_group_ip = '239.255.255.250'
        mcast_group_port = 37020
        zb_sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        zb_sock.settimeout(3)
        zb_sock.bind(("", 7788))
        msg_dist = {"id":"","deviceName":"","serialNumber":"","macAddress":"","ipAddress":""}
        sendmsgjson = json.dumps(msg_dist)
        #while self.t5_running:
        zb_sock.sendto(sendmsgjson.encode('ascii'), (mcast_group_ip, mcast_group_port))

    def startRecvFindIp(self):
        mcast_group_ip = '239.255.255.250'
        mcast_group_port = 7789
        zb_sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        #local_ip = socket.gethostbyname(gethostname())
        zb_sock.bind(("", mcast_group_port))
        mreq = struct.pack("=4sl", inet_aton(mcast_group_ip), INADDR_ANY)
        zb_sock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)
        zb_sock.settimeout(1)
        self.listmodel.removeRows(0, self.listmodel.rowCount())
        while True:
            try:
                message, addr = zb_sock.recvfrom(1024)
                #print(message)
                msg_data = bytes.decode(message)
                tindex = msg_data.rfind('}')
                msg_json = msg_data[:tindex + 1]
                dict_json = json.loads(msg_json)
                self.fileinfo.macaddr = dict_json['macAddress']
                self.fileinfo.ipaddr = dict_json['ipAddress']
                #print(self.fileinfo.macaddr, self.fileinfo.ipaddr)
                if self.fileinfo.ipaddr.find('192.168.42.10') >= 0:
                    pass
                else:
                    row = self.listmodel.rowCount()
                    self.listmodel.insertRow(row)
                    self.listmodel.setData(self.listmodel.index(row), str(self.fileinfo))
                    #print(self.listmodel.itemData(self.listmodel.index(row))[0])
            except:
                self.pushButton_findip.setText("find ip")
                self.pushButton_findip.setEnabled(True)
                break

    def push_findip(self):
            self.t5 = threading.Thread(target=self.startFindIp, args=())
            self.t5.setDaemon(True)
            self.t5.start()

            self.t6 = threading.Thread(target=self.startRecvFindIp, args=())
            self.t6.setDaemon(True)
            self.t6.start()

            self.pushButton_findip.setText("finding")
            self.pushButton_findip.setEnabled(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())

