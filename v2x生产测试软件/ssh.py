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

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QEventLoop, QTimer, QStringListModel
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from ssh_form import Ui_Form
from socket import *
from icon import *
from pynng import Pair0, Pair1
from multiprocessing import Process, Pipe

class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/logo.ico'))
        self.rwlock = threading.Lock()
        self.rwlock_ret = threading.Lock()
        self.pushButton_stop.setEnabled(False)
        self.parent_conn_Msg, self.child_conn_Msg = Pipe()

    def setCocColor(self, value, label):
        time.sleep(0.2)
        if value == "Y":
            label.setStyleSheet("color:#00aa00")
            return 1
        else:
            label.setStyleSheet("color:#ff0000")
            return 0

    def showResult(self):
        while self.t4_running:
            dict_json = {}
            tmp = 0
            ret = 0
            try:
                while self.parent_conn_Msg.poll():
                    dict_json = self.parent_conn_Msg.recv()
                    time.sleep(0.01)
                if len(dict_json) == 0:
                    time.sleep(1)
                else:
                    tmp = 1
                    ret = 1
            except:
                pass

            try:
                ret &= self.setCocColor(dict_json['GPS-MODULE']['init'], self.lab_gps_init)
                ret &= self.setCocColor(dict_json['GPS-MODULE']['recvFlg'], self.lab_gps_recvFlg)
                ret &= self.setCocColor(dict_json['GPS-MODULE']['avFlg'], self.lab_gps_avFlg)
                ret &= self.setCocColor(dict_json['GPS-MODULE']['setTimeFlg'], self.lab_gps_setTimeFlg)
                self.lab_gps_satellites.setText("satellites:"+ dict_json['GPS-MODULE']['satellites'])
            except:
                ret &= 1

            try:
                ret &= self.setCocColor(dict_json['V2X-MODULE-SEND']['initSend'], self.lab_v2xsend_init)
                ret &= self.setCocColor(dict_json['V2X-MODULE-SEND']['sendFlg'], self.lab_v2xsend_flg)
                self.lab_v2xsend_sendLen.setText("sendLen:"+ dict_json['V2X-MODULE-SEND']['sendLen'])
                self.lab_v2xsend_sendCnts.setText("sendCnts:" + dict_json['V2X-MODULE-SEND']['sendCnts'])
            except:
                ret &= 1

            try:
                ret &= self.setCocColor(dict_json['V2X-MODULE-RECV']['initRecv'], self.lab_v2xrecv_init)
                ret &= self.setCocColor(dict_json['V2X-MODULE-RECV']['recvFlg'], self.lab_v2xrecv_flg)        #print(self.dict_json['V2X-MODULE-RECV']['recvCnts'])
                self.lab_v2xrecv_recvLen.setText("recvLen:" + dict_json['V2X-MODULE-RECV']['recvLen'])
                self.lab_v2xrecv_recvCnts.setText("recvCnts:" + dict_json['V2X-MODULE-RECV']['recvCnts'])
                self.lab_v2xrecv_recvCnts.show()
            except:
                ret &= 1

            try:
                tmp = 1
                tmp &= self.setCocColor(dict_json['CAN0']['init'], self.lab_can0_init)
                tmp &= self.setCocColor(dict_json['CAN0']['recvFlg'], self.lab_can0_recvflg)
                tmp &= self.setCocColor(dict_json['CAN0']['sendFlg'], self.lab_can0_sendflg)
                self.lab_can0_recvCnts.setText("recvCnts:" + dict_json['CAN0']['recvCnts'])
                self.lab_can0_sendCnts.setText("sendCnts:" + dict_json['CAN0']['sendCnts'])

                tmp &= self.setCocColor(dict_json['CAN1']['init'], self.lab_can1_init)
                tmp &= self.setCocColor(dict_json['CAN1']['recvFlg'], self.lab_can1_recvflg)
                tmp &= self.setCocColor(dict_json['CAN1']['sendFlg'], self.lab_can1_sendflg)
                self.lab_can1_recvCnts.setText("recvCnts:" + dict_json['CAN1']['recvCnts'])
                self.lab_can1_sendCnts.setText("sendCnts:" + dict_json['CAN1']['sendCnts'])
                ret &= tmp
            except:
                ret &= 1

            try:
                tmp = 1
                tmp &= self.setCocColor(dict_json['RS485']['init'], self.lab_rs485_init)
                tmp &= self.setCocColor(dict_json['RS485']['recvFlg'], self.lab_rs485_recvflg)
                tmp &= self.setCocColor(dict_json['RS485']['sendFlg'], self.lab_rs485_sendflg)
                self.lab_rs485_recvCnts.setText("recvCnts:" + dict_json['RS485']['recvCnts'])
                self.lab_rs485_sendCnts.setText("sendCnts:" + dict_json['RS485']['sendCnts'])
                ret &= tmp
            except:
                ret &= 1

            try:
                tmp = 1
                tmp &= self.setCocColor(dict_json['SM']['init'], self.lab_SM_init)
                tmp &= self.setCocColor(dict_json['SM']['result'], self.lab_SM_result)
                ret &= tmp
            except:
                ret &= 1

            try:
                ret &= self.setCocColor(dict_json['E2']['write'], self.lab_e2_write)
                ret &= self.setCocColor(dict_json['E2']['read'], self.lab_e2_read)
            except:
                ret &= 1

            try:
                tmp = 1
                tmp &= self.setCocColor(dict_json['Sensor']['magnet'], self.lab_Sensor_magnet)
                tmp &= self.setCocColor(dict_json['Sensor']['acc'], self.lab_Sensor_acc)
                tmp &= self.setCocColor(dict_json['Sensor']['gyro'], self.lab_Sensor_gyro)
                ret &= tmp
            except:
                ret &= 1

            try:
                tmp = 1
                tmp &= self.setCocColor(dict_json['5G']['netdev'], self.lab_5g_netdev)
                tmp &= self.setCocColor(dict_json['5G']['sim'], self.lab_5g_sim)
                tmp &= self.setCocColor(dict_json['5G']['get_ip'], self.lab_5g_get_ip)
                tmp &= self.setCocColor(dict_json['5G']['ping'], self.lab_5g_ping)
                ret &= tmp
            except:
                ret &= 1

            try:
                tmp = 1
                tmp &= self.setCocColor(dict_json['4G']['ping'], self.lab_4G_ping)
                ret &= tmp
            except:
                ret &= 1

            try:
                tmp = 1
                tmp &= self.setCocColor(dict_json['WIFI']['netdev'], self.lab_WIFI_netdev)
                ret &= tmp
            except:
                ret &= 1

            try:
                tmp = 1
                tmp &= self.setCocColor(dict_json['TF']['insert'], self.lab_TF_insert)
                self.lab_TF_cap.setText("cap:" + dict_json['TF']['cap'])
                ret &= tmp
            except:
                ret &= 1

            try:
                tmp = 1
                tmp &= self.setCocColor(dict_json['USB']['insert'], self.lab_usb_insert)
                self.lab_usb_info.setText("info:" + dict_json['USB']['info'])
                ret &= tmp
            except:
                ret &= 1

            try:
                tmp = 1
                tmp &= self.setCocColor(dict_json['PSAM']['drv'], self.lab_psam_drv)
                tmp &= self.setCocColor(dict_json['PSAM']['test'], self.lab_psam_test)
                ret &= tmp
            except:
                ret &= 1

            self.rwlock_ret.acquire()
            self.getresult = ret
            self.rwlock_ret.release()

    def startVxtest(self):
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
                print("登陆成功")
                break
            except:
                TryConnNum += 1
                # print("登陆中..." + str(TryConnNum))
                if TryConnNum > 9:
                    print("登陆失败")
                    exit(-1)

        cmd_path = "export LD_LIBRARY_PATH=/lib:/usr/lib:/usr/exlib:/opt/platform/lib:/opt/v2x/lib"
        cmd_vxtest = "cd /opt/platform/bin/ && ./vxtest.bin &"
        stdin, stdout, stderr = self.sshSock.exec_command(cmd_path + " && " + cmd_vxtest)
        # while True:
        #     time.sleep(1)

    def msgRecv(self):
        time.sleep(5)
        PORT = 6610
        message = "irqmsg"
        self.nn_pairA = Pair0()
        nn_hostip = 'tcp://' + str(self.HOST_IP) + ':' + str(PORT)
        self.nn_pairA.dial(nn_hostip)
        print("nn_pairA connect")
        while self.t2_running:
            data = self.nn_pairA.recv()
            #print(data)
            msg_data = bytes.decode(data)
            tindex = msg_data.rfind('}')
            msg_json = msg_data[:tindex + 1]
            try:
                self.rwlock.acquire()
                self.connectState = "open"
                self.rwlock.release()
                dict_json = json.loads(msg_json)
                #print(self.dict_json)
                self.child_conn_Msg.send(dict_json)
                time.sleep(1)
                #self.showResult()
            except:
                print(msg_json)

    def lcdDisplay(self):
        mret = 0
        time_lcd = 60
        #self.label_ddtime.setText(str(time_lcd))
        self.lcdNumber.display(str(time_lcd))
        while self.t3_running:
            self.rwlock.acquire()
            state = self.connectState
            self.rwlock.release()

            if state == "open":
                time_lcd -= 1
                if time_lcd >= 0:
                    print(time_lcd)
                if time_lcd < 0:
                    time_lcd = 0
                    self.label_Ret.setStyleSheet("color:#ff0000")
                    self.label_Ret.setText("测试失败")
                    print("测试失败")
                    self.stopt1t2()
                    return

                self.rwlock_ret.acquire()
                mret = self.getresult
                self.rwlock_ret.release()
                #print(mret)
                if mret == 1 and time_lcd < 55:
                    self.label_Ret.setStyleSheet("color:#00aa00")
                    self.label_Ret.setText("测试成功")
                    print("测试成功")
                    self.stopt1t2()
                    return
                #self.label_ddtime.setText(str(time_lcd))
                self.lcdNumber.display(str(time_lcd))

            time.sleep(1)

    def push_udpconnect(self):
        self.rwlock_ret.acquire()
        self.getresult = 0
        self.rwlock_ret.release()

        self.rwlock.acquire()
        self.connectState = "stop"
        self.rwlock.release()
        self.HOST_IP = self.lineEdit.text()

        self.t1_running = True
        self.t1 = threading.Thread(target=self.startVxtest, args=())
        self.t1.setDaemon(True)
        self.t1.start()

        self.t2_running = True
        self.t2 = threading.Thread(target=self.msgRecv, args=())
        self.t2.setDaemon(True)
        self.t2.start()

        self.t3_running = True
        self.t3 = threading.Thread(target=self.lcdDisplay, args=())
        self.t3.setDaemon(True)
        self.t3.start()

        self.t4_running = True
        self.t4 = threading.Thread(target=self.showResult, args=())
        self.t4.setDaemon(True)
        self.t4.start()

        self.pushButton_connect.setEnabled(False)
        self.pushButton_stop.setEnabled(True)

        self.label_Ret.setStyleSheet("color:#000000")
        self.label_Ret.setText("测试中")

    def killbinpid(self, biname):
        try:
            cmd_psvxtest = "ps | grep " + biname + " | grep -v grep | awk '{print $1}'"
            cmd_killvxtest = "ps | grep " + biname + " | grep -v grep | awk '{print $1}' | xargs kill -9"
            while True:
                stdin, stdout, stderr = self.sshSock.exec_command(cmd_psvxtest)
                if len(stdout.read()) == 0:
                    break
                else:
                    stdin, stdout, stderr = self.sshSock.exec_command(cmd_killvxtest)
        except:
            pass

    def stopt1t2(self):
        self.t1_running = False
        self.t2_running = False
        self.t3_running = False
        self.t4_running = False
        self.rwlock.acquire()
        self.connectState = "stop"
        self.rwlock.release()
        time.sleep(0.5)

    def push_udpclose(self):
        self.killbinpid('vxtest.bin')
        self.killbinpid('gpsd')
        self.stopt1t2()
        self.pushButton_stop.setEnabled(False)
        self.pushButton_connect.setEnabled(True)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())

