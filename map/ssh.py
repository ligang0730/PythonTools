# -*- coding: utf-8 -*-

import os
import sys
import threading
import time
import paramiko
import json
import io, libconf
import qtree as Qtree
import numpy as np
import pandas as pd
import numpy as np
import folium
import math
from pynng import Pair0, Pair1

import random
from folium.plugins import HeatMap, MiniMap, MarkerCluster
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QEventLoop, QTimer, QStringListModel
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from ssh_form import Ui_Form
from enum import Enum
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtWebEngineWidgets
from geographiclib.geodesic import Geodesic
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import sys
import os
import folium
import copy

class E_DriveBehavior(Enum):
    goStraightForward = 0            #直行
    laneChangingToLeft = 1           #向左变更车道
    laneChangingToRight = 2          #向右变更车道
    rampIn = 3                       #驶入
    rampOut = 4                      #驶出
    intersectionStraightThrough = 5  #直行通过交叉路口
    intersectionTurnLeft = 6         #左转通过交叉路口
    intersectionTurnRight = 7        #右转通过交叉路口
    intersectionUTurn = 8            #掉头通过交叉路口
    stop = 10                        #停止
    slowdown = 11                    #减速慢行
    speedup = 12                     #加速行驶
    parking = 13                     #泊车

class E_Maneuvers(Enum):
    STRAIGHT = 0
    LEFTTURN = 1
    RIGHTTURN = 2
    UTURN = 3

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
        draw_line(map, loclist[i], loclist[i+1], wei, col, opa, tip + str(i))

def calgeo(loclist):
    for i in range(len(loclist)-1):
        geoResult = Geodesic.WGS84.Inverse(loclist[i][0], loclist[i][1], loclist[i+1][0], loclist[i+1][1])
        #print(geoResult)

def geoInit():
    #temp = Geodesic.WGS84.Inverse(loc1[0], loc1[1], loc2[0], loc2[1])
    geod = Geodesic.WGS84  # define the WGS84 ellipsoid
    #geod = Geodesic(6378388, 1/297.0) # altanatively custom the ellipsoid
    return geod

def getGeoInfo(loc1, loc2):
    geo = geoInit()
    geoinfo = geo.Inverse(loc1[0], loc1[1], loc2[0], loc2[1])
    return geoinfo

def getTarLoc(loc, brng, dist):
    #unit: azimuth (N=0deg), distance (m)
    geo = geoInit()
    tarloc = geo.Direct(loc[0], loc[1], brng, dist)
    return tarloc['lat2'], tarloc['lon2']

def calTarLoc(loc, brng, dist): #dist单位：米
    lat1 = loc[0]
    lon1 = loc[1]
    earth_arc = 111.199 #地球每度的弧长,单位：千米
    dist = dist / 1000
    brng = math.radians(brng)
    lon2 = lon1 + (dist * math.sin(brng)) / (earth_arc * math.cos(math.radians(lat1)))
    lat2 = lat1 + (dist * math.cos(brng)) / earth_arc
    return lat2, lon2

def point_distance_line(point,line_point1,line_point2):
    #计算向量
    vec1 = line_point1 - point
    vec2 = line_point2 - point
    distance = np.abs(np.cross(vec1,vec2)) / np.linalg.norm(line_point1-line_point2)
    return distance

def get_distance_from_point_to_line(point, line_point1, line_point2):
    #对于两点坐标为同一点时,返回点与点的距离
    if line_point1 == line_point2:
        point_array = np.array(point )
        point1_array = np.array(line_point1)
        return np.linalg.norm(point_array -point1_array )
    #计算直线的三个参数
    A = line_point2[1] - line_point1[1]
    B = line_point1[0] - line_point2[0]
    C = (line_point1[1] - line_point2[1]) * line_point1[0] + \
        (line_point2[0] - line_point1[0]) * line_point1[1]
    #根据点到直线的距离公式计算距离
    distance = np.abs(A * point[0] + B * point[1] + C) / (np.sqrt(A**2 + B**2))
    return distance


