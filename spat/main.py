# -*- coding: utf-8 -*-

import os
import sys
import time
import serial
import copy
import threading
import binascii
import serial.tools.list_ports

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from main_form import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from socket import *


from icon import *
# class EmittingStr(QtCore.QObject):
#     textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号
#
#     def write(self, text):
#         self.textWritten.emit(str(text))
#         loop = QEventLoop()
#         QTimer.singleShot(1000, loop.quit)
#         loop.exec_()

class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/logo.ico'))
        #sys.stdout = EmittingStr(textWritten=self.outputWritten)
        #sys.stderr = EmittingStr(textWritten=self.outputWritten)
        #self.setWindowIcon(QtGui.QIcon(':/logo.ico'))
        #self.textEdit.setStyleSheet("background:#ffffff")
        self.pushButton_connect.setEnabled(True)
        self.pushButton_break.setEnabled(False)
        self.pushButton_start.setEnabled(True)
        self.pushButton_stop.setEnabled(False)
        self.t1_running = True
        comList = []
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            self.show_message("The Serial port can't find!")
        else:
            for i in list(port_list):
                comList.append(i[0])
        self.comboBox_comid.addItems(comList)

        brtelist = ['4800', '9600', '19200', '38400', '115200']
        self.comboBox_branrate.addItems(brtelist)
        self.comboBox_branrate.setCurrentText('115200')

        self.data = ['#', 'F', '2', ',',
                     '0', '0', '0', ',',
                     '0', '0', '0', ',',
                     '0', '0', '0', ',',
                     '0', '0', '0', ',',
                     '1', 'R', ',',
                     '0', '0', '0', ',',
                     '2', 'G', ',',
                     '0', '0', '0', ';']

    def int2chr(self, icnt):
        strlist = ['0', '0', '0']
        scnt = str(icnt)
        ilen = len(scnt)
        for i in range(ilen):
            strlist[2-i] = scnt[-1-i]
        return strlist

    def fillData(self, phase1Time, phase2Time, allRedTime, yellowTime,
                 phase1Color, phase1Downcnt, phase2Color, phase2Downcnt):
        data = copy.deepcopy(self.data)
        data[4:7] = self.int2chr(phase1Time)
        data[8:11] = self.int2chr(phase2Time)
        data[12:15] = self.int2chr(allRedTime)
        data[16:19] = self.int2chr(yellowTime)
        data[21] = phase1Color
        data[23:26] = self.int2chr(phase1Downcnt)
        data[28] = phase2Color
        data[30:33] = self.int2chr(phase2Downcnt)
        return data

    # def outputWritten(self, text):
    #     # self.textEdit.clear()
    #     cursor = self.textEdit.textCursor()
    #     cursor.movePosition(QtGui.QTextCursor.End)
    #     cursor.insertText(text)
    #     self.textEdit.setTextCursor(cursor)
    #     self.textEdit.ensureCursorVisible()

    def show_message(self, warnMsg):
        msg_box = QMessageBox(QMessageBox.Information, 'warning', warnMsg)
        msg_box.exec_()

    def push_connect(self):
        if self.comboBox_connectMode.currentText() == "COM":
            serial_port = str(self.comboBox_comid.currentText())
            serial_brte = int(self.comboBox_branrate.currentText())
            try:
                self.fd_com = serial.Serial(serial_port, serial_brte, timeout=0.01)
                if self.fd_com.isOpen():
                    self.pushButton_connect.setEnabled(False)
                    self.pushButton_break.setEnabled(True)
                    self.comboBox_connectMode.setEnabled(False)
                else:
                    self.show_message("端口" + serial_port + "打开失败")
            except:
                self.show_message('端口' + serial_port + '无效或被占用')

        elif self.comboBox_connectMode.currentText() == "UDP":
            try:
                udpip = self.lineEdit_udpip.text()
                udpport = self.getNumValue(self.lineEdit_udpport)
                self.address = (udpip, udpport)
                self.udpSock = socket(AF_INET, SOCK_DGRAM)
                self.udpSock.settimeout(1)
                self.pushButton_connect.setEnabled(False)
                self.pushButton_break.setEnabled(True)
                self.comboBox_connectMode.setEnabled(False)
            except:
                self.show_message("UDP" + udpip + "连接失败")

    def push_break(self):
        if self.comboBox_connectMode.currentText() == "COM":
            self.fd_com.close()
        elif self.comboBox_connectMode.currentText() == "UDP":
            self.udpSock.close()
        self.pushButton_connect.setEnabled(True)
        self.pushButton_break.setEnabled(False)
        self.comboBox_connectMode.setEnabled(True)

    def getNumValue(self, lineEditId):
        try:
            ret = int(lineEditId.text())
        except:
            ret = 0
        return ret

    def push_start(self):
        data = copy.deepcopy(self.data)
        phase1Time = self.getNumValue(self.lineEdit_phase1Time)
        phase2Time = self.getNumValue(self.lineEdit_phase2Time)
        allRedTime = self.getNumValue(self.lineEdit_allRedTime)
        yellowTime = self.getNumValue(self.lineEdit_yellowTime)
        phase1Gtime = phase1Time
        phase1Rtime = phase2Time + yellowTime + allRedTime + allRedTime
        phase2Gtime = phase2Time
        phase2Rtime = phase1Time + yellowTime + allRedTime + allRedTime

        self.t1_running = True
        self.t1 = threading.Thread(target=self.msgSend, args=(phase1Time, phase2Time,
                                                              allRedTime, yellowTime,
                                                              phase1Gtime, phase1Rtime,
                                                              phase2Gtime, phase2Rtime))
        self.t1.setDaemon(True)
        self.t1.start()
        self.pushButton_start.setEnabled(False)
        self.pushButton_stop.setEnabled(True)

    def push_stop(self):
        self.t1_running = False
        self.pushButton_start.setEnabled(True)
        self.pushButton_stop.setEnabled(False)
        self.setLabelColor(self.label_phase1Downcnt, '')
        self.setLabelColor(self.label_phase2Downcnt, '')
        self.label_phase1Downcnt.setText('0')
        self.label_phase2Downcnt.setText('0')

    def getLow8(self, num):
        if num > 255:
            return (num - 256)
        else:
            return num

    def setLabelColor(self, label, color):
        if color == "G":
            label.setStyleSheet("color:#00ff00")
        elif color == "R":
            label.setStyleSheet("color:#ff0000")
        elif color == "Y":
            label.setStyleSheet("color:#ffff00")
        else:
            label.setStyleSheet("color:#000000")

    def msgSend(self, phase1Time, phase2Time, allRedTime, yellowTime,
                phase1Gtime, phase1Rtime, phase2Gtime, phase2Rtime):
        roundColor1 = ['G', 'Y', 'R']
        roundColor2 = ['G', 'Y', 'R']
        roundTime1 = [phase1Gtime, yellowTime, phase1Rtime]
        roundTime2 = [phase2Gtime, yellowTime, phase2Rtime]
        step1 = 0
        step2 = 2
        curPhase1Color = roundColor1[step1]
        curPhase2Color = roundColor2[step2]
        curPhase1Time = roundTime1[step1]
        curPhase2Time = roundTime2[step2] - allRedTime
        while self.t1_running:
            data = self.fillData(phase1Time, phase2Time, allRedTime, yellowTime,
                                 curPhase1Color, self.getLow8(curPhase1Time),
                                 curPhase2Color, self.getLow8(curPhase2Time))

            if self.comboBox_connectMode.currentText() == "COM":
                msgList = []
                for d in data:
                    msgList.append(ord(d))
                self.fd_com.write(msgList)
            elif self.comboBox_connectMode.currentText() == "UDP":
                sendMag = ''.join(data)
                self.udpSock.sendto(sendMag.encode('ascii'), self.address)

            self.setLabelColor(self.label_phase1Downcnt, curPhase1Color)
            self.label_phase1Downcnt.setText(str(curPhase1Time))
            self.setLabelColor(self.label_phase2Downcnt, curPhase2Color)
            self.label_phase2Downcnt.setText(str(curPhase2Time))

            time.sleep(1)

            curPhase1Time -= 1
            curPhase2Time -= 1
            if curPhase1Time == 0:
                step1 += 1
                step1 = 0 if (step1 == 3) else step1
                curPhase1Color = roundColor1[step1]
                curPhase1Time = roundTime1[step1]
            if curPhase2Time == 0:
                step2 += 1
                step2 = 0 if (step2 == 3) else step2
                curPhase2Color = roundColor2[step2]
                curPhase2Time = roundTime2[step2]


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
