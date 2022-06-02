# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import io, libconf
import qtree as Qtree
import folium
import copy
import csv
from folium.plugins import HeatMap, MiniMap, MarkerCluster
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from ssh_form import Ui_Form
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from icon import *
from PyQt5.Qt import (QMutex, QThread)
from pathlib2 import Path

# 在地图上绘制无边框圆形，填充颜色
def draw_CircleMarker(loc, radius, map):
    folium.CircleMarker(
        location=loc,
        radius=radius,
        color="cornflowerblue",
        stroke=False,
        fill=True,
        fill_opacity=0.6,
        opacity=1,
        popup="{} 像素".format(radius),
        tooltip=str(loc),
    ).add_to(map)

# 在地图上绘制一个小Info标记物
def draw_icon(map, loc, col):
    mk = folium.features.Marker(loc)
    pp = folium.Popup(str(loc))
    ic = folium.features.Icon(color=col)
    mk.add_child(ic)
    mk.add_child(pp)
    map.add_child(mk)

# 在地图上绘制一个圆圈
def draw_Circle(map, loc, radius):
    folium.CircleMarker(
        location=loc,
        radius=radius,
        color="red",
        weight=3,
        fill=False,
        fill_opacity=0.6,
        opacity=1,
    ).add_to(map)

# 绘制可缩放的标记物数字指示
def draw_MarkerCluster(map, loc, tip1, tip2):
    marker_cluster = MarkerCluster().add_to(map)
    folium.Marker(
        location=loc,
        popup=tip1,
        icon=None,
    ).add_to(marker_cluster)
    folium.Marker(
        location=loc,
        popup=tip2,
        icon=None,
    ).add_to(marker_cluster)

# 画线
def draw_line(map, loc1, loc2, wei, col, opa, tip):
    kw = {"opacity": opa, "weight": wei}
    folium.PolyLine(
        smooth_factor=10,
        locations=[loc1, loc2],
        color=col,
        tooltip=tip,
        **kw,
    ).add_to(map)

def draw_lines(map, loclist, wei, col, opa, tip):
    for i in range(len(loclist)-1):
        draw_line(map, loclist[i], loclist[i+1], wei, col, opa, tip)

