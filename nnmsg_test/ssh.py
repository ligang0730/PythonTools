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

from pynng import Pair0, Pair1, Pub0, Sub0
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QEventLoop, QTimer, QStringListModel
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from ssh_form import Ui_Form
from socket import *
from icon import *

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

        self.setWindowIcon(QtGui.QIcon(':/logo.ico'))
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)

        #self.pushButton_unconnect.setEnabled(False)
        self.textEdit_send.setStyleSheet("background:#ffffff")
        self.textEdit.setStyleSheet("background:#ffffff")
        self.t1_running = True

    def outputWritten(self, text):
        # self.textEdit.clear()
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

    #def showResult(self):

    def msgRecv(self):
        while self.t1_running:
            if self.radioButton_pair.isChecked():
                if self.radioButton_connect.isChecked():
                    data = self.nn_pairA.recv()
                    print(data)
                elif self.radioButton_bind.isChecked():
                    data = self.nn_pairB.recv()
                    print(data)

            elif self.radioButton_sub.isChecked():
                data = self.nn_sub.recv()
                print(data)

            else:
                pass

    def push_connect(self):
        PORT = int(self.lineEdit_port.text())
        HOST_IP = self.lineEdit_ip.text()
        nn_hostip = 'tcp://' + str(HOST_IP) + ':' + str(PORT)

        if self.radioButton_pair.isChecked():
            if self.radioButton_connect.isChecked():
                self.nn_pairA = Pair0()
                self.nn_pairA.dial(nn_hostip)
            elif self.radioButton_bind.isChecked():
                self.nn_pairB = Pair0()
                self.nn_pairB.listen(nn_hostip)

        elif self.radioButton_pub.isChecked():
            if self.radioButton_connect.isChecked():
                self.nn_pub = Pub0(dial=nn_hostip, send_timeout=5000)
            elif self.radioButton_bind.isChecked():
                self.nn_pub = Pub0(listen=nn_hostip, send_timeout=5000)

        elif self.radioButton_sub.isChecked():
            if self.radioButton_connect.isChecked():
                self.nn_sub = Sub0(dial=nn_hostip)
            elif self.radioButton_bind.isChecked():
                self.nn_sub = Sub0(listen=nn_hostip)
            self.nn_sub.subscribe('')

        self.t1_running = True
        self.t1 = threading.Thread(target=self.msgRecv, args=())
        self.t1.setDaemon(True)
        self.t1.start()

        self.pushButton_connect.setEnabled(False)
        self.pushButton_unconnect.setEnabled(True)

    def push_unconnect(self):
        if self.radioButton_pair.isChecked():
            if self.radioButton_connect.isChecked():
                self.nn_pairA.close()
            elif self.radioButton_bind.isChecked():
                self.nn_pairB.close()

        elif self.radioButton_pub.isChecked():
            self.nn_pub.close()

        elif self.radioButton_sub.isChecked():
            self.nn_sub.close()

        self.pushButton_connect.setEnabled(True)
        self.pushButton_unconnect.setEnabled(False)

    def push_send(self):
        data = self.textEdit_send.toPlainText()
        sendmsg = data.encode('ascii')
        #print(sendmsg)
        if self.radioButton_pair.isChecked():
            if self.radioButton_connect.isChecked():
                self.nn_pairA.send(sendmsg)
            elif self.radioButton_bind.isChecked():
                self.nn_pairB.send(sendmsg)

        elif self.radioButton_pub.isChecked():
            self.nn_pub.send(sendmsg)

        else:
            pass

    def msgSend(self):
        cbt = int(self.lineEdit_sendint.text())
        sendCnt = 0
        while self.t2_running:
            data = self.textEdit_send.toPlainText()
            sendmsg = data.encode('ascii')
            # print(sendmsg)
            if self.radioButton_pair.isChecked():
                if self.radioButton_connect.isChecked():
                    self.nn_pairA.send(sendmsg)
                    sendCnt += 1
                elif self.radioButton_bind.isChecked():
                    self.nn_pairB.send(sendmsg)
                    sendCnt += 1
            elif self.radioButton_pub.isChecked():
                self.nn_pub.send(sendmsg)
                sendCnt += 1
            else:
                pass
            self.label_sendfinish.setText(str(sendCnt))
            time.sleep(cbt)

    def push_xhsend(self):
        if self.pushButton_sendxh.text() == "停止":
            self.t2_running = False
            self.pushButton_sendxh.setText("发送")

        elif self.pushButton_sendxh.text() == "发送":
            self.t2_running = True
            self.t2 = threading.Thread(target=self.msgSend, args=())
            self.t2.setDaemon(True)
            self.t2.start()
            self.pushButton_sendxh.setText("停止")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())

# from pynng import Pair0
# s1 = Pair0()
# s1.listen('tcp://127.0.0.1:54321')
# s2 = Pair0()
# s2.dial('tcp://127.0.0.1:54321')
# s1.send(b'Well hello there')
# print(s2.recv())
# s1.close()
# s2.close()

# import pynng import trio async
# def send_and_recv(sender,receiver,message):
#     awaitsender.asend(message)
#     returnawaitreceiver.arecv()
#     withpynng.Pair0(listen='tcp://127.0.0.1:54321')ass1,
#     pynng.Pair0(dial='tcp://127.0.0.1:54321')
#     ass2:received=trio.run(send_and_recv,s1,s2,b'hello there old pal!')
#     assertreceived==b'hello there old pal!'
#
# from pynng import Pair0 with Pair0(listen='tcp://127.0.0.1:54321')
#     ass1, \
#     Pair0(dial='tcp://127.0.0.1:54321')
#     ass2: s1.send(b'Well hello there')
#     print(s2.recv())