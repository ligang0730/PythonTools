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
import paho.mqtt.client as mqtt
import datetime

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QEventLoop, QTimer, QStringListModel
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from ssh_form import Ui_Form
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt, QAbstractListModel, QMimeData, \
    QDataStream, QByteArray, QJsonDocument, QVariant, QJsonValue, QJsonParseError
from PyQt5.QtWidgets import QApplication, QFileDialog, QTreeView
from multiprocessing import Process, Pipe

global child_conn_Register, parent_conn_Register
global child_conn_BaseInfo, parent_conn_BaseInfo
global child_conn_OpertionConf, parent_conn_OpertionConf
global child_conn_DeviceState, parent_conn_DeviceState
global child_conn_ServiceState, parent_conn_ServiceState
global child_conn_ServiceConf, parent_conn_ServiceConf
global child_conn_Alarm, parent_conn_Alarm
global child_conn_HeartBeat, parent_conn_HeartBeat
global child_conn_Bsm, parent_conn_Bsm
global child_conn_Spat, parent_conn_Spat
global child_conn_MsgStatus, parent_conn_MsgStatus
global child_conn_MsgConf, parent_conn_MsgMsgConf

global autorecvflag

class QJsonTreeItem(object):
    def __init__(self, parent=None):
        self.mParent = parent
        self.mChilds = []
        self.mType =None
        self.mValue =None

    def appendChild(self, item):
        self.mChilds.append(item)

    def child(self, row:int):
        return self.mChilds[row]

    def parent(self):
        return self.mParent

    def childCount(self):
        return len(self.mChilds)

    def row(self):
        if self.mParent is not None:
            return self.mParent.mChilds.index(self)
        return 0

    def setKey(self, key:str):
        self.mKey = key

    def setValue(self, value:str):
       self. mValue = value

    def setType(self, type:QJsonValue.Type):
        self.mType = type

    def key(self):
        return self.mKey

    def value(self):
        return self.mValue

    def type(self):
        return self.mType

    def load(self, value, parent=None):
        rootItem = QJsonTreeItem(parent)
        rootItem.setKey("root")
        jsonType = None
        try:
            value = value.toVariant()
            jsonType = value.type()
        except AttributeError:
            pass
        try:
            value = value.toObject()
            jsonType = value.type()
        except AttributeError:
            pass
        if isinstance(value, dict):
            # process the key/value pairs
            for key in value:
                v = value[key]
                child = self.load(v, rootItem)
                child.setKey(key)
                try:
                    child.setType(v.type())
                except AttributeError:
                    child.setType(v.__class__)
                rootItem.appendChild(child)
        elif isinstance(value, list):
            # process the values in the list
            for i, v in enumerate(value):
                child = self.load(v, rootItem)
                child.setKey(str(i))
                child.setType(v.__class__)
                rootItem.appendChild(child)
        else:
            # value is processed
            rootItem.setValue(value)
            try:
                rootItem.setType(value.type())
            except AttributeError:
                if jsonType is not None:
                    rootItem.setType(jsonType)
                else:
                    rootItem.setType(value.__class__)
        return rootItem

class QJsonModel(QAbstractItemModel):
    def __init__(self, parent =None):
        super().__init__(parent)
        self.mRootItem = QJsonTreeItem()
        self.mHeaders = ["key","value","type"]

    def load(self, fileName):
        if fileName is None or fileName is False:
            return False
        with open(fileName,"rb",) as file:
            if file is None:
                return False
            else:
                self.loadJson(file.read())

    def loadJson(self, json):
        error = QJsonParseError()
        self.mDocument = QJsonDocument.fromJson(json,error)
        if self.mDocument is not None:
            self.beginResetModel()
            if self.mDocument.isArray():
                self.mRootItem.load(list(self.mDocument.array()))
            else:
                self.mRootItem = self.mRootItem.load(self.mDocument.object())
            self.endResetModel()
            return True
        print("QJsonModel: error loading Json")
        return False

    def data(self, index: QModelIndex, role: int = ...):
        if not index.isValid():
            return QVariant()
        item = index.internalPointer()
        col = index.column()
        if role == Qt.DisplayRole:
            if col == 0:
                return str(item.key())
            elif col == 1:
                return str(item.value())
            elif col == 2:
                return str(item.type())
        return QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            return self.mHeaders[section]
        return QVariant()

    def index(self, row: int, column: int, parent: QModelIndex = ...):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parentItem = self.mRootItem
        else:
            parentItem = parent.internalPointer()
        try:
            childItem = parentItem.child(row)
            return self.createIndex(row, column, childItem)
        except IndexError:
            return QModelIndex()

    def parent(self, index: QModelIndex):
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem == self.mRootItem:
            return QModelIndex()
        return self.createIndex(parentItem.row(),0, parentItem)

    def rowCount(self, parent: QModelIndex = ...):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.mRootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def columnCount(self, parent: QModelIndex = ...):
        return 3

class MQTTClient(object):
    def __init__(self, host, port):
        self._client = mqtt.Client()  # create MQTT client
        self.host = host
        self.port = port
        self.on_message = None
        self.msg_topic = None
        self.msg_payload = None
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = False
        self._client.on_message = self._on_message
        self._connected = False
        self._client.on_publish = self._on_publish

    def connect(self, username, password):
        self._client.username_pw_set(username, password)
        self._client.connect(self.host, self.port, 60)

    def disconnect(self):
        self._client.loop_stop()
        print("Client disconnect called.")
        pass

    def _on_connect(self, client, userdata, flags, rc):
        print("Client on_connect called.")

    def is_connected(self):
        return self._connected

    def _on_message(self, client, userdata, msg):
        global child_conn_Register, child_conn_BaseInfo, child_conn_OpertionConf, child_conn_ServiceConf,\
            child_conn_DeviceState, child_conn_ServiceState, child_conn_Alarm, child_conn_HeartBeat,\
            child_conn_Bsm, child_conn_MsgStatus, child_conn_MsgConf
        global autorecvflag

        msgTopic = msg.topic
        msgData = msg.payload
        msg_data = bytes.decode(msgData)
        tindex = msg_data.rfind('}')
        msg_json = msg_data[:tindex + 1]
        jsonstring = msg_json.encode()
        try:
            dict_json = json.loads(msg_json)
            dict_tag = dict_json['tag']
        except:
            dict_tag = 0
            pass

        if dict_tag == 10001:
            child_conn_BaseInfo.send(jsonstring)
            child_conn_BaseInfo.send(dict_json)
        elif dict_tag == 10002:
            child_conn_OpertionConf.send(dict_json)
        elif dict_tag == 10003:
            child_conn_ServiceConf.send(dict_json)
        elif dict_tag == 10007:
            child_conn_Register.send(jsonstring)

        if autorecvflag == 1:
            if msgTopic.rfind('bsm') >= 0:
                child_conn_Bsm.send(jsonstring)
            if msgTopic.rfind('spat') >= 0:
                child_conn_Spat.send(jsonstring)
            if dict_tag == 10004:
                child_conn_DeviceState.send(jsonstring)
            if dict_tag == 10005:
                child_conn_ServiceState.send(jsonstring)
            if dict_tag == 10006:
                child_conn_Alarm.send(jsonstring)
            if dict_tag == 10008:
                child_conn_HeartBeat.send(jsonstring)
        else:
            if dict_tag == 30001:
                child_conn_BaseInfo.send(jsonstring)
                child_conn_BaseInfo.send(dict_json)
            if dict_tag == 30002:
                child_conn_OpertionConf.send(dict_json)
            if dict_tag == 30003:
                child_conn_ServiceConf.send(dict_json)
            if dict_tag == 30004:
                child_conn_DeviceState.send(jsonstring)
            if dict_tag == 30005:
                child_conn_ServiceState.send(jsonstring)
            if dict_tag == 10011:
                child_conn_MsgStatus.send(dict_json)
            if dict_tag == 10012:
                child_conn_MsgConf.send(dict_json)

    def _on_publish(self, client, userdata, result):
        pass

    def _on_subscribe(self, client, userdata, result):
        pass

    def on_loopstart(self):
        self._client.loop_start()

    def on_subscribe(self, topic):
        self._client.subscribe(topic)
        self._client.on_message = self._on_message

    def on_publish(self, topic, msg, qos):
        self._client.publish(topic, payload=str(msg), qos=qos)