class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/logo.ico'))

        self.treeView_read.setStyleSheet("background:#ffffff")
        self.model_read = Qtree.QJsonModel()

        # 新建一个QWebEngineView()对象
        self.qwebengine = QWebEngineView(self.frame)# 设置网页在窗口中显示的位置和大小
        self.qwebengine.setGeometry(QtCore.QRect(10, 10, 731, 461))# 在QWebEngineView中加载网址
        self.gridLayout_14.addWidget(self.qwebengine, 0, 0, 1, 1)

        self.loadMapFile()

        self.dictRsi = {"RSI": {"id": "", "moy": 0, "refPos": [0, 0, 0], "rtes": [], "rtss": []}}
        self.dictPoint = {"offset": [0, 0]}
        self.dictRtes = {"description": {"present": 0, "text": ""}, "eventConfidence": 10,
                         "eventPos": {"present": 7, "offset": [0, 0]}, "eventRadius": 0, "eventSource": 4,
                         "eventType": 0, "priority": 0, "rteId": 0,
                         "timeDetails": {"startTime": 100, "endTime": 200, "endTimeConfidence": 2},
                         "referencePaths": [], "referenceLinks": []}
        self.dictReferencePaths = {"pathRadius": 100, "present": 7, "points": []}
        self.dictReferenceLinks = {"upstreamNodeId": {"region": 10, "id": 1},
                                   "downstreamNodeId": {"region": 10, "id": 2},
                                   "referenceLanes": 0}
        self.dictRtss = {"description": {"present": 0, "text": ""},
                         "signPos": {"present": 7, "offset": [0, 0]},
                         "signType": 0, "priority": 0, "rtsId": 0,
                         "timeDetails": {"startTime": 100, "endTime": 200, "endTimeConfidence": 2},
                         "referencePaths": [], "referenceLinks": []}

        self.rtesTypeNumList, self.rtssTypeNumList = self.getTypeFromCsv()

    def getTypeFromCsv(self):
        rtesTypeNumList = []
        rtssTypeNumList = []
        rtesTypeList = []
        rtssTypeList = []
        with open("rtes.csv", "r", encoding="utf-8") as fecsv:
            reader = csv.reader(fecsv)
            for row in reader:
                rtesTypeList.append(row[0])
                rtesTypeNumList.append(row[1])
            self.comboBox_rtesType.addItems(rtesTypeList)
        with open("rtss.csv", "r", encoding="utf-8") as fscsv:
            reader = csv.reader(fscsv)
            for row in reader:
                rtssTypeList.append(row[0])
                rtssTypeNumList.append(row[1])
            self.comboBox_rtssType.addItems(rtssTypeList)
        return rtesTypeNumList, rtssTypeNumList

    def getNumValue(self, lineEditId):
        try:
            ret = int(lineEditId.text())
        except:
            ret = 0
        return ret

    def getFloatValue(self, lineEditId):
        try:
            fret = float(lineEditId.text()) * 10000000
        except:
            fret = 0.0

        iret = int(fret)
        return iret

    def getStrValue(self, lineEditId):
        try:
            ret = str(lineEditId.text())
        except:
            ret = ""
        return ret

    def push_modRsi(self):
        #self.dictRsi = copy.deepcopy(self.dictRsi)
        self.dictRsi['RSI']['id'] = self.getStrValue(self.lineEdit_rsiId)
        self.dictRsi['RSI']['moy'] = self.getNumValue(self.lineEdit_moy)
        self.dictRsi['RSI']['refPos'][0] = self.getFloatValue(self.lineEdit_refLat)
        self.dictRsi['RSI']['refPos'][1] = self.getFloatValue(self.lineEdit_refLon)
        self.dictRsi['RSI']['refPos'][2] = self.getFloatValue(self.lineEdit_refEle)

    def push_loadRsi(self):
        self.lineEdit_rsiId.setText(str(self.dictRsi['RSI']['id']))
        self.lineEdit_moy.setText(str(self.dictRsi['RSI']['moy']))
        self.lineEdit_refLat.setText(str(self.dictRsi['RSI']['refPos'][0] / 10000000))
        self.lineEdit_refLon.setText(str(self.dictRsi['RSI']['refPos'][1] / 10000000))
        self.lineEdit_refEle.setText(str(self.dictRsi['RSI']['refPos'][2] / 10000000))

    def push_addRtes(self):
        self.comboBox_rtesPathPos.clear()
        self.comboBox_rtesPaths.clear()
        td_rtes = copy.deepcopy(self.dictRtes)
        td_rtes['description']['present'] = self.comboBox_rtesDesc.currentIndex()
        td_rtes['description']['text'] = self.getStrValue(self.lineEdit_rtesDesc)
        td_rtes['rteId'] = self.getNumValue(self.lineEdit_rtesId)
        td_rtes['eventPos']['offset'][0] = self.getFloatValue(self.lineEdit_rtesLat)
        td_rtes['eventPos']['offset'][1] = self.getFloatValue(self.lineEdit_rtesLon)
        td_rtes['eventRadius'] = self.getNumValue(self.lineEdit_rtesRadius)
        #td_rtes['eventType'] = self.getNumValue(self.lineEdit_rtesType)
        td_rtes['eventType'] = int(self.rtesTypeNumList[self.comboBox_rtesType.currentIndex()])
        td_rtes['priority'] = self.getNumValue(self.lineEdit_rtesPriority)

        cur_rtes = self.dictRsi['RSI']['rtes']
        cur_rtes.append(td_rtes)
        self.comboBox_rtes.addItem(str(td_rtes['rteId']))
        self.comboBox_rtes.setCurrentIndex(self.comboBox_rtes.currentIndex()+1)

    def push_delRtes(self):
        if len(self.dictRsi['RSI']['rtes']) > 0:
            self.dictRsi['RSI']['rtes'].pop(self.comboBox_rtes.currentIndex())
            self.comboBox_rtes.removeItem(self.comboBox_rtes.currentIndex())

    def push_modRtes(self):
        cur_rtes = self.dictRsi['RSI']['rtes'][self.comboBox_rtes.currentIndex()]
        cur_rtes['description']['present'] = self.comboBox_rtesDesc.currentIndex()
        cur_rtes['description']['text'] = self.getStrValue(self.lineEdit_rtesDesc)
        cur_rtes['rteId'] = self.getNumValue(self.lineEdit_rtesId)
        cur_rtes['eventPos']['offset'][0] = self.getFloatValue(self.lineEdit_rtesLat)
        cur_rtes['eventPos']['offset'][1] = self.getFloatValue(self.lineEdit_rtesLon)
        cur_rtes['eventRadius'] = self.getNumValue(self.lineEdit_rtesRadius)
        #cur_rtes['eventType'] = self.getNumValue(self.lineEdit_rtesType)
        cur_rtes['eventType'] = int(self.rtesTypeNumList[self.comboBox_rtesType.currentIndex()])
        cur_rtes['priority'] = self.getNumValue(self.lineEdit_rtesPriority)
        self.comboBox_rtes.setItemText(self.comboBox_rtes.currentIndex(), str(cur_rtes['rteId']))

    def push_loadRtes(self):
        if len(self.dictRsi['RSI']['rtes']) > 0:
            cur_rtes = self.dictRsi['RSI']['rtes'][self.comboBox_rtes.currentIndex()]
            self.lineEdit_rtesDesc.setText(str(cur_rtes['description']['text']))
            self.lineEdit_rtesId.setText(str(cur_rtes['rteId']))
            self.lineEdit_rtesLat.setText(str(cur_rtes['eventPos']['offset'][0] / 10000000))
            self.lineEdit_rtesLon.setText(str(cur_rtes['eventPos']['offset'][1] / 10000000))
            self.lineEdit_rtesRadius.setText(str(cur_rtes['eventRadius']))
            #self.lineEdit_rtesType.setText(str(cur_rtes['eventType']))
            self.comboBox_rtesType.setCurrentIndex(self.rtesTypeNumList.index(str(cur_rtes['eventType'])))
            self.lineEdit_rtesPriority.setText(str(cur_rtes['priority']))

            if len(cur_rtes['referencePaths']) > 0:
                self.comboBox_rtesPaths.clear()
                for i in range(len(cur_rtes['referencePaths'])):
                    self.comboBox_rtesPaths.addItem(str(i))

    def push_addRtesPaths(self):
        td_paths = copy.deepcopy(self.dictReferencePaths)
        td_paths['pathRadius'] = self.getNumValue(self.lineEdit_rtesPathRadius)
        cur_paths = self.dictRsi['RSI']['rtes'][self.comboBox_rtes.currentIndex()]['referencePaths']
        cur_paths.append(td_paths)
        self.comboBox_rtesPaths.addItem(str(self.comboBox_rtesPaths.currentIndex() + 1))
        self.comboBox_rtesPaths.setCurrentIndex(self.comboBox_rtesPaths.currentIndex() + 1)
        self.comboBox_rtesPathPos.clear()

    def push_delRtesPaths(self):
        cur_rtesPath = self.dictRsi['RSI']['rtes'][self.comboBox_rtes.currentIndex()]['referencePaths']
        if len(cur_rtesPath) > 0:
            cur_rtesPath.pop(self.comboBox_rtesPaths.currentIndex())
            self.comboBox_rtesPaths.removeItem(self.comboBox_rtesPaths.currentIndex())

    def push_modRtesPaths(self):
        cur_paths = self.dictRsi['RSI']['rtes'][self.comboBox_rtes.currentIndex()]['referencePaths'][
            self.comboBox_rtesPaths.currentIndex()]
        cur_paths['pathRadius'] = self.getNumValue(self.lineEdit_rtesPathRadius)

    def push_loadRtesPaths(self):
        if len(self.dictRsi['RSI']['rtes'][self.comboBox_rtes.currentIndex()]['referencePaths']) > 0:
            cur_paths = self.dictRsi['RSI']['rtes'][self.comboBox_rtes.currentIndex()]['referencePaths'][
                self.comboBox_rtesPaths.currentIndex()]
            self.lineEdit_rtesPathRadius.setText(str(cur_paths['pathRadius']))
            if len(cur_paths['points']) > 0:
                self.comboBox_rtesPathPos.clear()
                for pos in cur_paths['points']:
                    self.comboBox_rtesPathPos.addItem(str(pos['offset'][0]) + ', ' + str(pos['offset'][1]))

    def push_addRtesPos(self):
        td_pos = copy.deepcopy(self.dictPoint)
        td_pos['offset'][0] = self.getFloatValue(self.lineEdit_rtesPathLat)
        td_pos['offset'][1] = self.getFloatValue(self.lineEdit_rtesPathLon)
        cur_paths = self.dictRsi['RSI']['rtes'][self.comboBox_rtes.currentIndex()]['referencePaths'][
            self.comboBox_rtesPaths.currentIndex()]
        cur_paths['points'].append(td_pos)
        self.comboBox_rtesPathPos.addItem(str(td_pos['offset'][0]) + ', ' + str(td_pos['offset'][1]))

    def push_delRtesPos(self):
        cur_paths = self.dictRsi['RSI']['rtes'][self.comboBox_rtes.currentIndex()]['referencePaths'][
            self.comboBox_rtesPaths.currentIndex()]
        if len(cur_paths['points']) > 0:
            cur_paths['points'].pop(self.comboBox_rtesPathPos.currentIndex())
            self.comboBox_rtesPathPos.removeItem(self.comboBox_rtesPathPos.currentIndex())

    def push_addRtss(self):
        self.comboBox_rtssPaths.clear()
        self.comboBox_rtssPathPos.clear()
        td_rtss = copy.deepcopy(self.dictRtss)
        td_rtss['description']['present'] = self.comboBox_rtssDesc.currentIndex()
        td_rtss['description']['text'] = self.getStrValue(self.lineEdit_rtssDesc)
        td_rtss['rtsId'] = self.getNumValue(self.lineEdit_rtssId)
        td_rtss['signPos']['offset'][0] = self.getFloatValue(self.lineEdit_rtssLat)
        td_rtss['signPos']['offset'][1] = self.getFloatValue(self.lineEdit_rtssLon)
        #td_rtss['signType'] = self.getNumValue(self.lineEdit_rtssType)
        print(self.rtssTypeNumList[self.comboBox_rtssType.currentIndex()])
        td_rtss['signType'] = int(self.rtssTypeNumList[self.comboBox_rtssType.currentIndex()])
        td_rtss['priority'] = self.getNumValue(self.lineEdit_rtssPriority)

        cur_rtss = self.dictRsi['RSI']['rtss']
        cur_rtss.append(td_rtss)
        self.comboBox_rtss.addItem(str(td_rtss['rtsId']))
        self.comboBox_rtss.setCurrentIndex(self.comboBox_rtss.currentIndex()+1)

    def push_delRtss(self):
        if len(self.dictRsi['RSI']['rtss']) > 0:
            self.dictRsi['RSI']['rtss'].pop(self.comboBox_rtss.currentIndex())
            self.comboBox_rtss.removeItem(self.comboBox_rtss.currentIndex())

    def push_modRtss(self):
        cur_rtss = self.dictRsi['RSI']['rtss'][self.comboBox_rtss.currentIndex()]
        cur_rtss['description']['present'] = self.comboBox_rtssDesc.currentIndex()
        cur_rtss['description']['text'] = self.getStrValue(self.lineEdit_rtssDesc)
        cur_rtss['rtsId'] = self.getNumValue(self.lineEdit_rtssId)
        cur_rtss['signPos']['offset'][0] = self.getFloatValue(self.lineEdit_rtssLat)
        cur_rtss['signPos']['offset'][1] = self.getFloatValue(self.lineEdit_rtssLon)
        #cur_rtss['signType'] = self.getNumValue(self.lineEdit_rtssType)
        cur_rtss['signType'] = int(self.rtssTypeNumList[self.comboBox_rtssType.currentIndex()])
        cur_rtss['priority'] = self.getNumValue(self.lineEdit_rtssPriority)
        self.comboBox_rtes.setItemText(self.comboBox_rtss.currentIndex(), str(cur_rtss['rtsId']))

    def push_loadRtss(self):
        if len(self.dictRsi['RSI']['rtss']) > 0:
            cur_rtss = self.dictRsi['RSI']['rtss'][self.comboBox_rtss.currentIndex()]
            self.lineEdit_rtssDesc.setText(str(cur_rtss['description']['text']))
            self.lineEdit_rtssId.setText(str(cur_rtss['rtsId']))
            self.lineEdit_rtssLat.setText(str(cur_rtss['signPos']['offset'][0]/10000000))
            self.lineEdit_rtssLon.setText(str(cur_rtss['signPos']['offset'][1]/10000000))
            #self.lineEdit_rtssType.setText(str(cur_rtss['signType']))
            self.comboBox_rtssType.setCurrentIndex(self.rtssTypeNumList.index(str(cur_rtss['signType'])))
            self.lineEdit_rtssPriority.setText(str(cur_rtss['priority']))

            if len(cur_rtss['referencePaths']) > 0:
                self.comboBox_rtssPaths.clear()
                for i in range(len(cur_rtss['referencePaths'])):
                    self.comboBox_rtssPaths.addItem(str(i))

    def push_addRtssPaths(self):
        td_paths = copy.deepcopy(self.dictReferencePaths)
        td_paths['pathRadius'] = self.getNumValue(self.lineEdit_rtssPathRadius)
        cur_paths = self.dictRsi['RSI']['rtss'][self.comboBox_rtss.currentIndex()]['referencePaths']
        cur_paths.append(td_paths)
        self.comboBox_rtssPaths.addItem(str(self.comboBox_rtssPaths.currentIndex() + 1))
        self.comboBox_rtssPaths.setCurrentIndex(self.comboBox_rtssPaths.currentIndex() + 1)
        self.comboBox_rtssPathPos.clear()

    def push_delRtssPaths(self):
        cur_rtssPath = self.dictRsi['RSI']['rtss'][self.comboBox_rtss.currentIndex()]['referencePaths']
        if len(cur_rtssPath) > 0:
            cur_rtssPath.pop(self.comboBox_rtssPaths.currentIndex())
            self.comboBox_rtssPaths.removeItem(self.comboBox_rtssPaths.currentIndex())

    def push_modRtssPaths(self):
        cur_paths = self.dictRsi['RSI']['rtss'][self.comboBox_rtss.currentIndex()]['referencePaths'][
            self.comboBox_rtssPaths.currentIndex()]
        cur_paths['pathRadius'] = self.getNumValue(self.lineEdit_rtssPathRadius)

    def push_loadRtssPaths(self):
        if len(self.dictRsi['RSI']['rtss'][self.comboBox_rtss.currentIndex()]['referencePaths']) > 0:
            cur_paths = self.dictRsi['RSI']['rtss'][self.comboBox_rtss.currentIndex()]['referencePaths'][
                self.comboBox_rtssPaths.currentIndex()]
            self.lineEdit_rtssPathRadius.setText(str(cur_paths['pathRadius']))
            if len(cur_paths['points']) > 0:
                self.comboBox_rtssPathPos.clear()
                for pos in cur_paths['points']:
                    self.comboBox_rtssPathPos.addItem(str(pos['offset'][0]) + ', ' + str(pos['offset'][1]))

    def push_addRtssPos(self):
        td_pos = copy.deepcopy(self.dictPoint)
        td_pos['offset'][0] = self.getFloatValue(self.lineEdit_rtssPathLat)
        td_pos['offset'][1] = self.getFloatValue(self.lineEdit_rtssPathLon)

        cur_paths = self.dictRsi['RSI']['rtss'][self.comboBox_rtss.currentIndex()]['referencePaths'][
            self.comboBox_rtssPaths.currentIndex()]
        cur_paths['points'].append(td_pos)
        self.comboBox_rtssPathPos.addItem(str(td_pos['offset'][0]) + ', ' + str(td_pos['offset'][1]))

    def push_delRtssPos(self):
        cur_paths = self.dictRsi['RSI']['rtss'][self.comboBox_rtss.currentIndex()]['referencePaths'][
            self.comboBox_rtssPaths.currentIndex()]
        if len(cur_paths['points']) > 0:
            cur_paths['points'].pop(self.comboBox_rtssPathPos.currentIndex())
            self.comboBox_rtssPathPos.removeItem(self.comboBox_rtssPathPos.currentIndex())

    def push_save(self):
        if os.path.exists('v2xRsuGbRsi.cfg.tmp'):
            os.remove('v2xRsuGbRsi.cfg.tmp')
        if os.path.exists('v2xRsuGbRsi.cfg'):
            os.rename('v2xRsuGbRsi.cfg', 'v2xRsuGbRsi.cfg.tmp')
        #print(self.dictRsi['RSI'])
        for rtes in self.dictRsi['RSI']['rtes']:
            for rtesPaths in rtes['referencePaths']:
                rtesPaths['points'] = libconf.LibconfList(rtesPaths['points'])
            rtes['referencePaths'] = libconf.LibconfList(rtes['referencePaths'])
        self.dictRsi['RSI']['rtes'] = libconf.LibconfList(self.dictRsi['RSI']['rtes'])

        for rtss in self.dictRsi['RSI']['rtss']:
            for rtssPaths in rtss['referencePaths']:
                rtssPaths['points'] = libconf.LibconfList(rtssPaths['points'])
            rtss['referencePaths'] = libconf.LibconfList(rtss['referencePaths'])
        self.dictRsi['RSI']['rtss'] = libconf.LibconfList(self.dictRsi['RSI']['rtss'])

        #print(self.dictRsi)
        configText = libconf.dumps(self.dictRsi)
        #print(configText)
        with open('v2xRsuGbRsi.cfg', 'w') as fd_file:
            fd_file.write(configText)
            fd_file.close()

    def openConfFile(self):
        with io.open('v2xRsuGbRsi.cfg') as f:
            self.config = libconf.load(f)
        try:
            self.lon13 = self.config['RSI']['refPos'][0]
            self.lat13 = self.config['RSI']['refPos'][1]
            self.lon = self.lon13 / 10000000
            self.lat = self.lat13 / 10000000
            return True
        except:
            return False

    def push_open(self):
        self.loadMapFile()
        #print(self.config)32
        self.config['RSI']['rtes'] = libconf.LibconfArray(self.config['RSI']['rtes'])
        self.config['RSI']['rtss'] = libconf.LibconfArray(self.config['RSI']['rtss'])
        self.dictRsi = self.config

        self.comboBox_rtes.clear()
        for irtes, rtes in enumerate(self.config['RSI']['rtes']):
            self.comboBox_rtes.addItem(str(rtes['rteId']))
            self.comboBox_rtesPaths.clear()
            self.dictRsi['RSI']['rtes'][irtes]['referencePaths'] = libconf.LibconfArray(rtes['referencePaths'])
            for irtesPaths, rtesPaths in enumerate(rtes['referencePaths']):
                self.dictRsi['RSI']['rtes'][irtes]['referencePaths'][irtesPaths]['points'] = libconf.LibconfArray(
                    rtesPaths['points'])

        for irtss, rtss in enumerate(self.config['RSI']['rtss']):
            self.comboBox_rtss.addItem(str(rtss['rtsId']))
            self.comboBox_rtssPaths.clear()
            self.dictRsi['RSI']['rtss'][irtss]['referencePaths'] = libconf.LibconfArray(rtss['referencePaths'])
            for irtssPaths, rtssPaths in enumerate(rtss['referencePaths']):
                self.dictRsi['RSI']['rtss'][irtss]['referencePaths'][irtssPaths]['points'] = libconf.LibconfArray(
                    rtssPaths['points'])

        self.treeView_read.setModel(self.model_read)
        MsgContent_Dict = self.config['RSI']
        linkjson = json.dumps(MsgContent_Dict)
        self.model_read.loadJson(linkjson.encode())

    def loadMapFile(self):
        if self.openConfFile():
            self.loadMap()
            path = "file:\\" + os.getcwd() + "\\save_map.html"
            path = path.replace('\\', '/')
            self.qwebengine.load(QUrl(path))

    def push_ditu(self):
        self.loadMapFile()

    def loadMap(self):
        color_list = ['olive', 'pink', 'red', 'blue', 'orange', 'green', 'purple']
        color_num = 0
        map = folium.Map(location=[self.lon, self.lat], tiles="openstreetmap", zoom_start=18)
        map.add_child(folium.LatLngPopup())
        #map.add_child(folium.ClickForMarker())
        rtesList = self.config['RSI']['rtes']
        for rtes in rtesList:
            rtesEventPosList = [0, 0]
            rtesEventPosList[0] = rtes['eventPos']['offset'][0] / 10000000
            rtesEventPosList[1] = rtes['eventPos']['offset'][1] / 10000000
            draw_icon(map, rtesEventPosList, 'blue')
            for rtesPathi, rtesPaths in enumerate(rtes['referencePaths']):
                rtesPathsPosList = []
                for rtesPos in rtesPaths['points']:
                    rtesPosList = [0, 0]
                    rtesPosList[0] = rtesPos['offset'][0] / 10000000
                    rtesPosList[1] = rtesPos['offset'][1] / 10000000
                    rtesPathsPosList.append(rtesPosList)
                draw_lines(map, rtesPathsPosList, 3, color_list[color_num], 1,
                           'rtes-'+str(rtes['rteId'])+'-'+str(rtesPathi)+'-'+str(rtes['eventType']))
                color_num = 0 if color_num == (len(color_list)-1) else (color_num+1)

        rtssList = self.config['RSI']['rtss']
        for rtss in rtssList:
            rtssEventPosList = [0, 0]
            rtssEventPosList[0] = rtss['signPos']['offset'][0] / 10000000
            rtssEventPosList[1] = rtss['signPos']['offset'][1] / 10000000
            draw_icon(map, rtssEventPosList, 'red')
            for rtssPathi, rtssPaths in enumerate(rtss['referencePaths']):
                rtssPathsPosList = []
                for rtssPos in rtssPaths['points']:
                    rtssPosList = [0, 0]
                    rtssPosList[0] = rtssPos['offset'][0] / 10000000
                    rtssPosList[1] = rtssPos['offset'][1] / 10000000
                    rtssPathsPosList.append(rtssPosList)
                draw_lines(map, rtssPathsPosList, 3, color_list[color_num], 1,
                           'rtss-'+str(rtss['rtsId'])+'-'+str(rtssPathi)+'-'+str(rtss['signType']))
                color_num = 0 if color_num == (len(color_list)-1) else (color_num+1)
        map.save("save_map.html")
        curPath = os.getcwd().replace('\\', '/')
        replacetext('https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.js',
                    curPath+'/js/leaflet.js')
        replacetext('https://code.jquery.com/jquery-1.12.4.min.js',
                    curPath + '/js/jquery-1.12.4.min.js')
        replacetext('https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js',
                    curPath + '/js/bootstrap.min.js')
        replacetext('https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js',
                    curPath + '/js/leaflet.awesome-markers.js')
        replacetext('https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css',
                    curPath + '/js/leaflet.css')
        replacetext('https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css',
                    curPath + '/js/bootstrap.min.css')
        replacetext('https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css',
                    curPath + '/js/bootstrap-theme.min.css')
        replacetext('https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css',
                    curPath + '/js/font-awesome.min.css')
        replacetext('https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css',
                    curPath + '/js/leaflet.awesome-markers.css')
        replacetext('https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css',
                    curPath + '/js/leaflet.awesome.rotate.min.css')

def replacetext(search_text, replace_text):
    file = Path(r"save_map.html")
    data = file.read_text()
    data = data.replace(search_text, replace_text)
    file.write_text(data)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
