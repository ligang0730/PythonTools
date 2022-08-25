# -*- coding: utf-8 -*-

import sys, os
import optparse
import random
import threading
import json
import subprocess

from pynng import Pair0, Pair1
from PyQt5.QtCore import QEventLoop, QTimer, QStringListModel
from PyQt5 import QtWidgets
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from qfsumo import Ui_Form
from runner import QfSumo_Class
from jxxml import XmlParse

class itemfileinfo:
    def __init__(self, veh_id, veh_type, veh_color, veh_speed, veh_startlaneNum, veh_endlaneNum, veh_startlane,
                 veh_endlane, veh_num):
        self.veh_id = veh_id
        self.veh_type = veh_type
        self.veh_color = veh_color
        self.veh_speed = veh_speed
        self.veh_startlaneNum = veh_startlaneNum
        self.veh_endlaneNum = veh_endlaneNum
        self.veh_startlane = veh_startlane
        self.veh_endlane = veh_endlane
        self.veh_num = veh_num

    def __repr__(self):
        return "%s    %s    %s    %s    %s    %s    %s    %s    %s" % \
               (self.veh_id, self.veh_type, self.veh_color, self.veh_speed,
                self.veh_startlaneNum, self.veh_endlaneNum, self.veh_startlane,
                self.veh_endlane, self.veh_num)