#加载url文件相对位置的子线程
class Refresh_temp_url(QThread):
    single_refresh_temp_url = pyqtSignal(str)
    def __init__(self):
        super(Refresh_temp_url,self).__init__()
        self.RunStatus = True
    def run(self):
        while self.RunStatus:
            path = str(os.getcwd()) + "\\save_map.html"
            self.url_path = path.replace('\\', '/')
            self.single_refresh_temp_url.emit(str(self.url_path))
            time.sleep(2)
    def stop(self):
        self.RunStatus = False

class itemfileinfo:
    def __init__(self, carId, startlinkName, startlaneId, startroadXh,
                 endlinkName, endlaneId, endroadXh, speed, color):
        self.carId = carId
        self.startlinkName = startlinkName
        self.startlaneId = startlaneId
        self.startroadXh = startroadXh
        self.endlinkName = endlinkName
        self.endlaneId = endlaneId
        self.endroadXh = endroadXh
        self.speed = speed
        self.color = color

    def __repr__(self):
        return "%s    %s    %s    %s    %s    %s    %s    %s    %s" % \
               (self.carId, self.startlinkName, self.startlaneId, self.startroadXh,
                self.endlinkName, self.endlaneId, self.endroadXh, self.speed,
                self.color)

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
        #sys.stdout = EmittingStr(textWritten=self.outputWritten)
        #sys.stderr = EmittingStr(textWritten=self.outputWritten)
        self.listView.setStyleSheet("background:#ffffff")
        self.showlist = []
        self.fileinfo = itemfileinfo('', '', '', '', '', '', '', '', '')
        self.listmodel = QStringListModel(self)
        self.listmodel.setStringList(self.showlist)
        self.listView.setModel(self.listmodel)
        self.listmodel.dataChanged.connect(self.lvsave)

        with io.open('v2xRsuGbMap.cfg') as f:
            self.config = libconf.load(f)
            self.lat13 = self.config['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][0]['refPoint'][0]
            self.lon13 = self.config['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][0]['refPoint'][1]
            self.lat = self.lat13 / 10000000
            self.lon = self.lon13 / 10000000

        # 新建一个QWebEngineView()对象
        self.qwebengine = QWebEngineView(self.frame)  # 设置网页在窗口中显示的位置和大小
        self.qwebengine.setGeometry(QtCore.QRect(0, 0, 701, 571))  # 在QWebEngineView中加载网址
        self.gridLayout.addWidget(self.qwebengine, 0, 0, 1, 1)

        self.catCount = 0
        self.poslanesList = []  #画线用
        self.roadInfoList = []
        self.laneWidth = 10

        self.firstLoadMap()
        self.loadMapFile()
        #self.fram_5_information_temp_graph()

        tdlinks = self.config['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][0]['links']
        self.roadInfoList = self.getroadInfo(tdlinks)
        self.pool = ThreadPoolExecutor(max_workers=2)

    # def outputWritten(self, text):
    #     # self.textEdit.clear()
    #     cursor = self.textEdit.textCursor()
    #     cursor.movePosition(QtGui.QTextCursor.End)
    #     cursor.insertText(text)
    #     self.textEdit.setTextCursor(cursor)
    #     self.textEdit.ensureCursorVisible()

    def getroadInfo(self, linkInfo):
        roadInfoList = []
        for link in linkInfo:
            linkDict = {"linkName": "", "laneInfo": []}
            for lane in link['lanes']:
                laneDict = {"laneId": 1, "points": []}
                for ipos in range(len(lane['points'])-1):
                    pointDict = {"startpos": [0.0, 0.0], "endpos": [0.0, 0.0], "brng": 0.0, "dist": 0.0}

                    pointDict['startpos'][0] = (self.lat13 + lane['points'][ipos]['value'][0]) / 10000000
                    pointDict['startpos'][1] = (self.lon13 + lane['points'][ipos]['value'][1]) / 10000000

                    pointDict['endpos'][0] = (self.lat13 + lane['points'][ipos+1]['value'][0]) / 10000000
                    pointDict['endpos'][1] = (self.lon13 + lane['points'][ipos+1]['value'][1]) / 10000000

                    geoInfo = getGeoInfo(pointDict['startpos'], pointDict['endpos'])
                    pointDict['brng'] = geoInfo['azi1']
                    pointDict['dist'] = geoInfo['s12']
                    laneDict['points'].append(pointDict)
                laneDict['laneId'] = lane['laneID']
                linkDict['laneInfo'].append(laneDict)
            linkDict['linkName'] = link['desptName']
            roadInfoList.append(linkDict)
        return roadInfoList

    def fram_5_information_temp_graph(self):
        self.refresh_temp = Refresh_temp_url() #建立子线程链接
        self.refresh_temp.single_refresh_temp_url.connect(self.refresh_temp_url_2)#链接信号并将数据创给方法refresh_temp_url_2
        self.refresh_temp.start()

    def refresh_temp_url_2(self,path_url):
        self.qwebengine.load(QUrl.fromLocalFile(path_url))#获得子程序传来的数据，每10s更新一次显示

    def loadMapFile(self):
        path = "file:\\" + os.getcwd() + "\\save_map.html"
        path = path.replace('\\', '/')
        self.qwebengine.load(QUrl(path))

    def push_connect(self):
        PORT = int(self.lineEdit_port.text())
        HOST_IP = self.lineEdit_ip.text()
        nn_hostip = 'tcp://' + str(HOST_IP) + ':' + str(PORT)
        self.nn_pairA = Pair0()
        self.nn_pairA.dial(nn_hostip)
        self.pushButton_connect.setEnabled(False)

    def push_start(self):
        carInfoList = []
        carNum = self.listmodel.rowCount()
        for i in range(carNum):
            carDict = {'carId': 0, 'speed': 0, 'color': "",
                       'roadinfo': [{'linkName': "", 'laneId': 1, 'roadXh': 0, 'pos': [0, 0]},
                                    {'linkName': "", 'laneId': 1, 'roadXh': 0, 'pos': [0, 0]}]}
            carDict['carId'] = int(self.showlist[i].split('    ')[0], 16)
            carDict['roadinfo'][0]['linkName'] = self.showlist[i].split('    ')[1]
            carDict['roadinfo'][0]['laneId'] = int(self.showlist[i].split('    ')[2])
            carDict['roadinfo'][0]['roadXh'] = int(self.showlist[i].split('    ')[3])
            carDict['roadinfo'][1]['linkName'] = self.showlist[i].split('    ')[4]
            carDict['roadinfo'][1]['laneId'] = int(self.showlist[i].split('    ')[5])
            carDict['roadinfo'][1]['roadXh'] = int(self.showlist[i].split('    ')[6])
            carDict['speed'] = int(self.showlist[i].split('    ')[7])
            carDict['color'] = self.showlist[i].split('    ')[8]

            for roadinfo in self.roadInfoList:
                for i in range(len(carDict['roadinfo'])):
                    if roadinfo['linkName'] == carDict['roadinfo'][i]['linkName']:
                        for lane in roadinfo['laneInfo']:
                            if lane['laneId'] == carDict['roadinfo'][i]['laneId']:
                                if carDict['roadinfo'][i]['roadXh'] > (len(lane['points'])-1):
                                    carDict['roadinfo'][i]['roadXh'] = len(lane['points'])-1
                                #carDict['startPos'] = lane['points'][carDict['startroadXh']]['startpos']
                                #catDict['endPos'] = lane['points'][catDict['startroadXh']]['startpos']

            carInfoList.append(carDict)
            #print(carInfoList)

        self.t1_RunStatus = True
        self.t1 = threading.Thread(target=self.startRunCart, args=(carInfoList, ))
        self.t1.setDaemon(True)
        self.t1.start()
        self.pushButton_start.setEnabled(False)
        self.pushButton_stop.setEnabled(True)
        self.fram_5_information_temp_graph()

        self.t2_RunStatus = True
        self.t2 = threading.Thread(target=self.recvSuggestion, args=())
        self.t2.setDaemon(True)
        self.t2.start()

    def setSuggestionLabel(self, sugg, label_sugg):
        driveBehaviorList = ["直行", "左转", "右转", "汇入", "汇出", "交叉路口直行", "交叉路口左转", "交叉路口右转",
                             "交叉路口调头", "暂停避让", "停下", "减速通过", "加速通过", "驶入停车场"]
        label_sugg.setText(driveBehaviorList[sugg])

    def clearSuggestionLabel(self, timelist):
        if timelist[0] == 20:
            self.label_sugg0.setText("-")
        if timelist[1] == 20:
            self.label_sugg1.setText("-")
        if timelist[2] == 20:
            self.label_sugg2.setText("-")
        if timelist[3] == 20:
            self.label_sugg3.setText("-")
        if timelist[4] == 20:
            self.label_sugg4.setText("-")

    def recvSuggestion(self):
        clearTimeList = [0,0,0,0,0]
        while self.t2_RunStatus:
            try:
                data = self.nn_pairA.recv()
                msg_json = bytes.decode(data)
                dict_data = json.loads(msg_json)
                for i, v in enumerate(clearTimeList):
                    clearTimeList[i] = v + 1
                self.clearSuggestionLabel(clearTimeList)
                if dict_data['type'] == "suggestion":
                    for sd in dict_data['data']:
                        if sd['carid'] == self.label_carid1.text():
                            clearTimeList[1] = 0
                            self.setSuggestionLabel(sd['suggestion'], self.label_sugg1)
                        elif sd['carid'] == self.label_carid2.text():
                            clearTimeList[2] = 0
                            self.setSuggestionLabel(sd['suggestion'], self.label_sugg2)
                        elif sd['carid'] == self.label_carid3.text():
                            clearTimeList[3] = 0
                            self.setSuggestionLabel(sd['suggestion'], self.label_sugg3)
                        elif sd['carid'] == self.label_carid4.text():
                            clearTimeList[4] = 0
                            self.setSuggestionLabel(sd['suggestion'], self.label_sugg4)
                        else:
                            clearTimeList[0] = 0
                            self.setSuggestionLabel(sd['suggestion'], self.label_sugg0)
                elif dict_data['type'] == "vir":
                    #print(dict_data['vir']['light'], dict_data['vir']['vehClass'])
                    if dict_data['vir']['light'] == 4:
                        self.label_curB.setText("左转")
                    elif dict_data['vir']['light'] == 8:
                        self.label_curB.setText("右转")
                    else:
                        self.label_curB.setText("直行")
            except:
                pass

    def push_pause(self):
        pass

    def push_continue(self):
        pass

    def push_stop(self):
        self.t1_RunStatus = False
        self.t2_RunStatus = False
        self.refresh_temp.stop()
        self.pushButton_start.setEnabled(True)
        self.pushButton_stop.setEnabled(False)

    def push_del(self):
        index = self.listView.currentIndex()
        self.listmodel.removeRow(index.row())

    def push_add(self):
        self.catCount += 1
        self.lineEdit_catName.setText(str(self.catCount))
        self.fileinfo.carId = self.catCount
        self.fileinfo.startlinkName = str(self.comboBox_startLinkName.currentText())
        self.fileinfo.startlaneId = str(self.comboBox_startLaneId.currentText())
        self.fileinfo.startroadXh = str(self.comboBox_startroadxh.currentText())
        self.fileinfo.endlinkName = str(self.comboBox_endLinkName.currentText())
        self.fileinfo.endlaneId = str(self.comboBox_endLaneId.currentText())
        self.fileinfo.endroadXh = str(self.comboBox_endroadxh.currentText())
        self.fileinfo.speed = str(self.comboBox_speed.currentText())
        self.fileinfo.color = str(self.comboBox_color.currentText())

        row = self.listmodel.rowCount()
        self.listmodel.insertRow(row)
        self.listmodel.setData(self.listmodel.index(row), str(self.fileinfo))

    def lvsave(self):
        self.showlist = self.listmodel.stringList()

    def judgeInLane(self, catState):
        curloc = catState['curloc']
        for roadinfo in self.roadInfoList:
            if catState['linkName'] == roadinfo['linkName']:
                for lane in roadinfo['laneInfo']:
                    if catState['laneId'] == lane['laneId']:
                        for i in range(len(lane['points'])):
                            sgeoInfo = getGeoInfo(lane['points'][i]['startpos'], curloc)
                            egeoInfo = getGeoInfo(lane['points'][i]['endpos'], curloc)
                            sdist = sgeoInfo['s12']
                            edist = egeoInfo['s12']
                            offsetdist = sdist + edist - catState['speed'] - 1
                            if offsetdist < lane['points'][i]['dist']:  # 点在线段内
                                catState['linkName'] = roadinfo['linkName']
                                catState['laneId'] = lane['laneId']
                                catState['roadXh'] = i
                                #catState['curbrng'] = egeoInfo['azi1'] + 180
                                catState['curbrng'] = lane['points'][i]['brng']
                                catState['curloc'] = catState['tarloc']
        return catState

    def runCarInit(self, carInfo, curStep):
        cartdict = {"carId": 0, "speed": 0, "color": "", "curloc": [0.0, 0.0],
                    "tarloc": [0.0, 0.0], "linkName": "", "laneId": 0, "roadXh": 0, "curbrng": 0.0}
        for roadinfo in self.roadInfoList:
            if carInfo['roadinfo'][curStep]['linkName'] == roadinfo['linkName']:
                for lane in roadinfo['laneInfo']:
                    if carInfo['roadinfo'][curStep]['laneId'] == lane['laneId']:
                        cartdict['curloc'] = lane['points'][carInfo['roadinfo'][curStep]['roadXh']]['startpos']
                        cartdict['curbrng'] = lane['points'][carInfo['roadinfo'][curStep]['roadXh']]['brng']
                        cartdict['linkName'] = roadinfo['linkName']
                        cartdict['laneId'] = lane['laneId']
                        cartdict['roadXh'] = carInfo['roadinfo'][curStep]['roadXh']
                        cartdict['carId'] = carInfo['carId']
                        cartdict['speed'] = carInfo['speed']
                        cartdict['color'] = carInfo['color']
                        break
        return cartdict

    def runCarFinish(self, carState, carInfo, curStep):
        stepRet = curStep
        for roadinfo in self.roadInfoList:
            if carState['linkName'] == roadinfo['linkName']:
                for lane in roadinfo['laneInfo']:
                    if carState['laneId'] == lane['laneId'] and carState['roadXh'] == (len(lane['points'])-1):
                        if carState['carId'] == carInfo['carId']:
                            stepRet += 1
                            if stepRet > 1:
                                stepRet = 0
        return stepRet

    def startRunCart(self, carInfoList):
        runStepList = []
        carStatelist = []
        for j in range(len(carInfoList)):
            runStepList.append(0)
            carStatelist.append(copy.deepcopy(self.runCarInit(carInfoList[j], runStepList[j])))
        #self.step = random.randint(1, 5)
        while self.t1_RunStatus:
            sendDict = {"data": []}
            for carSt in carStatelist:
                dict = {"id": 0, "lat": 0, "lon": 0, "brng": 0}
                carSt['tarloc'] = getTarLoc(carSt['curloc'], carSt['curbrng'], carSt['speed'])
                dict['id'] = carSt['carId']
                dict['lat'] = carSt['tarloc'][0] * 10000000
                dict['lon'] = carSt['tarloc'][1] * 10000000
                dict['brng'] = carSt['curbrng'] + 180
                sendDict['data'].append(dict)
                #print(carSt['tarloc'])
            #print("----------------")
            try:
                sendmsgjson = json.dumps(sendDict)
                #sendmsgjson
                #print(sendmsgjson)
                self.nn_pairA.send(sendmsgjson.encode())
            except:
                pass

            self.refreshMap(carStatelist)
            for catState in carStatelist:
                catState = self.judgeInLane(catState)
            for carIn in carInfoList:
                for i in range(len(carStatelist)):
                    ret = self.runCarFinish(carStatelist[i], carIn, runStepList[i])
                    #print(ret, runStepList[i])
                    if ret != runStepList[i]:
                        runStepList[i] = ret
                        carStatelist[i] = self.runCarInit(carIn, runStepList[i])
            time.sleep(2)

    def refreshMap(self, cartStatelist):
        zoom = int(self.comboBox_zoom.currentText())
        map = folium.Map(location=[self.lat, self.lon], tiles="openstreetmap", zoom_start=zoom)
        map.add_child(folium.LatLngPopup())

        for lane in self.poslanesList:
            draw_lines(map, lane, 3, "silver", 1, "")

        for carSt in cartStatelist:
            draw_line(map, carSt['curloc'], carSt['tarloc'], 3, carSt['color'], 1, "")

        map.save("save_map.html")

    def firstLoadMap(self):
        combox_speed_list = ['1', '3', '5', '7', '9', '11']
        combox_color_list = ['olive', 'pink', 'red', 'blue', 'orange', 'green', 'purple']
        combox_zoom_list = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        combox_link_list = []
        combox_lane_list = []
        combox_road_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
        map = folium.Map(location=[self.lat, self.lon], tiles="openstreetmap", zoom_start=17)
        map.add_child(folium.LatLngPopup())
        # map.add_child(folium.ClickForMarker())
        self.linkList = self.config['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][0]['links']
        for ilink in self.linkList:
            linkName = ilink['desptName']
            combox_link_list.append(linkName)
            # linkspeedLimitsUp = ilink['speedLimits'][0]['speed']
            # linkspeedLimitsDn = ilink['speedLimits'][1]['speed']
            # try:
            #     linkpoints = [[(self.lon13 + ilink['points'][0]['value'][0]) / 10000000,
            #                    (self.lat13 + ilink['points'][0]['value'][1]) / 10000000],
            #                   [(self.lon13 + ilink['points'][1]['value'][0]) / 10000000,
            #                    (self.lat13 + ilink['points'][1]['value'][1]) / 10000000]]
            #     draw_lines(map, linkpoints, 5, "grey", 0.5,
            #                'speedLimits' + ':' + str(linkspeedLimitsUp) + ', ' + str(linkspeedLimitsDn))
            # except:
            #     pass
            for ilanes in ilink['lanes']:
                lanesId = ilanes['laneID']
                combox_lane_list.append(str(lanesId))
                # lanespeedLimitsUp = ilanes['speedLimits'][0]['speed']
                # lanespeedLimitsDn = ilanes['speedLimits'][1]['speed']
                try:
                    self.laneWidth = ilanes['laneWidth']
                except:
                    pass
                pointslanesList = []
                for ilanespos in ilanes['points']:
                    pointslanesList.append([(self.lat13 + ilanespos['value'][0]) / 10000000,
                                            (self.lon13 + ilanespos['value'][1]) / 10000000])
                self.poslanesList.append(pointslanesList)
                curMane = ilanes['maneuvers']
                for conctTo in ilanes['conctTo']:
                    nextMane = conctTo['connectingLane']['maneuvers']
                    draw_MarkerCluster(map, pointslanesList[-1],
                                       'curMane:' + str(E_Maneuvers(curMane)),
                                       'nextMane:' + str(E_Maneuvers(nextMane)))
                draw_icon(map, pointslanesList[0], 'blue')
                draw_lines(map, pointslanesList, 3, "silver", 1,
                           linkName + '-' + str(lanesId) + ': ')
                map.save("save_map.html")

        self.comboBox_startLinkName.addItems(combox_link_list)
        self.comboBox_endLinkName.addItems(combox_link_list)
        self.comboBox_startLaneId.addItems(combox_lane_list)
        self.comboBox_endLaneId.addItems(combox_lane_list)
        self.comboBox_startroadxh.addItems(combox_road_list)
        self.comboBox_endroadxh.addItems(combox_road_list)
        #self.comboBox_endroadxh.setCurrentIndex(6)
        self.comboBox_speed.addItems(combox_speed_list)
        self.comboBox_speed.setCurrentIndex(3)
        self.comboBox_color.addItems(combox_color_list)
        self.comboBox_color.setCurrentIndex(2)
        self.comboBox_zoom.addItems(combox_zoom_list)
        self.comboBox_zoom.setCurrentIndex(7)

    def cal_limite(self, loc1, loc2, wei):
        locdict = {"locstart": [], "locend": [], "locdist": 0, "brng": 0}
        geoinfo = getGeoInfo(loc1, loc2)
        locdict['brng'] = geoinfo['azi1']
        locdict['locstart'] = loc1
        locdict['locend'] = loc2
        locdict['locdist'] = geoinfo['s12']
        return locdict


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
