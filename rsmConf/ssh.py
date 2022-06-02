# -*- coding: utf-8 -*-

import os
import sys
import json
import io, libconf
import qtree as Qtree
import folium
import copy
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
def draw_Circle(map, loc, col, radius):
    folium.CircleMarker(
        location=loc,
        radius=radius,
        color=col,
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

        self.dictRsm = {"RSM": {"id": "", "refPos": [0, 0, 0], "Participants": []}}
        self.Participants = {"ptcType": 0, "ptcId": 0, "SourceType": 0, "speed": 0,
                             "heading": 0, "Pos": {"present": 7, "offset": [0, 0]},
                             "Size": {"width": 0, "length": 0, "height": 0}}

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

    def push_rsmMod(self):
        cur_rsm = self.dictRsm['RSM']
        cur_rsm['id'] = self.lineEdit_rsmId.text()
        cur_rsm['refPos'][0] = self.getFloatValue(self.lineEdit_refLat)
        cur_rsm['refPos'][1] = self.getFloatValue(self.lineEdit_refLon)
        cur_rsm['refPos'][2] = self.getFloatValue(self.lineEdit_refEle)
        print(cur_rsm['refPos'])

    def push_rsmLoad(self):
        cur_rsm = self.dictRsm['RSM']
        self.lineEdit_rsmId.setText(str(cur_rsm['id']))
        self.lineEdit_refLat.setText(str(cur_rsm['refPos'][0] / 10000000))
        self.lineEdit_refLon.setText(str(cur_rsm['refPos'][1] / 10000000))
        self.lineEdit_refEle.setText(str(cur_rsm['refPos'][2] / 10000000))

    def push_add(self):
        td_part = copy.deepcopy(self.Participants)
        td_part['ptcType'] = self.comboBox_ptcType.currentIndex()
        td_part['ptcId'] = self.getNumValue(self.lineEdit_ptcId)
        td_part['SourceType'] = self.comboBox_SourceType.currentIndex()
        td_part['speed'] = self.getNumValue(self.lineEdit_speed)
        td_part['heading'] = self.getNumValue(self.lineEdit_heading)
        td_part['Size']['width'] = self.getNumValue(self.lineEdit_width)
        td_part['Size']['length'] = self.getNumValue(self.lineEdit_length)
        td_part['Size']['height'] = self.getNumValue(self.lineEdit_height)
        td_part['Pos']['offset'][0] = self.getFloatValue(self.lineEdit_lat)
        td_part['Pos']['offset'][1] = self.getFloatValue(self.lineEdit_lon)

        cur_part = self.dictRsm['RSM']['Participants']
        cur_part.append(td_part)
        self.comboBox_part.addItem(str(td_part['ptcId']))
        self.comboBox_part.setCurrentIndex(self.comboBox_part.currentIndex()+1)

    def push_del(self):
        if len(self.dictRsm['RSM']['Participants']) > 0:
            self.dictRsm['RSM']['Participants'].pop(self.comboBox_part.currentIndex())
            self.comboBox_part.removeItem(self.comboBox_part.currentIndex())

    def push_mod(self):
        cur_part = self.dictRsm['RSM']['Participants'][self.comboBox_part.currentIndex()]
        cur_part['ptcType'] = self.comboBox_ptcType.currentIndex()
        cur_part['ptcId'] = self.getNumValue(self.lineEdit_ptcId)
        cur_part['SourceType'] = self.comboBox_SourceType.currentIndex()
        cur_part['speed'] = self.getNumValue(self.lineEdit_speed)
        cur_part['heading'] = self.getNumValue(self.lineEdit_heading)
        cur_part['Size']['width'] = self.getNumValue(self.lineEdit_width)
        cur_part['Size']['length'] = self.getNumValue(self.lineEdit_length)
        cur_part['Size']['height'] = self.getNumValue(self.lineEdit_height)
        cur_part['Pos']['offset'][0] = self.getFloatValue(self.lineEdit_lat)
        cur_part['Pos']['offset'][1] = self.getFloatValue(self.lineEdit_lon)
        self.comboBox_part.setItemText(self.comboBox_part.currentIndex(), str(cur_part['ptcId']))

    def push_load(self):
        if len(self.dictRsm['RSM']['Participants']) > 0:
            cur_part = self.dictRsm['RSM']['Participants'][self.comboBox_part.currentIndex()]
            self.lineEdit_ptcId.setText(str(cur_part['ptcId']))
            self.lineEdit_speed.setText(str(cur_part['speed']))
            self.lineEdit_heading.setText(str(cur_part['heading']))
            self.lineEdit_lat.setText(str(cur_part['Pos']['offset'][0] / 10000000))
            self.lineEdit_lon.setText(str(cur_part['Pos']['offset'][1] / 10000000))
            self.lineEdit_width.setText(str(cur_part['Size']['width']))
            self.lineEdit_length.setText(str(cur_part['Size']['length']))
            self.lineEdit_height.setText(str(cur_part['Size']['height']))
            self.comboBox_ptcType.setCurrentIndex(cur_part['ptcType'])
            self.comboBox_SourceType.setCurrentIndex(cur_part['SourceType'])

    def push_save(self):
        if os.path.exists('v2xRsuGbRsm.cfg.tmp'):
            os.remove('v2xRsuGbRsm.cfg.tmp')
        if os.path.exists('v2xRsuGbRsm.cfg'):
            os.rename('v2xRsuGbRsm.cfg', 'v2xRsuGbRsm.cfg.tmp')
        self.dictRsm['RSM']['Participants'] = libconf.LibconfList(self.dictRsm['RSM']['Participants'])
        configText = libconf.dumps(self.dictRsm)
        with open('v2xRsuGbRsm.cfg', 'w') as fd_file:
            fd_file.write(configText)
            fd_file.close()

    def openConfFile(self):
        with io.open('v2xRsuGbRsm.cfg') as f:
            self.config = libconf.load(f)
        try:
            self.lon13 = self.config['RSM']['refPos'][0]
            self.lat13 = self.config['RSM']['refPos'][1]
            self.lon = self.lon13 / 10000000
            self.lat = self.lat13 / 10000000
            return True
        except:
            return False

    def push_open(self):
        self.loadMapFile()
        #print(self.config)
        self.config['RSM']['Participants'] = libconf.LibconfArray(self.config['RSM']['Participants'])
        self.dictRsm = self.config

        self.comboBox_part.clear()
        for ipart, part in enumerate(self.dictRsm['RSM']['Participants']):
            self.comboBox_part.addItem(str(part['ptcId']))

        self.treeView_read.setModel(self.model_read)
        MsgContent_Dict = self.config['RSM']
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
        color_list = ['red', 'orange', 'darkblue', 'lightgray', 'green',
                      'blue', 'black', 'darkgreen', 'gray', 'lightblue',
                      'beige', 'lightred', 'cadetblue', 'purple', 'lightgreen',
                      'darkpurple', 'white', 'darkred', 'pink']
        color_num = 0
        map = folium.Map(location=[self.lon, self.lat],
                         tiles='openstreetmap',
                         zoom_start=18)
        map.add_child(folium.LatLngPopup())
        #map.add_child(folium.ClickForMarker())
        partList = self.config['RSM']['Participants']
        for part in partList:
            partPosList = [0, 0]
            partPosList[0] = part['Pos']['offset'][0] / 10000000
            partPosList[1] = part['Pos']['offset'][1] / 10000000
            #draw_icon(map, partPosList, color_list[color_num])
            draw_Circle(map, partPosList, color_list[color_num], part['Size']['width'])
            color_num = 0 if color_num == (len(color_list) - 1) else (color_num + 1)

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
