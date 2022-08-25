# -*- coding: utf-8 -*-

import os
import sys
import threading
import time
import paramiko
import hashlib
import shutil
import json
import difflib
import select
import struct
import base64

from pynng import Pair0, Pair1
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QEventLoop, QTimer, QStringListModel
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from main_form import Ui_Form
from socket import *
from icon import *
import ObuApp_pb2 as ObuApp__pb2
import websock as websockCli

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
        self.textEdit.setStyleSheet("background:#ffffff")
        self.msgCnt = 0

    def outputWritten(self, text):
        # self.textEdit.clear()
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

    def recvWsMsg(self, message):
        #print("call_back message:", message)
        pass

    def push_connect(self):
        ip = self.lineEdit_ip.text()
        port = self.lineEdit_port.text()
        # "ws://172.16.11.25:5516"
        wsip = "ws://" + ip + ":" + port
        print(wsip)
        #self.ws_client = websockCli.WSClient(wsip, lambda message: print("call_back message:", message))
        self.ws_client = websockCli.WSClient(wsip, self.recvWsMsg)
        self.ws_client.run()

    def push_unconnect(self):
        #self.ws_client.send_message("time:" + str(time.time()))
        pass

    def is_number(self, str):
        try:
            return int(str)
        except:
            return 0

    def push_send(self):
        dict_msg = {"data": ""}

        syObuApp = ObuApp__pb2.ObuApp()
        syObuApp.info.time = int(time.time())
        syObuApp.info.id = "APTX-4869"

        syVehSetting = syObuApp.setting
        self.msgCnt += 1
        syVehSetting.msgCnt = self.msgCnt

        syVehSize = syVehSetting.size
        syVehSize.width = self.is_number(self.lineEdit_width.text())
        syVehSize.length = self.is_number(self.lineEdit_length.text())
        syVehSize.height = self.is_number(self.lineEdit_height.text())

        syVehicleClassification = syObuApp.setting.vehClass
        syVehicleClassification.classification = self.is_number(self.lineEdit_classification.text())
        syVehicleClassification.fuelType = self.is_number(self.lineEdit_fuelType.text())

        syBrakeSystemStatus = syObuApp.setting.brakeStatus
        syBrakeSystemStatus.brakePadel = self.is_number(self.lineEdit_bbp.text())
        syBrakeSystemStatus.wheelBrakes = self.is_number(self.lineEdit_wb.text())
        syBrakeSystemStatus.traction = self.is_number(self.lineEdit_tcr.text())
        syBrakeSystemStatus.abs = self.is_number(self.lineEdit_abs.text())
        syBrakeSystemStatus.scs = self.is_number(self.lineEdit_scs.text())
        syBrakeSystemStatus.brakeBoost = self.is_number(self.lineEdit_bbb.text())
        syBrakeSystemStatus.auxBrakes = self.is_number(self.lineEdit_aab.text())

        light = 0
        if self.checkBox_lowL.isChecked():
            light = 1
        if self.checkBox_highL.isChecked():
            light |= (1 << 1)
        if self.checkBox_leftL.isChecked():
            light |= (1 << 2)
        if self.checkBox_rightL.isChecked():
            light |= (1 << 3)
        if self.checkBox_hazardL.isChecked():
            light |= (1 << 4)
        if self.checkBox_autoL.isChecked():
            light |= (1 << 5)
        if self.checkBox_dayL.isChecked():
            light |= (1 << 6)
        if self.checkBox_fogL.isChecked():
            light |= (1 << 7)
        if self.checkBox_parkL.isChecked():
            light |= (1 << 8)
        syVehSetting.lights = light

        #print(syObuApp)
        bMsg= syObuApp.SerializeToString()
        #print(bMsg)
        base64_msg = base64.b64encode(bMsg)
        #print(str(base64_msg, 'utf-8'))
        dict_msg['data'] = str(base64_msg, 'utf-8')
        sendmsg = json.dumps(dict_msg)
        #print(sendmsg)
        self.ws_client.send_message(sendmsg)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
