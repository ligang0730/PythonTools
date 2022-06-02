# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import io, libconf
import qtree as Qtree
import numpy as np
import folium
import math
import copy
from folium.plugins import HeatMap, MiniMap, MarkerCluster
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from ssh_form import Ui_Form
from enum import Enum
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from icon import *
from PyQt5.Qt import (QMutex, QThread)
from pathlib2 import Path

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
        draw_line(map, loclist[i], loclist[i+1], wei, col, opa, tip)

gQmtex = QMutex()
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

        self.poslanesList = []
        self.loadMapFile()
        self.dict = {"V2XMAP": {"MAPTX": {"MsgContent":[{"msgCount": 0, "timeStamp": 0, "nodes":[ ]}]}}}
        self.dictNode = {"desptName": "qf#1", "nodeRefID": {"region": 0, "id": 0}, "refPoint": [0, 0], "links": [ ]}
        self.movements = {"remoteNodeID": {"region": 0, "id": 0}, "signalGroup": 0}
        self.dictLink = {"desptName": "", "upstreamNodeId": {"region": 0, "id": 0},
                         "speedLimits": [{"type": 4, "speed": 0}, {"type": 5, "speed": 0}], "laneWidth": 0,
                         "points": [ ], "movements": [ ], "lanes": [ ]}
        self.dictLanes = {"laneID": 0, "laneWidth": 0,
                          "laneAttributes": {"sharedWith": 0, "laneType": {"present": 1, "value": 1}},"maneuvers": 1,
                          "points": [ ], "conctTo": [ ], "speedLimits":[{"type": 4, "speed": 0}, {"type": 5, "speed": 0}]}
        self.dictPoint = {"present": 7, "value": [0, 0]}
        self.dictConctTo = {"remoteNodeID": {"region": 0, "id": 2},
                            "connectingLane": {"laneID": 0, "maneuvers": 1}, "signalGroup":1}

        self.repoint = [0, 0]

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

    def push_creatnode(self):
        td_node = copy.deepcopy(self.dictNode)
        td_node['desptName'] = self.getStrValue(self.lineEdit_nodeName)
        td_node['nodeRefID']['region'] = self.getNumValue(self.lineEdit_nodeRegion)
        td_node['nodeRefID']['id'] = self.getNumValue(self.lineEdit_nodeId)
        td_node['refPoint'][0] = self.getFloatValue(self.lineEdit_nodeLat)
        td_node['refPoint'][1] = self.getFloatValue(self.lineEdit_nodeLon)

        self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'].append(td_node)
        self.repoint = td_node['refPoint']
        self.comboBox_nodexh.addItem(td_node['desptName'] + ':' + str(td_node['nodeRefID']['id']))

    def push_modnode(self):
        cur_node = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]
        #td_node = copy.deepcopy(self.dictNode)
        cur_node['desptName'] = self.getStrValue(self.lineEdit_nodeName)
        cur_node['nodeRefID']['region'] = self.getNumValue(self.lineEdit_nodeRegion)
        cur_node['nodeRefID']['id'] = self.getNumValue(self.lineEdit_nodeId)
        cur_node['refPoint'][0] = self.getFloatValue(self.lineEdit_nodeLat)
        cur_node['refPoint'][1] = self.getFloatValue(self.lineEdit_nodeLon)
        self.comboBox_nodexh.setItemText(self.comboBox_nodexh.currentIndex(),
                                         cur_node['desptName'] + ':' + str(cur_node['nodeRefID']['id']))

    def push_delnode(self):
        self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'].pop(self.comboBox_nodexh.currentIndex())
        self.comboBox_nodexh.removeItem(self.comboBox_nodexh.currentIndex())

    def push_loadnode(self):
        td_node = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes']
        if len(td_node) > 0:
            node = td_node[self.comboBox_nodexh.currentIndex()]
            self.lineEdit_nodeName.setText(str(node['desptName']))
            self.lineEdit_nodeRegion.setText(str(node['nodeRefID']['region']))
            self.lineEdit_nodeId.setText(str(node['nodeRefID']['id']))
            self.lineEdit_nodeLat.setText(str(node['refPoint'][0]/10000000))
            self.lineEdit_nodeLon.setText(str(node['refPoint'][1]/10000000))
            self.repoint = node['refPoint']

    def push_loadlink(self):
        td_link = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]['links']
        if len(td_link) > 0:
            self.comboBox_linkPointsxh.clear()
            self.comboBox_linkmovementxh.clear()
            link = td_link[self.comboBox_linkxh.currentIndex()]
            self.lineEdit_linkName.setText(str(link['desptName']))
            self.lineEdit_linkUpNodeId.setText(str(link['upstreamNodeId']['id']))
            self.lineEdit_linkSpeedDown.setText(str(link['speedLimits'][0]['speed']))
            self.lineEdit_linkSpeedUp.setText(str(link['speedLimits'][1]['speed']))
            self.lineEdit_linkWidth.setText(str(link['laneWidth']))

            for point in link['points']:
                self.comboBox_linkPointsxh.addItem(str(self.repoint[0] + point['value'][0])
                                                   + ',' + str(self.repoint[1] + point['value'][1]))
            for movements in link['movements']:
                self.comboBox_linkmovementxh.addItem(str(movements['remoteNodeID']['id']))

    def push_addlink(self):
        self.comboBox_linkPointsxh.clear()
        self.comboBox_linkmovementxh.clear()
        td_link = copy.deepcopy(self.dictLink)
        td_link['desptName'] = self.getStrValue(self.lineEdit_linkName)
        td_link['upstreamNodeId']['id'] = self.getNumValue(self.lineEdit_linkUpNodeId)
        td_link['speedLimits'][0]['speed'] = self.getNumValue(self.lineEdit_linkSpeedDown)
        td_link['speedLimits'][1]['speed'] = self.getNumValue(self.lineEdit_linkSpeedUp)
        td_link['laneWidth'] = self.getNumValue(self.lineEdit_linkWidth)
        curLink = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]['links']
        curLink.append(td_link)
        self.comboBox_linkxh.addItem(td_link['desptName'])
        self.comboBox_linkxh.setCurrentIndex(self.comboBox_linkxh.currentIndex()+1)

    def push_dellink(self):
        cur_link = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]['links']
        if len(cur_link) > 0:
            cur_link.pop(self.comboBox_linkxh.currentIndex())
            self.comboBox_linkxh.removeItem(self.comboBox_linkxh.currentIndex())

    def push_modlink(self):
        td_link = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]\
            ['links'][self.comboBox_linkxh.currentIndex()]
        td_link['desptName'] = self.getStrValue(self.lineEdit_linkName)
        td_link['upstreamNodeId']['id'] = self.getNumValue(self.lineEdit_linkUpNodeId)
        td_link['speedLimits'][0]['speed'] = self.getNumValue(self.lineEdit_linkSpeedDown)
        td_link['speedLimits'][1]['speed'] = self.getNumValue(self.lineEdit_linkSpeedUp)
        td_link['laneWidth'] = self.getNumValue(self.lineEdit_linkWidth)
        self.comboBox_linkxh.setItemText(self.comboBox_linkxh.currentIndex(), td_link['desptName'])

    def push_dellinkpoints(self):
        cur_linkpoint = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes']\
            [self.comboBox_nodexh.currentIndex()]['links'][self.comboBox_linkxh.currentIndex()]['points']
        if len(cur_linkpoint) > 0:
            cur_linkpoint.pop(self.comboBox_linkPointsxh.currentIndex())
            self.comboBox_linkPointsxh.removeItem(self.comboBox_linkPointsxh.currentIndex())

    def push_addlinkpoint(self):
        td_point = copy.deepcopy(self.dictPoint)
        td_point['value'][0] = self.getFloatValue(self.lineEdit_linkPointsLat) - self.repoint[0]
        td_point['value'][1] = self.getFloatValue(self.lineEdit_linkPointsLon) - self.repoint[1]

        self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]['links'] \
            [self.comboBox_linkxh.currentIndex()]['points'].append(td_point)
        self.comboBox_linkPointsxh.addItem(str(self.repoint[0] + td_point['value'][0])
                                           + ',' + str(self.repoint[1] + td_point['value'][1]))

    def push_loadlinkmovement(self):
        cur_movement = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]['links'] \
            [self.comboBox_linkxh.currentIndex()]['movements']
        if len(cur_movement) > 0:
            td_movement = cur_movement[self.comboBox_linkmovementxh.currentIndex()]
            self.lineEdit_linkDownNodeId.setText(str(td_movement['remoteNodeID']['id']))
            self.lineEdit_linkDownNodeSign.setText(str(td_movement['signalGroup']))

    def push_modlinkmovement(self):
        td_movements = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]['links'] \
            [self.comboBox_linkxh.currentIndex()]['movements'][self.comboBox_linkmovementxh.currentIndex()]
        td_movements['remoteNodeID']['id'] = self.getNumValue(self.lineEdit_linkDownNodeId)
        td_movements['signalGroup'] = self.getNumValue(self.lineEdit_linkDownNodeSign)

        self.comboBox_linkmovementxh.setItemText(self.comboBox_linkmovementxh.currentIndex(),
                                               str(td_movements['remoteNodeID']['id']))

    def push_dellinkmovement(self):
        cur_linkmovement = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes']\
            [self.comboBox_nodexh.currentIndex()]['links'][self.comboBox_linkxh.currentIndex()]['movements']
        if len(cur_linkmovement) > 0:
            cur_linkmovement.pop(self.comboBox_linkmovementxh.currentIndex())
            self.comboBox_linkmovementxh.removeItem(self.comboBox_linkmovementxh.currentIndex())

    def push_addlinkmovement(self):
        td_movements = copy.deepcopy(self.movements)
        td_movements['remoteNodeID']['id'] = self.getNumValue(self.lineEdit_linkDownNodeId)
        td_movements['signalGroup'] = self.getNumValue(self.lineEdit_linkDownNodeSign)

        self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]['links'] \
            [self.comboBox_linkxh.currentIndex()]['movements'].append(td_movements)
        self.comboBox_linkmovementxh.addItem(str(td_movements['remoteNodeID']['id']))

    def push_loadlanes(self):
        self.comboBox_lanesPointsxh.clear()
        self.comboBox_lanesConctToxh.clear()
        lanes = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]\
            ['links'][self.comboBox_linkxh.currentIndex()]['lanes']

        if len(lanes) > 0:
            td_lanes = lanes[self.comboBox_lanexh.currentIndex()]
            self.lineEdit_lanesId.setText(str(td_lanes['laneID']))
            self.lineEdit_lanesWidth.setText(str(td_lanes['laneWidth']))
            self.lineEdit_lanesManeuvers.setText(str(td_lanes['maneuvers']))
            self.lineEdit_lanesSpeedLimitUp.setText(str(td_lanes['speedLimits'][1]['speed']))
            self.lineEdit_lanesSpeedLimitDown.setText(str(td_lanes['speedLimits'][0]['speed']))

            for point in td_lanes['points']:
                self.comboBox_lanesPointsxh.addItem(str(self.repoint[0] + point['value'][0])
                                                    + ',' + str(self.repoint[1] + point['value'][1]))
            for conct in td_lanes['conctTo']:
                self.comboBox_lanesConctToxh.addItem((str(conct['remoteNodeID']['id'])
                                             + ':' + str(conct['connectingLane']['laneID'])))

    def push_addlanes(self):
        self.comboBox_lanesPointsxh.clear()
        self.comboBox_lanesConctToxh.clear()
        td_Lanes = copy.deepcopy(self.dictLanes)
        td_Lanes['laneID'] = self.getNumValue(self.lineEdit_lanesId)
        td_Lanes['laneWidth'] = self.getNumValue(self.lineEdit_lanesWidth)
        td_Lanes['maneuvers'] = self.getNumValue(self.lineEdit_lanesManeuvers)
        td_Lanes['speedLimits'][1]['speed'] = self.getNumValue(self.lineEdit_lanesSpeedLimitUp)
        td_Lanes['speedLimits'][0]['speed'] = self.getNumValue(self.lineEdit_lanesSpeedLimitDown)

        self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]['links'] \
            [self.comboBox_linkxh.currentIndex()]['lanes'].append(td_Lanes)
        self.comboBox_lanexh.addItem(str(td_Lanes['laneID']))
        self.comboBox_lanexh.setCurrentIndex(self.comboBox_lanexh.currentIndex()+1)

    def push_modlanes(self):
        td_Lanes = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]['links'] \
            [self.comboBox_linkxh.currentIndex()]['lanes'][self.comboBox_lanexh.currentIndex()]
        td_Lanes['laneID'] = self.getNumValue(self.lineEdit_lanesId)
        td_Lanes['laneWidth'] = self.getNumValue(self.lineEdit_lanesWidth)
        td_Lanes['maneuvers'] = self.getNumValue(self.lineEdit_lanesManeuvers)
        td_Lanes['speedLimits'][1]['speed'] = self.getNumValue(self.lineEdit_lanesSpeedLimitUp)
        td_Lanes['speedLimits'][0]['speed'] = self.getNumValue(self.lineEdit_lanesSpeedLimitDown)

        self.comboBox_lanexh.setItemText(self.comboBox_lanexh.currentIndex(),
                                                 str(td_Lanes['laneID']))

    def push_dellanes(self):
        cur_lane = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes']\
            [self.comboBox_nodexh.currentIndex()]['links'][self.comboBox_linkxh.currentIndex()]['lanes']
        if len(cur_lane) > 0:
            cur_lane.pop(self.comboBox_lanexh.currentIndex())
            self.comboBox_lanexh.removeItem(self.comboBox_lanexh.currentIndex())

    def push_dellanespoints(self):
        cur_lanespoint = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes']\
            [self.comboBox_nodexh.currentIndex()]['links'][self.comboBox_linkxh.currentIndex()]\
            ['lanes'][self.comboBox_lanexh.currentIndex()]['points']
        if len(cur_lanespoint) > 0:
            cur_lanespoint.pop(self.comboBox_lanesPointsxh.currentIndex())
            self.comboBox_lanesPointsxh.removeItem(self.comboBox_lanesPointsxh.currentIndex())

    def push_addlanespoint(self):
        td_point = copy.deepcopy(self.dictPoint)
        td_point['value'][0] = self.getFloatValue(self.lineEdit_lanesPointsLat) - self.repoint[0]
        td_point['value'][1] = self.getFloatValue(self.lineEdit_lanesPointsLon) - self.repoint[1]
        self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]['links'] \
            [self.comboBox_linkxh.currentIndex()]['lanes'][self.comboBox_lanexh.currentIndex()] \
            ['points'].append(td_point)
        self.comboBox_lanesPointsxh.addItem(str(self.repoint[0] + td_point['value'][0])
                                            + ',' + str(self.repoint[1] + td_point['value'][1]))

    def push_loadconct(self):
        cur_conct = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]['links'] \
            [self.comboBox_linkxh.currentIndex()]['lanes'][self.comboBox_lanexh.currentIndex()] \
            ['conctTo']
        if len(cur_conct) > 0:
            td_conct = cur_conct[self.comboBox_lanesConctToxh.currentIndex()]
            self.lineEdit_lanesNodeId.setText(str(td_conct['remoteNodeID']['id']))
            self.lineEdit_lanesDownNodeId.setText(str(td_conct['connectingLane']['laneID']))
            self.lineEdit_lanesDownManeuvers.setText(str(td_conct['connectingLane']['maneuvers']))
            self.lineEdit_lanesDownSign.setText(str(td_conct['signalGroup']))

    def push_modconct(self):
        td_ConctTo = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]['links'] \
            [self.comboBox_linkxh.currentIndex()]['lanes'][self.comboBox_lanexh.currentIndex()] \
            ['conctTo'][self.comboBox_lanesConctToxh.currentIndex()]
        td_ConctTo['remoteNodeID']['id'] = self.getNumValue(self.lineEdit_lanesNodeId)
        td_ConctTo['connectingLane']['laneID'] = self.getNumValue(self.lineEdit_lanesDownNodeId)
        td_ConctTo['connectingLane']['maneuvers'] = self.getNumValue(self.lineEdit_lanesDownManeuvers)
        td_ConctTo['signalGroup'] = self.getNumValue(self.lineEdit_lanesDownSign)

        self.comboBox_lanesConctToxh.setItemText(self.comboBox_lanesConctToxh.currentIndex(),
                                                 (str(td_ConctTo['remoteNodeID']['id'])
                                                  + ':' + str(td_ConctTo['connectingLane']['laneID'])))

    def push_delconct(self):
        cur_conct = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes']\
            [self.comboBox_nodexh.currentIndex()]['links'][self.comboBox_linkxh.currentIndex()]\
            ['lanes'][self.comboBox_lanexh.currentIndex()]['conctTo']
        if len(cur_conct) > 0:
            cur_conct.pop(self.comboBox_lanesConctToxh.currentIndex())
            self.comboBox_lanesConctToxh.removeItem(self.comboBox_lanesConctToxh.currentIndex())

    def push_addlanesconct(self):
        td_ConctTo = copy.deepcopy(self.dictConctTo)
        td_ConctTo['remoteNodeID']['id'] = self.getNumValue(self.lineEdit_lanesNodeId)
        td_ConctTo['connectingLane']['laneID'] = self.getNumValue(self.lineEdit_lanesDownNodeId)
        td_ConctTo['connectingLane']['maneuvers'] = self.getNumValue(self.lineEdit_lanesDownManeuvers)
        td_ConctTo['signalGroup'] = self.getNumValue(self.lineEdit_lanesDownSign)
        self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]['links'] \
            [self.comboBox_linkxh.currentIndex()]['lanes'][self.comboBox_lanexh.currentIndex()] \
            ['conctTo'].append(td_ConctTo)
        self.comboBox_lanesConctToxh.addItem(str(td_ConctTo['remoteNodeID']['id'])
                                             + ':' + str(td_ConctTo['connectingLane']['laneID']))

    def sign_tabPageChange(self, page):
        if len(self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes']) == 0:
            return
        if page == 0:
            list_node = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes']
            self.comboBox_nodexh.clear()
            if len(list_node) > 0:
                for node in list_node:
                    self.comboBox_nodexh.addItem(node['desptName'] + ':' + str(node['nodeRefID']['id']))
        elif page == 1:
            self.comboBox_linkxh.clear()
            list_link = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()]['links']
            if len(list_link) > 0:
                for link in list_link:
                    self.comboBox_linkxh.addItem(link['desptName'])
        elif page == 2:
            self.comboBox_lanexh.clear()
            list_lanes = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][self.comboBox_nodexh.currentIndex()] \
                ['links'][self.comboBox_linkxh.currentIndex()]['lanes']
            if len(list_lanes) > 0:
                for lane in list_lanes:
                    self.comboBox_lanexh.addItem(str(lane['laneID']))

    def sign_comboxChange_node(self, index):
        list_node = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes']
        if len(list_node) > 0:
            self.comboBox_linkxh.clear()
            list_link = list_node[index]['links']
            if len(list_link) > 0:
                for link in list_link:
                    self.comboBox_linkxh.addItem(link['desptName'])
                self.comboBox_lanexh.clear()
                list_lanes = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][index] \
                    ['links'][self.comboBox_linkxh.currentIndex()]['lanes']
                if len(list_lanes) > 0:
                    for lane in list_lanes:
                        self.comboBox_lanexh.addItem(str(lane['laneID']))

    def sign_comboxChange_link(self, index):
        list_link = self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes']\
            [self.comboBox_nodexh.currentIndex()]['links']
        if len(list_link) > 0:
            self.comboBox_lanexh.clear()
            list_lanes = list_link[index]['lanes']
            if len(list_lanes) > 0:
                for lane in list_lanes:
                    self.comboBox_lanexh.addItem(str(lane['laneID']))

    def push_save(self):
        if os.path.exists('v2xRsuGbMap.cfg.tmp'):
            os.remove('v2xRsuGbMap.cfg.tmp')
        if os.path.exists('v2xRsuGbMap.cfg'):
            os.rename('v2xRsuGbMap.cfg', 'v2xRsuGbMap.cfg.tmp')
        #print(self.dict)
        for node in self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes']:
            for link in node['links']:
                link['speedLimits'] = libconf.LibconfList(link['speedLimits'])
                link['points'] = libconf.LibconfList(link['points'])
                link['movements'] = libconf.LibconfList(link['movements'])
                for lanes in link['lanes']:
                    lanes['points'] = libconf.LibconfList(lanes['points'])
                    lanes['conctTo'] = libconf.LibconfList(lanes['conctTo'])
                    lanes['speedLimits'] = libconf.LibconfList(lanes['speedLimits'])
                link['lanes'] = libconf.LibconfList(link['lanes'])
            node['links'] = libconf.LibconfList(node['links'])
        self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'] = libconf.LibconfList(self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'])
        self.dict['V2XMAP']['MAPTX']['MsgContent'] = libconf.LibconfList(self.dict['V2XMAP']['MAPTX']['MsgContent'])

        #print(self.dict)
        configText = libconf.dumps(self.dict)
        print(configText)
        with open('v2xRsuGbMap.cfg', 'w') as fd_file:
            fd_file.write(configText)
            fd_file.close()

    def openConfFile(self):
        with io.open('v2xRsuGbMap.cfg') as f:
            self.config = libconf.load(f)
        try:
            self.lon13 = self.config['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][0]['refPoint'][0]
            self.lat13 = self.config['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][0]['refPoint'][1]
            self.lon = self.lon13 / 10000000
            self.lat = self.lat13 / 10000000
            return True
        except:
            return False

    def push_open(self):
        self.loadMapFile()
        self.config['V2XMAP']['MAPTX']['MsgContent'] = libconf.LibconfArray(self.config['V2XMAP']['MAPTX']['MsgContent'])
        self.config['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'] = \
            libconf.LibconfArray(self.config['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'])
        self.dict = self.config
        dict_node = self.config['V2XMAP']['MAPTX']['MsgContent'][0]['nodes']
        for nodei, node in enumerate(dict_node):
            self.comboBox_nodexh.addItem(node['desptName'] + ':' + str(node['nodeRefID']['id']))
            self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][nodei]['links'] \
                = libconf.LibconfArray(node['links'])
            for linki, link in enumerate(node['links']):
                self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][nodei]['links'] \
                    [linki]['speedLimits'] = libconf.LibconfArray(link['speedLimits'])
                self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][nodei]['links'] \
                    [linki]['lanes'] = libconf.LibconfArray(link['lanes'])
                for lanesi, lanes in enumerate(link['lanes']):
                    self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][nodei]['links'] \
                        [linki]['lanes'][lanesi]['points'] = libconf.LibconfArray(lanes['points'])
                    self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][nodei]['links'] \
                        [linki]['lanes'][lanesi]['conctTo'] = libconf.LibconfArray(lanes['conctTo'])
                try:
                    self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][nodei]['links']\
                        [linki]['points'] = libconf.LibconfArray(link['points'])
                except:
                    pass
                try:
                    self.dict['V2XMAP']['MAPTX']['MsgContent'][0]['nodes'][nodei]['links'] \
                        [linki]['movements'] = libconf.LibconfArray(link['movements'])
                except:
                    pass

        self.treeView_read.setModel(self.model_read)
        MsgContent_Dict = self.config['V2XMAP']['MAPTX']['MsgContent'][0]
        linkjson = json.dumps(MsgContent_Dict)
        self.model_read.loadJson(linkjson.encode())

    def loadMapFile(self):
        if self.openConfFile():
            self.reLoadMap()
            path = "file:\\" + os.getcwd() + "\\save_map.html"
            path = path.replace('\\', '/')
            gQmtex.lock()
            self.qwebengine.load(QUrl(path))
            gQmtex.unlock()

    def push_ditu(self):
        self.loadMapFile()

    def reLoadMap(self):
        color_list = ['olive', 'pink', 'red', 'blue', 'orange', 'green', 'purple']
        color_num = 0
        map = folium.Map(location=[self.lon, self.lat], tiles="openstreetmap", zoom_start=18)
        map.add_child(folium.LatLngPopup())
        # map.add_child(folium.ClickForMarker())

        nodeList = self.config['V2XMAP']['MAPTX']['MsgContent'][0]['nodes']
        for inode in nodeList:
            nodeId = inode['nodeRefID']['id']
            for ilink in inode['links']:
                linkName = ilink['desptName']
                try:
                    linkpointstart = [(self.lon13 + ilink['points'][0]['value'][0]) / 10000000,
                                   (self.lat13 + ilink['points'][0]['value'][1]) / 10000000]
                    draw_icon(map, linkpointstart, 'blue')
                except:
                    pass
                for ilanes in ilink['lanes']:
                    lanesId = ilanes['laneID']
                    try:
                        self.laneWidth = ilanes['laneWidth']
                    except:
                        pass
                    pointslanesList = []
                    for ilanespos in ilanes['points']:
                        pointslanesList.append([(self.lon13 + ilanespos['value'][0]) / 10000000,
                                                (self.lat13 + ilanespos['value'][1]) / 10000000])
                    self.poslanesList.append(pointslanesList)
                    curMane = ilanes['maneuvers']
                    draw_lines(map, pointslanesList, 3, color_list[color_num], 1,
                               str(nodeId) + '-' + linkName + '-' + str(lanesId) + ':' + str(E_Maneuvers(curMane)))
            color_num = 0 if color_num == (len(color_list) - 1) else (color_num + 1)

        gQmtex.lock()
        map.save("save_map.html")
        curPath = os.getcwd().replace('\\', '/')
        replacetext('https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.js',
                    curPath + '/js/leaflet.js')
        replacetext('https://code.jquery.com/jquery-1.12.4.min.js',
                    curPath + '/js/jquery-1.12.4.min.js')
        replacetext('https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js',
                    curPath + '/js/bootstrap.min.js')
        replacetext(
            'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js',
            curPath + '/js/leaflet.awesome-markers.js')
        replacetext('https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css',
                    curPath + '/js/leaflet.css')
        replacetext('https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css',
                    curPath + '/js/bootstrap.min.css')
        replacetext('https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css',
                    curPath + '/js/bootstrap-theme.min.css')
        replacetext('https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css',
                    curPath + '/js/font-awesome.min.css')
        replacetext(
            'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css',
            curPath + '/js/leaflet.awesome-markers.css')
        replacetext(
            'https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css',
            curPath + '/js/leaflet.awesome.rotate.min.css')
        gQmtex.unlock()

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