class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        global autorecvflag
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)
        self.pushBrokerDis.setEnabled(False)
        self.pushPublish.setEnabled(False)
        self.pushQuery.setEnabled(False)
        self.pushStartRecv.setEnabled(False)

        self.treeView_Register.setStyleSheet("background:#ffffff")
        self.treeView_BaseInfo.setStyleSheet("background:#ffffff")
        #self.treeView_OpertionConf.setStyleSheet("background:#ffffff")
        self.treeView_DeviceState.setStyleSheet("background:#ffffff")
        self.treeView_ServiceState.setStyleSheet("background:#ffffff")
        #self.treeView_ServiceConf.setStyleSheet("background:#ffffff")
        self.treeView_Alarm.setStyleSheet("background:#ffffff")
        self.treeView_Map_tx.setStyleSheet("background:#ffffff")
        self.treeView_Rsi_tx.setStyleSheet("background:#ffffff")
        self.treeView_Rsm_tx.setStyleSheet("background:#ffffff")
        self.treeView_Bsm_tx.setStyleSheet("background:#ffffff")
        self.treeView_Spat_tx.setStyleSheet("background:#ffffff")
        self.treeView_Map_rx.setStyleSheet("background:#ffffff")
        self.treeView_Rsi_rx.setStyleSheet("background:#ffffff")
        self.treeView_Rsm_rx.setStyleSheet("background:#ffffff")
        self.treeView_Bsm_rx.setStyleSheet("background:#ffffff")
        self.treeView_Spat_rx.setStyleSheet("background:#ffffff")

        self.model_Register = QJsonModel()
        self.model_BaseInfo = QJsonModel()
        self.model_OpertionConf = QJsonModel()
        self.model_DeviceState = QJsonModel()
        self.model_ServiceState = QJsonModel()
        self.model_ServiceConf = QJsonModel()
        self.model_Alarm = QJsonModel()
        self.model_Map = QJsonModel()
        self.model_Rsi = QJsonModel()
        self.model_Rsm = QJsonModel()
        self.model_Bsm = QJsonModel()
        self.model_Spat = QJsonModel()

        autorecvflag = 0
        self.seqNum = 0

    def push_broker(self):
        brokerip = self.lineEdit_serverip.text()
        user = self.lineEdit_user.text()
        pswd = self.lineEdit_pswd.text()
        stopic = self.lineEdit_stopic.text()
        stopic2 = self.lineEdit_stopic_2.text()
        try:
            self.client = MQTTClient(brokerip, 1883)
            self.client.connect(user, pswd)
            self.client.on_subscribe(stopic)
            self.client.on_subscribe(stopic2)
            self.client.on_loopstart()
        except:
            return
        self.pushBroker.setEnabled(False)
        self.pushBrokerDis.setEnabled(True)
        self.pushPublish.setEnabled(True)
        self.pushQuery.setEnabled(True)
        self.pushStartRecv.setEnabled(True)

        self.t1 = threading.Thread(target=self.startShowJsontreeView_Register, args=())
        self.t1.setDaemon(True)
        self.t1.start()

        self.t2 = threading.Thread(target=self.startShowJsontreeView_BaseInfo, args=())
        self.t2.setDaemon(True)
        self.t2.start()

        self.t3 = threading.Thread(target=self.startShowJsontreeView_OpertionConf, args=())
        self.t3.setDaemon(True)
        self.t3.start()

        self.t4 = threading.Thread(target=self.startShowJsontreeView_DeviceState, args=())
        self.t4.setDaemon(True)
        self.t4.start()

        self.t5 = threading.Thread(target=self.startShowJsontreeView_ServiceState, args=())
        self.t5.setDaemon(True)
        self.t5.start()

        self.t6 = threading.Thread(target=self.startShowJsontreeView_ServiceConf, args=())
        self.t6.setDaemon(True)
        self.t6.start()

        self.t7 = threading.Thread(target=self.startShowJsontreeView_Alarm, args=())
        self.t7.setDaemon(True)
        self.t7.start()

        self.t8 = threading.Thread(target=self.startShowJsontreeView_HeartBeat, args=())
        self.t8.setDaemon(True)
        self.t8.start()

        self.t9 = threading.Thread(target=self.startShowJsontreeView_Bsm, args=())
        self.t9.setDaemon(True)
        self.t9.start()

        self.t10 = threading.Thread(target=self.startShowJsontreeView_Spat, args=())
        self.t10.setDaemon(True)
        self.t10.start()

        self.t11 = threading.Thread(target=self.startShowJsonLable_MsgStatus, args=())
        self.t11.setDaemon(True)
        self.t11.start()

        self.t12 = threading.Thread(target=self.startShowJsonLable_MsgConf, args=())
        self.t12.setDaemon(True)
        self.t12.start()

    def startShowJsontreeView_Register(self):
        global parent_conn_Register
        cnt = 0
        while True:
            self.treeView_Register.setModel(self.model_Register)
            starttime = datetime.datetime.now()
            msg = parent_conn_Register.recv()
            cnt += 1
            endtime = datetime.datetime.now()
            duringtime = endtime - starttime
            self.model_Register.loadJson(msg)
            self.label_DeviceRegister.setText(str(cnt))
            self.label_DeviceRegister_2.setText(str(duringtime.seconds))

    def startShowJsontreeView_BaseInfo(self):
        global parent_conn_BaseInfo
        cnt = 0
        while True:
            self.treeView_BaseInfo.setModel(self.model_BaseInfo)
            starttime = datetime.datetime.now()
            msg = parent_conn_BaseInfo.recv()
            try:
                msg_dist = msg['msgData']
                self.lineEdit_deviceId.setText(str(msg_dist['deviceId']))
                self.lineEdit_deviceName.setText(str(msg_dist['deviceName']))
                self.lineEdit_regionCode.setText(str(msg_dist['regionCode']))
                self.lineEdit_curCommType.setText(str(msg_dist['curCommType']))
                self.lineEdit_ip.setText(str(msg_dist['ip']))
                self.lineEdit_port.setText(str(msg_dist['port']))
                self.lineEdit_gatewayIP.setText(str(msg_dist['gatewayIP']))
                self.lineEdit_mask.setText(str(msg_dist['mask']))
                self.lineEdit_deviceGroupType.setText(str(msg_dist['deviceGroupType']))
                self.lineEdit_deviceGroupCode.setText(str(msg_dist['deviceGroupCode']))
                self.lineEdit_montantId.setText(str(msg_dist['montantId']))
                self.lineEdit_locationDesc.setText(str(msg_dist['locationDesc']))
                self.lineEdit_locationType.setText(str(msg_dist['locationType']))
                self.lineEdit_owner.setText(str(msg_dist['owner']))
                self.lineEdit_transEncryption.setText(str(msg_dist['transEncryption']))
            except:
                self.model_BaseInfo.loadJson(msg)
            cnt += 1
            endtime = datetime.datetime.now()
            duringtime = endtime - starttime
            self.label_DeviceBaseInfo.setText(str(cnt))
            self.label_DeviceBaseInfo_2.setText(str(duringtime.seconds))

    def startShowJsontreeView_OpertionConf(self):
        global parent_conn_OpertionConf
        cnt = 0
        while True:
            #self.treeView_OpertionConf.setModel(self.model_OpertionConf)
            starttime = datetime.datetime.now()
            msg = parent_conn_OpertionConf.recv()
            msg_dist = msg['msgData']
            cnt += 1
            endtime = datetime.datetime.now()
            duringtime = endtime - starttime
            # self.model_OpertionConf.loadJson(msg)
            self.label_OpertionConf.setText(str(cnt))
            self.label_OpertionConf_2.setText(str(duringtime.seconds))

            self.lineEdit_deviceId2.setText(msg_dist['deviceId'])
            self.lineEdit_heartbeatRate.setText(str(msg_dist['heartbeatRate']))
            self.lineEdit_deviceRunningInfoRate.setText(str(msg_dist['deviceRunningInfoRate']))
            self.lineEdit_appRunningInfoRate.setText(str(msg_dist['appRunningInfoRate']))
            self.lineEdit_logInfoRate.setText(str(msg_dist['logInfoRate']))
            self.lineEdit_alarmInfoRate.setText(str(msg_dist['alarmInfoRate']))

    def startShowJsontreeView_DeviceState(self):
        global parent_conn_DeviceState
        cnt = 0
        while True:
            self.treeView_DeviceState.setModel(self.model_DeviceState)
            starttime = datetime.datetime.now()
            msg = parent_conn_DeviceState.recv()
            cnt += 1
            endtime = datetime.datetime.now()
            duringtime = endtime - starttime
            self.model_DeviceState.loadJson(msg)
            self.label_DeviceState.setText(str(cnt))
            self.label_DeviceState_2.setText(str(duringtime.seconds))

    def startShowJsontreeView_ServiceState(self):
        global parent_conn_ServiceState
        cnt = 0
        while True:
            self.treeView_ServiceState.setModel(self.model_ServiceState)
            starttime = datetime.datetime.now()
            msg = parent_conn_ServiceState.recv()
            cnt += 1
            endtime = datetime.datetime.now()
            duringtime = endtime - starttime
            self.model_ServiceState.loadJson(msg)
            self.label_ServiceState.setText(str(cnt))
            self.label_ServiceState_2.setText(str(duringtime.seconds))

    def startShowJsontreeView_ServiceConf(self):
        global parent_conn_ServiceConf
        cnt = 0
        while True:
            #self.treeView_ServiceConf.setModel(self.model_ServiceConf)
            starttime = datetime.datetime.now()
            msg = parent_conn_ServiceConf.recv()
            msg_dist = msg['msgData']
            cnt += 1
            endtime = datetime.datetime.now()
            duringtime = endtime - starttime
            #self.model_ServiceConf.loadJson(msg)
            self.label_ServiceConf.setText(str(cnt))
            self.label_ServiceConf_2.setText(str(duringtime.seconds))

            self.lineEdit_upLimit.setText(str(msg_dist['mapConfig']['upLimit']))
            self.lineEdit_downLimit.setText(str(msg_dist['mapConfig']['downLimit']))
            self.lineEdit_upFilterskey1.setText(str(msg_dist['mapConfig']['upFilters'][0]))
            self.lineEdit_upFiltersval1.setText(str(msg_dist['mapConfig']['upFilters'][1]))
            self.lineEdit_upFilterskey2.setText(str(msg_dist['mapConfig']['upFilters'][2]))
            self.lineEdit_upFiltersval2.setText(str(msg_dist['mapConfig']['upFilters'][3]))

            self.lineEdit_upLimit_3.setText(str(msg_dist['rsiConfig']['upLimit']))
            self.lineEdit_downLimit_3.setText(str(msg_dist['rsiConfig']['downLimit']))
            self.lineEdit_upFilterskey5.setText(str(msg_dist['rsiConfig']['upFilters'][0]))
            self.lineEdit_upFiltersval5.setText(str(msg_dist['rsiConfig']['upFilters'][1]))
            self.lineEdit_upFilterskey6.setText(str(msg_dist['rsiConfig']['upFilters'][2]))
            self.lineEdit_upFiltersval6.setText(str(msg_dist['rsiConfig']['upFilters'][3]))

            self.lineEdit_upLimit_4.setText(str(msg_dist['rsmConfig']['upLimit']))
            self.lineEdit_downLimit_4.setText(str(msg_dist['rsmConfig']['downLimit']))
            self.lineEdit_upFilterskey7.setText(str(msg_dist['rsmConfig']['upFilters'][0]))
            self.lineEdit_upFiltersval7.setText(str(msg_dist['rsmConfig']['upFilters'][1]))
            self.lineEdit_upFilterskey8.setText(str(msg_dist['rsmConfig']['upFilters'][2]))
            self.lineEdit_upFiltersval8.setText(str(msg_dist['rsmConfig']['upFilters'][3]))

            self.lineEdit_upLimit_5.setText(str(msg_dist['spatConfig']['upLimit']))
            self.lineEdit_downLimit_5.setText(str(msg_dist['spatConfig']['downLimit']))
            self.lineEdit_upFilterskey9.setText(str(msg_dist['spatConfig']['upFilters'][0]))
            self.lineEdit_upFiltersval9.setText(str(msg_dist['spatConfig']['upFilters'][1]))
            self.lineEdit_upFilterskey10.setText(str(msg_dist['spatConfig']['upFilters'][2]))
            self.lineEdit_upFiltersval10.setText(str(msg_dist['spatConfig']['upFilters'][3]))

            self.lineEdit_sampleMode.setText(str(msg_dist['bsmConfig']['sampleMode']))
            self.lineEdit_sampleRate.setText(str(msg_dist['bsmConfig']['sampleRate']))
            self.lineEdit_upLimit_2.setText(str(msg_dist['bsmConfig']['upLimit']))
            self.lineEdit_downLimit_2.setText(str(msg_dist['bsmConfig']['downLimit']))
            self.lineEdit_upFilterskey3.setText(str(msg_dist['bsmConfig']['upFilters'][0]))
            self.lineEdit_upFiltersval3.setText(str(msg_dist['bsmConfig']['upFilters'][1]))
            self.lineEdit_upFilterskey4.setText(str(msg_dist['bsmConfig']['upFilters'][2]))
            self.lineEdit_upFiltersval4.setText(str(msg_dist['bsmConfig']['upFilters'][3]))

    def startShowJsontreeView_Alarm(self):
        global parent_conn_Alarm
        cnt = 0
        while True:
            self.treeView_Alarm.setModel(self.model_Alarm)
            starttime = datetime.datetime.now()
            msg = parent_conn_Alarm.recv()
            cnt += 1
            endtime = datetime.datetime.now()
            duringtime = endtime - starttime
            self.model_Alarm.loadJson(msg)
            self.label_Alarm.setText(str(cnt))
            self.label_Alarm_2.setText(str(duringtime.seconds))

    def startShowJsontreeView_HeartBeat(self):
        global parent_conn_HeartBeat
        cnt = 0
        while True:
            starttime = datetime.datetime.now()
            msg = parent_conn_HeartBeat.recv()
            cnt += 1
            endtime = datetime.datetime.now()
            duringtime = endtime - starttime
            self.label_HeartBeat.setText(str(cnt))
            self.label_HeartBeat_2.setText(str(duringtime.seconds))

    def startShowJsontreeView_Bsm(self):
        global parent_conn_Bsm
        cnt = 0
        while True:
            self.treeView_Bsm_rx.setModel(self.model_Bsm)
            starttime = datetime.datetime.now()
            msg = parent_conn_Bsm.recv()
            cnt += 1
            endtime = datetime.datetime.now()
            duringtime = endtime - starttime
            self.model_Bsm.loadJson(msg)
            self.label_BsmRx.setText(str(cnt))
            self.label_BsmRx_2.setText(str(duringtime.seconds))

    def startShowJsontreeView_Spat(self):
        global parent_conn_Spat
        cnt = 0
        while True:
            self.treeView_Spat_rx.setModel(self.model_Spat)
            starttime = datetime.datetime.now()
            msg = parent_conn_Spat.recv()
            cnt += 1
            endtime = datetime.datetime.now()
            duringtime = endtime - starttime
            self.model_Spat.loadJson(msg)
            self.label_SpatRx.setText(str(cnt))
            self.label_SpatRx_2.setText(str(duringtime.seconds))

    def showBool(self, date):
        if date == True:
            return "成功"
        elif date == False:
            return "失败"
        else:
            return "-"

    def startShowJsonLable_MsgStatus(self):
        global parent_conn_MsgStatus
        while True:
            msg = parent_conn_MsgStatus.recv()
            msg_dist = msg['msgData']
            tab_curindex = self.tabWidget_set.currentIndex()
            if tab_curindex == 11:
                try:
                    self.label_msgsinits.setText(self.showBool(msg_dist['vx_module_init_status']))
                    self.label_msgsrs.setText(self.showBool(msg_dist['vx_module_rx_status']))
                    self.label_msgts.setText(self.showBool(msg_dist['vx_module_tx_status']))
                    self.label_msgsmapts.setText(self.showBool(msg_dist['map_tx_status']))
                    self.label_msgsrsits.setText(self.showBool(msg_dist['rsi_tx_status']))
                    self.label_msgsspatts.setText(self.showBool(msg_dist['spat_tx_status']))
                    self.label_msgsrsmts.setText(self.showBool(msg_dist['rsm_tx_status']))
                    self.label_msgsrtcmts.setText(self.showBool(msg_dist['rtcm_tx_status']))
                    self.label_msgsbsmrs.setText(self.showBool(msg_dist['bsm_rx_status']))
                except:
                    pass
                try:
                    self.label_msgsmap.setText(self.showBool(msg_dist['map']['cfg_load_status']))
                    self.label_msgsmap_2.setText(self.showBool(msg_dist['map']['from_local_status']))
                    self.label_msgsmap_3.setText(self.showBool(msg_dist['map']['net_coming_status']))
                    self.label_msgsmap_4.setText(self.showBool(msg_dist['map']['to_ans_exchange_status']))
                    self.label_msgsmap_5.setText(self.showBool(msg_dist['map']['to_ans_encode_status']))
                    self.label_msgsmap_6.setText(self.showBool(msg_dist['map']['to_rxtx_center_status']))
                except:
                    pass
                try:
                    self.label_msgsrsi.setText(self.showBool(msg_dist['rsi']['cfg_load_status']))
                    self.label_msgsrsi_2.setText(self.showBool(msg_dist['rsi']['from_local_status']))
                    self.label_msgsrsi_3.setText(self.showBool(msg_dist['rsi']['net_coming_status']))
                    self.label_msgsrsi_4.setText(self.showBool(msg_dist['rsi']['to_ans_exchange_status']))
                    self.label_msgsrsi_5.setText(self.showBool(msg_dist['rsi']['to_ans_encode_status']))
                    self.label_msgsrsi_6.setText(self.showBool(msg_dist['rsi']['to_rxtx_center_status']))
                except:
                    pass
                try:
                    self.label_msgsspat.setText(self.showBool(msg_dist['spat']['cfg_load_status']))
                    self.label_msgsspat_2.setText(self.showBool(msg_dist['spat']['from_local_status']))
                    self.label_msgsspat_3.setText(self.showBool(msg_dist['spat']['net_coming_status']))
                    self.label_msgsspat_4.setText(self.showBool(msg_dist['spat']['to_ans_exchange_status']))
                    self.label_msgsspat_5.setText(self.showBool(msg_dist['spat']['to_ans_encode_status']))
                    self.label_msgsspat_6.setText(self.showBool(msg_dist['spat']['to_rxtx_center_status']))
                except:
                    pass
                try:
                    self.label_msgsrsm.setText(self.showBool(msg_dist['rsm']['cfg_load_status']))
                    self.label_msgsrsm_2.setText(self.showBool(msg_dist['rsm']['from_local_status']))
                    self.label_msgsrsm_3.setText(self.showBool(msg_dist['rsm']['net_coming_status']))
                    self.label_msgsrsm_4.setText(self.showBool(msg_dist['rsm']['to_ans_exchange_status']))
                    self.label_msgsrsm_5.setText(self.showBool(msg_dist['rsm']['to_ans_encode_status']))
                    self.label_msgsrsm_6.setText(self.showBool(msg_dist['rsm']['to_rxtx_center_status']))
                except:
                    pass
                try:
                    self.label_msgsrtcm.setText(self.showBool(msg_dist['rtcm']['cfg_load_status']))
                    self.label_msgsrtcm_2.setText(self.showBool(msg_dist['rtcm']['from_local_status']))
                    self.label_msgsrtcm_3.setText(self.showBool(msg_dist['rtcm']['net_coming_status']))
                    self.label_msgsrtcm_4.setText(self.showBool(msg_dist['rtcm']['to_ans_exchange_status']))
                    self.label_msgsrtcm_5.setText(self.showBool(msg_dist['rtcm']['to_ans_encode_status']))
                    self.label_msgsrtcm_6.setText(self.showBool(msg_dist['rtcm']['to_rxtx_center_status']))
                except:
                    pass
    def startShowJsonLable_MsgConf(self):
        global parent_conn_MsgConf
        while True:
            msg = parent_conn_MsgConf.recv()
            msg_dist = msg['msgData']

            self.checkBox_bsmenable.setCheckState(msg_dist['bsmRx']['status'])
            self.lineEdit_bsmaid.setText(str(msg_dist['bsmRx']['aid']))
            self.lineEdit_bsmstartime.setText(str(msg_dist['bsmRx']['begin_time']))
            self.lineEdit_bsmendtime.setText(str(msg_dist['bsmRx']['end_time']))

            self.checkBox_mapenable.setCheckState(msg_dist['mapTx']['status'])
            self.lineEdit_mapaid.setText(str(msg_dist['mapTx']['aid']))
            self.lineEdit_mappriotity.setText(str(msg_dist['mapTx']['priotity']))
            self.lineEdit_mapmac.setText(str(msg_dist['mapTx']['mac_addr']))

            self.checkBox_mapenable.setCheckState(msg_dist['mapTx']['status'])
            self.lineEdit_mapaid.setText(str(msg_dist['mapTx']['aid']))
            self.lineEdit_mappriotity.setText(str(msg_dist['mapTx']['priotity']))
            self.lineEdit_mapmac.setText(str(msg_dist['mapTx']['mac_addr']))
            self.checkBox_mapsecurity.setCheckState(msg_dist['mapTx']['security_flg'])
            self.lineEdit_mapstartime.setText(str(msg_dist['mapTx']['begin_time']))
            self.lineEdit_mapendtime.setText(str(msg_dist['mapTx']['end_time']))
            self.comboBox_mapbroadcast.setCurrentIndex(msg_dist['mapTx']['broadcast_style'])
            self.lineEdit_mapinterval.setText(str(msg_dist['mapTx']['interval']))
            self.comboBox_mapsource.setCurrentIndex(msg_dist['mapTx']['source'])

            self.checkBox_spatenable.setCheckState(msg_dist['spatTx']['status'])
            self.lineEdit_spataid.setText(str(msg_dist['spatTx']['aid']))
            self.lineEdit_spatpriotity.setText(str(msg_dist['spatTx']['priotity']))
            self.lineEdit_spatmac.setText(str(msg_dist['spatTx']['mac_addr']))
            self.checkBox_spatsecurity.setCheckState(msg_dist['spatTx']['security_flg'])
            self.lineEdit_spatstartime.setText(str(msg_dist['spatTx']['begin_time']))
            self.lineEdit_spatendtime.setText(str(msg_dist['spatTx']['end_time']))
            self.comboBox_spatbroadcast.setCurrentIndex(msg_dist['spatTx']['broadcast_style'])
            self.lineEdit_spatinterval.setText(str(msg_dist['spatTx']['interval']))
            self.comboBox_spatsource.setCurrentIndex(msg_dist['spatTx']['source'])

            self.checkBox_rsienable.setCheckState(msg_dist['rsiTx']['status'])
            self.lineEdit_rsiaid.setText(str(msg_dist['rsiTx']['aid']))
            self.lineEdit_rsipriotity.setText(str(msg_dist['rsiTx']['priotity']))
            self.lineEdit_rsimac.setText(str(msg_dist['rsiTx']['mac_addr']))
            self.checkBox_rsisecurity.setCheckState(msg_dist['rsiTx']['security_flg'])
            self.lineEdit_rsistartime.setText(str(msg_dist['rsiTx']['begin_time']))
            self.lineEdit_rsiendtime.setText(str(msg_dist['rsiTx']['end_time']))
            self.comboBox_rsibroadcast.setCurrentIndex(msg_dist['rsiTx']['broadcast_style'])
            self.lineEdit_rsiinterval.setText(str(msg_dist['rsiTx']['interval']))
            self.comboBox_rsisource.setCurrentIndex(msg_dist['rsiTx']['source'])

            self.checkBox_rsmenable.setCheckState(msg_dist['rsmTx']['status'])
            self.lineEdit_rsmaid.setText(str(msg_dist['rsmTx']['aid']))
            self.lineEdit_rsmpriotity.setText(str(msg_dist['rsmTx']['priotity']))
            self.lineEdit_rsmmac.setText(str(msg_dist['rsmTx']['mac_addr']))
            self.checkBox_rsmsecurity.setCheckState(msg_dist['rsmTx']['security_flg'])
            self.lineEdit_rsmstartime.setText(str(msg_dist['rsmTx']['begin_time']))
            self.lineEdit_rsmendtime.setText(str(msg_dist['rsmTx']['end_time']))
            self.comboBox_rsmbroadcast.setCurrentIndex(msg_dist['rsmTx']['broadcast_style'])
            self.lineEdit_rsminterval.setText(str(msg_dist['rsmTx']['interval']))
            self.comboBox_rsmsource.setCurrentIndex(msg_dist['rsmTx']['source'])

            self.checkBox_rtcmenable.setCheckState(msg_dist['rtcmTx']['status'])
            self.lineEdit_rtcmaid.setText(str(msg_dist['rtcmTx']['aid']))
            self.lineEdit_rtcmpriotity.setText(str(msg_dist['rtcmTx']['priotity']))
            self.lineEdit_rtcmmac.setText(str(msg_dist['rtcmTx']['mac_addr']))
            self.checkBox_rtcmsecurity.setCheckState(msg_dist['rtcmTx']['security_flg'])
            self.lineEdit_rtcmstartime.setText(str(msg_dist['rtcmTx']['begin_time']))
            self.lineEdit_rtcmendtime.setText(str(msg_dist['rtcmTx']['end_time']))
            self.comboBox_rtcmbroadcast.setCurrentIndex(msg_dist['rtcmTx']['broadcast_style'])
            self.lineEdit_rtcminterval.setText(str(msg_dist['rtcmTx']['interval']))
            self.comboBox_rtcmsource.setCurrentIndex(msg_dist['rtcmTx']['source'])

    def push_disconnect(self):
        self.client.disconnect()
        self.pushBroker.setEnabled(True)
        self.pushBrokerDis.setEnabled(False)
        self.pushPublish.setEnabled(False)
        self.pushQuery.setEnabled(False)
        self.pushStartRecv.setEnabled(False)

    def is_number(self, s):
        try:
            return int(s)
        except:
            return 0

    def msgTxRxConf(self):
        msgTxRx_dict = {}
        item_dict = {"state": False, "aid": 0, "priotity": 0, "mac_addr": [0,0,0,0,0,0], "security_flg": 0,
                        "begin_time": 0, "end_time": 0, "broadcast_style" : 0, "interval" : 0, "source" : 0}

        #tab_i = self.tabWidget_msg.currentIndex()
        bsm_dist = item_dict.copy()
        bsm_dist['state'] = self.checkBox_bsmenable.isChecked()
        bsm_dist['aid'] = self.is_number(self.lineEdit_bsmaid.text())
        bsm_dist['begin_time'] = self.is_number(self.lineEdit_bsmstartime.text())
        bsm_dist['end_time'] = self.is_number(self.lineEdit_bsmendtime.text())
        msgTxRx_dict['bsmRx'] = bsm_dist

        map_dist = item_dict.copy()
        map_dist['state'] = self.checkBox_mapenable.isChecked()
        map_dist['aid'] = self.is_number(self.lineEdit_mapaid.text())
        map_dist['priotity'] = self.is_number(self.lineEdit_mappriotity.text())
        macstring = self.lineEdit_mapmac.text().split(":", 6)
        for i in range(len(macstring)):
            map_dist['mac_addr'][i] = self.is_number(macstring[i])
        map_dist['security_flg'] = self.checkBox_mapsecurity.isChecked()
        map_dist['begin_time'] = self.is_number(self.lineEdit_mapstartime.text())
        map_dist['end_time'] = self.is_number(self.lineEdit_mapendtime.text())
        map_dist['broadcast_style'] = self.comboBox_mapbroadcast.currentIndex()
        map_dist['interval'] = self.is_number(self.lineEdit_mapinterval.text())
        map_dist['source'] = self.comboBox_mapsource.currentIndex()
        msgTxRx_dict['mapTx'] = map_dist

        spat_dist = item_dict.copy()
        spat_dist['state'] = self.checkBox_spatenable.isChecked()
        spat_dist['aid'] = self.is_number(self.lineEdit_spataid.text())
        spat_dist['priotity'] = self.is_number(self.lineEdit_spatpriotity.text())
        macstring = self.lineEdit_spatmac.text().split(":", 6)
        for i in range(len(macstring)):
            spat_dist['mac_addr'][i] = self.is_number(macstring[i])
        spat_dist['security_flg'] = self.checkBox_spatsecurity.isChecked()
        spat_dist['begin_time'] = self.is_number(self.lineEdit_spatstartime.text())
        spat_dist['end_time'] = self.is_number(self.lineEdit_spatendtime.text())
        spat_dist['broadcast_style'] = self.comboBox_spatbroadcast.currentIndex()
        spat_dist['interval'] = self.is_number(self.lineEdit_spatinterval.text())
        spat_dist['source'] = self.comboBox_spatsource.currentIndex()
        msgTxRx_dict['spatTx'] = spat_dist

        rsi_dist = item_dict.copy()
        rsi_dist['state'] = self.checkBox_rsienable.isChecked()
        rsi_dist['aid'] = self.is_number(self.lineEdit_rsiaid.text())
        rsi_dist['priotity'] = self.is_number(self.lineEdit_rsipriotity.text())
        macstring = self.lineEdit_rsimac.text().split(":", 6)
        for i in range(len(macstring)):
            rsi_dist['mac_addr'][i] = self.is_number(macstring[i])
        rsi_dist['security_flg'] = self.checkBox_rsisecurity.isChecked()
        rsi_dist['begin_time'] = self.is_number(self.lineEdit_rsistartime.text())
        rsi_dist['end_time'] = self.is_number(self.lineEdit_rsiendtime.text())
        rsi_dist['broadcast_style'] = self.comboBox_rsibroadcast.currentIndex()
        rsi_dist['interval'] = self.is_number(self.lineEdit_rsiinterval.text())
        rsi_dist['source'] = self.comboBox_rsisource.currentIndex()
        msgTxRx_dict['rsiTx'] = rsi_dist

        rsm_dist = item_dict.copy()
        rsm_dist['state'] = self.checkBox_rsmenable.isChecked()
        rsm_dist['aid'] = self.is_number(self.lineEdit_rsmaid.text())
        rsm_dist['priotity'] = self.is_number(self.lineEdit_rsmpriotity.text())
        macstring = self.lineEdit_rsmmac.text().split(":", 6)
        for i in range(len(macstring)):
            rsm_dist['mac_addr'][i] = self.is_number(macstring[i])
        rsm_dist['security_flg'] = self.checkBox_rsmsecurity.isChecked()
        rsm_dist['begin_time'] = self.is_number(self.lineEdit_rsmstartime.text())
        rsm_dist['end_time'] = self.is_number(self.lineEdit_rsmendtime.text())
        rsm_dist['broadcast_style'] = self.comboBox_rsmbroadcast.currentIndex()
        rsm_dist['interval'] = self.is_number(self.lineEdit_rsminterval.text())
        rsm_dist['source'] = self.comboBox_rsmsource.currentIndex()
        msgTxRx_dict['rsmTx'] = rsm_dist

        rtcm_dist = item_dict.copy()
        rtcm_dist['state'] = self.checkBox_rtcmenable.isChecked()
        rtcm_dist['aid'] = self.is_number(self.lineEdit_rtcmaid.text())
        rtcm_dist['priotity'] = self.is_number(self.lineEdit_rtcmpriotity.text())
        macstring = self.lineEdit_rtcmmac.text().split(":", 6)
        for i in range(len(macstring)):
            rtcm_dist['mac_addr'][i] = self.is_number(macstring[i])
        rtcm_dist['security_flg'] = self.checkBox_rtcmsecurity.isChecked()
        rtcm_dist['begin_time'] = self.is_number(self.lineEdit_rtcmstartime.text())
        rtcm_dist['end_time'] = self.is_number(self.lineEdit_rtcmendtime.text())
        rtcm_dist['broadcast_style'] = self.comboBox_rtcmbroadcast.currentIndex()
        rtcm_dist['interval'] = self.is_number(self.lineEdit_rtcminterval.text())
        rtcm_dist['source'] = self.comboBox_rtcmsource.currentIndex()
        msgTxRx_dict['rtcmTx'] = rtcm_dist
        return msgTxRx_dict

    def push_publish(self):
        sendmsgjson = ""
        dict = {"timeStamp":"","deviceSN":"","seqNum":"","ack":True,"msgType":"","tag":0,"msgData":{}}
        dict_OperationSet = {"deviceId":"","heartbeatRate":0,"deviceRunningInfoRate":0,"appRunningInfoRate":0,
                             "logInfoRate":0,"logFTP":"","alarmInfoRate":0}
        dict_DeviceSet = {"deviceId": "", "deviceName": "", "regionCode": 0, "curCommType": "", "ip":"", "port":0,
                          "gatewayIP":"", "mask":"", "deviceGroupType":"", "deviceGroupCode":"", "montantId":"",
                          "locationDesc":"", "locationType":0, "owner":"", "transEncryption":""}
        dict_ServiceSet = {"deviceId": "",
                           "mapConfig":{"upLimit":0, "downLimit":0, "upFilters":[]},
                           "bsmConfig": {"sampleMode":"", "sampleRate":0, "upLimit":0, "downLimit":0, "upFilters":[]},
                           "rsiConfig": {"upLimit":0, "downLimit":0,"upFilters":[]},
                           "spatConfig": {"upLimit":0, "downLimit":0,"upFilters":[]},
                           "rsmConfig": {"upLimit":0, "downLimit":0,"upFilters":[]}}
        dict_Restart = {"deviceID": "", "restartTime": 0}
        dict_Update = {"deviceID": "", "oldVersion": "", "newVersion": "", "downloadAddr": "", "ftpAccount": "",
                       "ftpPWD": "", "time": ""}

        tabIndexSet = self.tabWidget_set.currentIndex()
        if tabIndexSet == 0:
            dict['msgType'] = 'DeviceSetRequest'
            dict['tag'] = codeType2Tag(dict['msgType'])
            dict_DeviceSet['deviceId'] = self.deviceId.text()
            dict_DeviceSet['deviceName'] = self.lineEdit_deviceName.text()
            dict_DeviceSet['regionCode'] = self.is_number(self.lineEdit_regionCode.text())
            dict_DeviceSet['curCommType'] = self.lineEdit_curCommType.text()
            dict_DeviceSet['ip'] = self.lineEdit_ip.text()
            dict_DeviceSet['port'] = self.is_number(self.lineEdit_port.text())
            dict_DeviceSet['gatewayIP'] = self.lineEdit_gatewayIP.text()
            dict_DeviceSet['mask'] = self.lineEdit_mask.text()
            dict_DeviceSet['deviceGroupType'] = self.lineEdit_deviceGroupType.text()
            dict_DeviceSet['deviceGroupCode'] = self.lineEdit_deviceGroupCode.text()
            dict_DeviceSet['montantId'] = self.lineEdit_montantId.text()
            dict_DeviceSet['locationDesc'] = self.lineEdit_locationDesc.text()
            dict_DeviceSet['locationType'] = self.is_number(self.lineEdit_locationType.text())
            dict_DeviceSet['owner'] = self.lineEdit_owner.text()
            dict_DeviceSet['transEncryption'] = self.lineEdit_transEncryption.text()
            dict['msgData'] = dict_DeviceSet
            sendmsgjson = json.dumps(dict)
            ptopic = self.lineEdit_ptopic.text()

        if tabIndexSet == 1:
            dict['msgType'] = 'OperationSetRequest'
            dict['tag'] = codeType2Tag(dict['msgType'])
            dict_OperationSet['heartbeatRate'] = self.is_number(self.lineEdit_heartbeatRate.text())
            dict_OperationSet['deviceRunningInfoRate'] = self.is_number(self.lineEdit_deviceRunningInfoRate.text())
            dict_OperationSet['appRunningInfoRate'] = self.is_number(self.lineEdit_appRunningInfoRate.text())
            dict_OperationSet['logInfoRate'] = self.is_number(self.lineEdit_logInfoRate.text())
            dict_OperationSet['alarmInfoRate'] = self.is_number(self.lineEdit_alarmInfoRate.text())
            dict_OperationSet['logFTP'] = self.lineEdit_logFTP.text()
            dict['msgData'] = dict_OperationSet
            sendmsgjson = json.dumps(dict)
            ptopic = self.lineEdit_ptopic.text()

        if tabIndexSet == 2:
            dict['msgType'] = 'ServiceSetRequest'
            dict['tag'] = codeType2Tag(dict['msgType'])

            dict_ServiceSet['mapConfig']['upLimit'] = self.is_number(self.lineEdit_upLimit.text())
            dict_ServiceSet['mapConfig']['downLimit'] = self.is_number(self.lineEdit_downLimit.text())
            dict_ServiceSet['mapConfig']['upFilters'].append\
                (json.loads(self.lineEdit_upFilterskey1.text().replace("\'", "\"")))
            dict_ServiceSet['mapConfig']['upFilters'].append\
                (json.loads(self.lineEdit_upFiltersval1.text().replace("\'", "\"")))
            dict_ServiceSet['mapConfig']['upFilters'].append\
                (json.loads(self.lineEdit_upFilterskey2.text().replace("\'", "\"")))
            dict_ServiceSet['mapConfig']['upFilters'].append\
                (json.loads(self.lineEdit_upFiltersval2.text().replace("\'", "\"")))

            dict_ServiceSet['bsmConfig']['sampleMode'] = self.lineEdit_sampleMode.text()
            dict_ServiceSet['bsmConfig']['sampleRate'] = self.is_number(self.lineEdit_sampleRate.text())
            dict_ServiceSet['bsmConfig']['upLimit'] = self.is_number(self.lineEdit_upLimit_2.text())
            dict_ServiceSet['bsmConfig']['downLimit'] = self.is_number(self.lineEdit_downLimit_2.text())
            dict_ServiceSet['bsmConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFilterskey3.text().replace("\'", "\"")))
            dict_ServiceSet['bsmConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFiltersval3.text().replace("\'", "\"")))
            dict_ServiceSet['bsmConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFilterskey4.text().replace("\'", "\"")))
            dict_ServiceSet['bsmConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFiltersval4.text().replace("\'", "\"")))

            dict_ServiceSet['rsiConfig']['upLimit'] = self.is_number(self.lineEdit_upLimit_3.text())
            dict_ServiceSet['rsiConfig']['downLimit'] = self.is_number(self.lineEdit_downLimit_3.text())
            dict_ServiceSet['rsiConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFilterskey5.text().replace("\'", "\"")))
            dict_ServiceSet['rsiConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFiltersval5.text().replace("\'", "\"")))
            dict_ServiceSet['rsiConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFilterskey6.text().replace("\'", "\"")))
            dict_ServiceSet['rsiConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFiltersval6.text().replace("\'", "\"")))

            dict_ServiceSet['spatConfig']['upLimit'] = self.is_number(self.lineEdit_upLimit_4.text())
            dict_ServiceSet['spatConfig']['downLimit'] = self.is_number(self.lineEdit_downLimit_4.text())
            dict_ServiceSet['spatConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFilterskey9.text().replace("\'", "\"")))
            dict_ServiceSet['spatConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFiltersval9.text().replace("\'", "\"")))
            dict_ServiceSet['spatConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFilterskey10.text().replace("\'", "\"")))
            dict_ServiceSet['spatConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFiltersval10.text().replace("\'", "\"")))

            dict_ServiceSet['rsmConfig']['upLimit'] = self.is_number(self.lineEdit_upLimit_5.text())
            dict_ServiceSet['rsmConfig']['downLimit'] = self.is_number(self.lineEdit_downLimit_5.text())
            dict_ServiceSet['rsmConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFilterskey7.text().replace("\'", "\"")))
            dict_ServiceSet['rsmConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFiltersval7.text().replace("\'", "\"")))
            dict_ServiceSet['rsmConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFilterskey8.text().replace("\'", "\"")))
            dict_ServiceSet['rsmConfig']['upFilters'].append \
                (json.loads(self.lineEdit_upFiltersval8.text().replace("\'", "\"")))

            dict['msgData'] = dict_ServiceSet
            sendmsgjson = json.dumps(dict)
            ptopic = self.lineEdit_ptopic.text()

        if tabIndexSet == 3:
            dict['msgType'] = 'RestartRequest'
            dict['tag'] = codeType2Tag(dict['msgType'])
            dict_Restart['restartTime'] = self.is_number(self.label_restartTime.text())
            dict['msgData'] = dict_Restart
            sendmsgjson = json.dumps(dict)
            ptopic = self.lineEdit_ptopic.text()

        if tabIndexSet == 4:
            dict['msgType'] = 'UpdateRequest'
            dict['tag'] = codeType2Tag(dict['msgType'])
            dict_Update['deviceID'] = self.lineEdit_deviceID2.text()
            dict_Update['oldVersion'] = self.lineEdit_oldVersion.text()
            dict_Update['newVersion'] = self.lineEdit_newVersion.text()
            dict_Update['downloadAddr'] = self.lineEdit_downloadAddr.text()
            dict_Update['ftpAccount'] = self.lineEdit_ftpAccount.text()
            dict_Update['ftpPWD'] = self.lineEdit_ftpPWD.text()
            dict_Update['time'] = self.lineEdit_time.text()
            dict['msgData'] = dict_Update
            sendmsgjson = json.dumps(dict)
            ptopic = self.lineEdit_ptopic.text()

        if tabIndexSet == 5:
            self.treeView_Map_tx.setModel(self.model_Map)
            try:
                fp = open("./map.json", "rb")
                fileData = fp.read()
                self.model_Map.loadJson(fileData)
            except:
                return
            sendmsgjson = bytes.decode(fileData)
            ptopic = self.lineEdit_ptopic_2.text() + "map"

        if tabIndexSet == 6:
            self.treeView_Rsi_tx.setModel(self.model_Rsi)
            try:
                fp = open("./rsi.json", "rb")
                fileData = fp.read()
                self.model_Rsi.loadJson(fileData)
            except:
                return
            sendmsgjson = bytes.decode(fileData)
            ptopic = self.lineEdit_ptopic_2.text() + "rsi"

        if tabIndexSet == 7:
            self.treeView_Rsm_tx.setModel(self.model_Rsm)
            try:
                fp = open("./rsm.json", "rb")
                fileData = fp.read()
                self.model_Rsm.loadJson(fileData)
            except:
                return
            sendmsgjson = bytes.decode(fileData)
            ptopic = self.lineEdit_ptopic_2.text() + "rsm"

        if tabIndexSet == 8:
            return

        if tabIndexSet == 9:
            return

        if tabIndexSet == 10:
            dict['msgType'] = 'MsgRxTxConfRequest'
            dict['msgData'] = self.msgTxRxConf()
            sendmsgjson = json.dumps(dict)
            ptopic = self.lineEdit_ptopic.text()
            #ptopic = self.lineEdit_ptopic_2.text() + "msgTxRxConf"

        if tabIndexSet > 10:
            return
        #print(sendmsgjson)
        self.client.on_publish(ptopic, sendmsgjson, 1)

    def publish(self, msgType):
        self.seqNum += 1
        curtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        dict = {'timeStamp': curtime, 'deviceSN': '', 'seqNum': str(self.seqNum), 'ack': True, 'msgType': '', 'tag': 0,
                'msgData': {'deviceId': '', 'deviceName': ''}}
        dict['msgType'] = msgType
        dict['tag'] = codeType2Tag(dict['msgType'])
        sendmsgjson = json.dumps(dict)
        ptopic = self.lineEdit_ptopic.text()
        self.client.on_publish(ptopic, sendmsgjson, 1)

    def push_query(self):
        tab_index_show = self.tabWidget_show.currentIndex()
        tab_index_set = self.tabWidget_set.currentIndex()
        if tab_index_show == 2 or tab_index_set == 0:
            self.publish('DeviceBaseInfoQuery')
        if tab_index_show == 3:
            self.publish('DeviceStateQuery')
        if tab_index_show == 4:
            self.publish('ServiceStateQuery')
        if tab_index_set == 1:
            self.publish('OpertionConfQuery')
        if tab_index_set == 2:
            self.publish('ServiceConfQuery')
        if tab_index_set == 10:
            self.publish('MsgRxTxConfQuery')
        if tab_index_set == 11:
            self.publish('MsgStatusQuery')

    def push_startrecv(self):
        global autorecvflag
        if autorecvflag == 0:
            autorecvflag = 1
            self.pushStartRecv.setText("停止接收")
        else:
            autorecvflag = 0
            self.pushStartRecv.setText("开始接收")

def codeType2Tag(type):
    enumtypedict = {'AlarmReport':10006,'DeviceRegisterRequest':10007,'DeviceHeartBeat':10008,
                    'DeviceSetRequest':20003,'OperationSetRequest':20004,'ServiceSetRequest':20005,
                    'RestartRequest':20006,'UpdateRequest':20007,'EventNotifyReport':20008,
                    'DeviceBaseInfoQuery':30001,'OpertionConfQuery':30002,'ServiceConfQuery':30003,
                    'DeviceStateQuery':30004,'ServiceStateQuery':30005,'DeviceBaseInfoResponse':10001,
                    'OperationConfResponse':10002,'ServiceConfResponse':10003,'DeviceRegisterResponse':10007,
                    'DeviceSetResponse':20003,'OperationSetResponse':20004,'ServiceSetResponse':20005,
                    'RestartResponse':20006,'UpdateResponse':20007,'DeviceBaseInfoQueryResponse':30001,
                    'OperationConfQueryResponse':30002,'ServiceConfQueryResponse':30003,
                    'DeviceStateQueryResponse':30004,'ServiceStateQueryResponse':30005,
                    'MsgStatusResponse':10011,'MsgStatusQuery':30011,
                    'MsgRxTxConfResponse':10012,'MsgRxTxConfRequest':20012,'MsgRxTxConfQuery':30012}
    for item in enumtypedict.items():
        if type == item[0]:
            return item[1]

def codeTag2Type(tag):
    enumtagdict = {'10001':'DeviceBaseInfo','10002':'OpertionConf','10003':'ServiceConf',
                   '10004':'DeviceStateReport','10005':'ServiceStateReport','10006':'AlarmReport',
                   '10007':'DeviceRegister','10008':'DeviceHeartBeat','10011':'MsgStatus',
                   '10012':'MsgRxTxConfResponse',
                   '20003':'DeviceSet','20004':'OperationSet','20005':'ServiceSet',
                   '20006':'Restart','20007':'Update','20008':'EventNotifyReport','20011':'MsgRxTxConf',
                   '30001':'DeviceBaseInfo','30002':'OpertionConf','30003':'ServiceConf',
                   '30004':'DeviceState','30005':'ServiceState','30011':'MsgStatus',
                   '30012':'MsgRxTxConf'}
    for item in enumtagdict.items():
        if tag == item[0]:
            return item[1]

if __name__ == '__main__':
    global child_conn_Register, parent_conn_Register
    global child_conn_BaseInfo, parent_conn_BaseInfo
    global child_conn_OpertionConf, parent_conn_OpertionConf
    global child_conn_DeviceState, parent_conn_DeviceState
    global child_conn_ServiceState, parent_conn_ServiceState
    global child_conn_ServiceConf, parent_conn_ServiceConf
    global child_conn_Alarm, parent_conn_Alarm
    global child_conn_HeartBeat, parent_conn_HeartBeat
    global child_conn_Bsm, parent_conn_Bsm
    global child_conn_Spat, parent_conn_Spat
    global child_conn_MsgStatus, parent_conn_MsgStatus
    global child_conn_MsgConf, parent_conn_MsgMsgConf

    parent_conn_Register, child_conn_Register = Pipe()
    parent_conn_BaseInfo, child_conn_BaseInfo = Pipe()
    parent_conn_OpertionConf, child_conn_OpertionConf = Pipe()
    parent_conn_DeviceState, child_conn_DeviceState = Pipe()
    parent_conn_ServiceState, child_conn_ServiceState = Pipe()
    parent_conn_ServiceConf, child_conn_ServiceConf = Pipe()
    parent_conn_Alarm, child_conn_Alarm = Pipe()
    parent_conn_HeartBeat, child_conn_HeartBeat = Pipe()
    parent_conn_Bsm, child_conn_Bsm = Pipe()
    parent_conn_Spat, child_conn_Spat = Pipe()
    parent_conn_MsgStatus, child_conn_MsgStatus = Pipe()
    parent_conn_MsgConf, child_conn_MsgConf = Pipe()

    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())