class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)
        self.loadXmlFileList()
        try:
            self.loadLanesInfo()
        except:
            pass
        self.loadCarStateList()

        # self.listView.setStyleSheet("background:#ffffff")
        # self.showlist = []
        # self.fileinfo = itemfileinfo('', '', '', '', '', '', '', '', '')
        # self.listmodel = QStringListModel(self)
        # self.listmodel.setStringList(self.showlist)
        # self.listView.setModel(self.listmodel)
        # self.listmodel.dataChanged.connect(self.lvsave)
        self.catCount = 0

    def lvsave(self):
        self.showlist = self.listmodel.stringList()

    def push_start(self):
        port = int(self.lineEdit_port.text())
        ip = self.lineEdit_ip.text()
        startLane = self.comboBox_startLane.currentText()
        endlane = self.comboBox_endLane.currentText()

        sumo = QfSumo_Class()
        sumo.qfSumo_start(port, ip, startLane, endlane)

    def push_osm2MapConf(self):
        osm_file_name = self.comboBox_osmName.currentText()
        nodeName = self.lineEdit_nodeName.text()
        region = self.lineEdit_nodeRegion.text()
        id = self.lineEdit_nodeId.text()
        parseXml = XmlParse()
        parseXml.osm2MapConf(osm_file_name, nodeName, region, id)

    def push_osm2Net(self):
        osm_file_name = self.comboBox_osmName.currentText()
        net_file_name = os.path.splitext(osm_file_name)[0] + '.net.xml'
        #print(os.path.splitext(osm_file_name)[0])
        retcode = subprocess.call(
            ['netconvert', '--osm-files', osm_file_name, '-o', net_file_name],
            stdout=sys.stdout, stderr=sys.stderr)
        print(">> Simulation closed with status %s" % retcode)
        sys.stdout.flush()
        self.loadXmlFileList()

    def loadXmlFileList(self):
        osm_list = []
        net_list = []
        rou_list = []
        file_list = os.listdir('.')
        for file in file_list:
            file_ext = os.path.splitext(file)  # 分离文件前后缀，front为前缀名，ext为后缀名
            front, ext = file_ext  # 将前后缀分别赋予front和ext
            if ext == '.osm':
                osm_list.append(file)
            if ext == '.xml':
                file_ext2 = os.path.splitext(front)
                front2, ext2 = file_ext2
                if ext2 == '.net':
                    net_list.append(file)
                if ext2 == '.rou':
                    rou_list.append(file)
        self.comboBox_osmName.clear()
        self.comboBox_netName.clear()
        self.comboBox_rouName.clear()
        self.comboBox_osmName.addItems(osm_list)
        self.comboBox_netName.addItems(net_list)
        self.comboBox_rouName.addItems(rou_list)

    def loadLanesInfo(self):
        deallinePos_showList = []
        carType_list = ['passenger', 'bus', 'bicycle', 'pedestrian']
        carColor_list = ['olive', 'pink', 'red', 'blue', 'orange', 'green', 'purple']
        osm_file_name = self.comboBox_osmName.currentText()
        net_file_name = self.comboBox_netName.currentText()
        parseXml = XmlParse()
        lanesInfo_list = parseXml.getLanesInfo(osm_file_name, net_file_name)
        print(lanesInfo_list)
        for laneInfo in lanesInfo_list:
            for lane_id in laneInfo['id_list']:
                for lane_i in range(laneInfo['laneNum']):
                    deallinePos_show = laneInfo['laneName'] + '@' + lane_id + '@' + str(lane_i)
                    deallinePos_showList.append(deallinePos_show)
        self.comboBox_startLane.clear()
        self.comboBox_endLane.clear()
        # self.comboBox_carType.clear()
        # self.comboBox_color.clear()
        self.comboBox_startLane.addItems(deallinePos_showList)
        self.comboBox_endLane.addItems(deallinePos_showList)
        # self.comboBox_carType.addItems(carType_list)
        # self.comboBox_color.addItems(carColor_list)

    def push_refreshFileList(self):
        self.loadXmlFileList()
        self.loadLanesInfo()

    def loadCarStateList(self):
        carState_list = ['stop', 'resume', 'change lane', 'slow down']
        self.comboBox_caozuo.addItems(carState_list)

    def push_stop(self):
        sumo = QfSumo_Class()
        sumo.qfSumo_stop()

    def push_carryout(self):
        sumo = QfSumo_Class()
        curCarStateItem = self.comboBox_caozuo.currentText()
        catvehId = self.lineEdit_carId.text()
        sumo.vehState_carryout(catvehId, curCarStateItem)

        print('666666666666666666')
    # def push_addCar(self):
    #     self.catCount += 1
    #     self.lineEdit_carId.setText(str(self.catCount))
    #     self.fileinfo.veh_id = self.catCount
    #     self.fileinfo.veh_type = str(self.comboBox_carType.currentText())
    #     self.fileinfo.veh_color = str(self.comboBox_color.currentText())
    #     self.fileinfo.veh_speed = str(self.lineEdit_speed.text())
    #     self.fileinfo.veh_startlaneNum = self.comboBox_startLane.currentText().split("@")[1]
    #     self.fileinfo.veh_endlaneNum = self.comboBox_startLane.currentText().split("@")[2]
    #     self.fileinfo.veh_startlane = self.comboBox_endLane.currentText().split("@")[1]
    #     self.fileinfo.veh_endlane = self.comboBox_endLane.currentText().split("@")[2]
    #     self.fileinfo.veh_num = str(self.lineEdit_carNum.text())
    #
    #     row = self.listmodel.rowCount()
    #     self.listmodel.insertRow(row)
    #     self.listmodel.setData(self.listmodel.index(row), str(self.fileinfo))
    #
    # def push_saveRou(self):
    #     carInfoList = []
    #     carNum = self.listmodel.rowCount()
    #     for i in range(carNum):
    #         veh_dict = {'id': self.showlist[i].split('    ')[0], 'type': self.showlist[i].split('    ')[1],
    #                     'color': self.showlist[i].split('    ')[2], 'departSpeed': self.showlist[i].split('    ')[3],
    #                     'departLane': self.showlist[i].split('    ')[4],
    #                     'arrivalLane': self.showlist[i].split('    ')[5],
    #                     'from': self.showlist[i].split('    ')[6], 'to': self.showlist[i].split('    ')[7],
    #                     'number': self.showlist[i].split('    ')[8]}
    #         carInfoList.append(veh_dict)
    #     parseXml = XmlParse()
    #     parseXml.creatRouXmlFile(carInfoList)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())

