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
            child_conn_Bsm
        global autorecvflag
        mode = 0

        msgTopic = msg.topic
        msgData = msg.payload
        msg_data = bytes.decode(msgData)
        tindex = msg_data.rfind('}')
        msg_json = msg_data[:tindex + 1]
        jsonstring = msg_json.encode()

        if msgTopic.rfind('bsm') >= 0 and autorecvflag == 1:
            child_conn_Bsm.send(jsonstring)
        elif msgTopic.rfind('spat') >= 0 and autorecvflag == 1:
            child_conn_Spat.send(jsonstring)
        else:
            try:
                dict_json = json.loads(msg_json)
                dict_tag = dict_json['tag']
                try:
                    dict_key = dict_json['msgType']
                    mode = 1
                except:
                    dict_key = codeTag2Type(str(dict_tag))
                    mode = 0

                if dict_key == "DeviceRegisterReport":
                    child_conn_Register.send(jsonstring)
                if dict_key == "AlarmReport":
                    child_conn_Alarm.send(jsonstring)
                if dict_key == "DeviceHeartBeat":
                    child_conn_HeartBeat.send(jsonstring)
                if (autorecvflag == 1 and dict_key.rfind('Report') >= 0) or \
                        (autorecvflag == 0 and (mode == 0 or dict_key.rfind('Response') >= 0)):
                    if dict_key.find('DeviceBaseInfo') >= 0:
                        child_conn_BaseInfo.send(jsonstring)
                    if dict_key.find('OpertionConf') >= 0:
                        child_conn_OpertionConf.send(jsonstring)
                    if dict_key.find('ServiceConf') >= 0:
                        child_conn_ServiceConf.send(jsonstring)
                    if dict_key.find('DeviceState') >= 0:
                        child_conn_DeviceState.send(jsonstring)
                    if dict_key.find('ServiceState') >= 0:
                        child_conn_ServiceState.send(jsonstring)
            except:
                pass

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

        self.treeView_Register.setStyleSheet("background:#ffffff")
        self.treeView_BaseInfo.setStyleSheet("background:#ffffff")
        self.treeView_OpertionConf.setStyleSheet("background:#ffffff")
        self.treeView_DeviceState.setStyleSheet("background:#ffffff")
        self.treeView_ServiceState.setStyleSheet("background:#ffffff")
        self.treeView_ServiceConf.setStyleSheet("background:#ffffff")
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

        self.client = MQTTClient(brokerip, 1883)
        self.client.connect(user, pswd)
        self.client.on_subscribe(stopic)
        self.client.on_subscribe(stopic2)
        self.client.on_loopstart()

        self.pushBroker.setEnabled(False)
        self.pushBrokerDis.setEnabled(True)

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
            cnt += 1
            endtime = datetime.datetime.now()
            duringtime = endtime - starttime
            self.model_BaseInfo.loadJson(msg)
            self.label_DeviceBaseInfo.setText(str(cnt))
            self.label_DeviceBaseInfo_2.setText(str(duringtime.seconds))

    def startShowJsontreeView_OpertionConf(self):
        global parent_conn_OpertionConf
        cnt = 0
        while True:
            self.treeView_OpertionConf.setModel(self.model_OpertionConf)
            starttime = datetime.datetime.now()
            msg = parent_conn_OpertionConf.recv()
            cnt += 1
            endtime = datetime.datetime.now()
            duringtime = endtime - starttime
            self.model_OpertionConf.loadJson(msg)
            self.label_OpertionConf.setText(str(cnt))
            self.label_OpertionConf_2.setText(str(duringtime.seconds))

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
            self.treeView_ServiceConf.setModel(self.model_ServiceConf)
            starttime = datetime.datetime.now()
            msg = parent_conn_ServiceConf.recv()
            cnt += 1
            endtime = datetime.datetime.now()
            duringtime = endtime - starttime
            self.model_ServiceConf.loadJson(msg)
            self.label_ServiceConf.setText(str(cnt))
            self.label_ServiceConf_2.setText(str(duringtime.seconds))

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
            #self.label_HeartBeat.setText(str(cnt))
            #self.label_HeartBeat_2.setText(str(duringtime.seconds))

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
            #self.label_HeartBeat.setText(str(cnt))
            #self.label_HeartBeat_2.setText(str(duringtime.seconds))

    def push_disconnect(self):
        self.client.disconnect()
        self.pushBroker.setEnabled(True)
        self.pushBrokerDis.setEnabled(False)

    def is_number(self, s):
        try:
            return int(s)
        except:
            return 0

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
                           "bsmConfig": {"sampleMode":"", "sampleRate":"", "upLimit":0, "downLimit":0,"upFilters":[]},
                           "rsiConfig": {"upLimit":0, "downLimit":0,"upFilters":[]},
                           "spatConfig": {"upLimit":0, "downLimit":0,"upFilters":[]},
                           "rsmConfig": {"upLimit":0, "downLimit":0,"upFilters":[]}}
        dict_Restart = {"deviceID": "", "restartTime": 0}
        dict_Update = {"deviceID": "", "oldVersion": "", "newVersion": "", "downloadAddr": "", "ftpAccount": "",
                       "ftpPWD": "", "time": ""}

        tab_index = self.tabWidget_set.currentIndex()
        if tab_index == 0:
            dict['msgType'] = 'DeviceSetRequest'
            dict['tag'] = codeType2Tag(dict['msgType'])
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

        if tab_index == 1:
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

        if tab_index == 2:
            dict['msgType'] = 'ServiceSetRequest'
            dict['tag'] = codeType2Tag(dict['msgType'])

            dict_ServiceSet['mapConfig']['upLimit'] = self.is_number(self.lineEdit_upLimit.text())
            dict_ServiceSet['mapConfig']['downLimit'] = self.is_number(self.lineEdit_downLimit.text())
            dict_ServiceSet['mapConfig']['upFilters'].append({self.lineEdit_upFilterskey1.text(): self.lineEdit_upFiltersval1.text()})
            dict_ServiceSet['mapConfig']['upFilters'].append({self.lineEdit_upFilterskey2.text(): self.lineEdit_upFiltersval2.text()})

            dict_ServiceSet['bsmConfig']['sampleMode'] = self.lineEdit_sampleMode.text()
            dict_ServiceSet['bsmConfig']['sampleRate'] = self.is_number(self.lineEdit_sampleRate.text())
            dict_ServiceSet['bsmConfig']['upLimit'] = self.is_number(self.lineEdit_upLimit_2.text())
            dict_ServiceSet['bsmConfig']['downLimit'] = self.is_number(self.lineEdit_downLimit_2.text())
            dict_ServiceSet['bsmConfig']['upFilters'].append({self.lineEdit_upFilterskey3.text(), self.lineEdit_upFiltersval3.text()})
            dict_ServiceSet['bsmConfig']['upFilters'].append({self.lineEdit_upFilterskey4.text(), self.lineEdit_upFiltersval4.text()})

            dict_ServiceSet['rsiConfig']['upLimit'] = self.is_number(self.lineEdit_upLimit_3.text())
            dict_ServiceSet['rsiConfig']['downLimit'] = self.is_number(self.lineEdit_downLimit_3.text())
            dict_ServiceSet['rsiConfig']['upFilters'].append({self.lineEdit_upFilterskey5.text(), self.lineEdit_upFiltersval5.text()})
            dict_ServiceSet['rsiConfig']['upFilters'].append({self.lineEdit_upFilterskey6.text(), self.lineEdit_upFiltersval6.text()})

            dict_ServiceSet['spatConfig']['upLimit'] = self.is_number(self.lineEdit_upLimit_4.text())
            dict_ServiceSet['spatConfig']['downLimit'] = self.is_number(self.lineEdit_downLimit_4.text())
            dict_ServiceSet['spatConfig']['upFilters'].append({self.lineEdit_upFilterskey7.text(), self.lineEdit_upFiltersval7.text()})
            dict_ServiceSet['spatConfig']['upFilters'].append({self.lineEdit_upFilterskey8.text(), self.lineEdit_upFiltersval8.text()})

            dict_ServiceSet['rsmConfig']['upLimit'] = self.is_number(self.lineEdit_upLimit_5.text())
            dict_ServiceSet['rsmConfig']['downLimit'] = self.is_number(self.lineEdit_downLimit_5.text())
            dict_ServiceSet['rsmConfig']['upFilters'].append({self.lineEdit_upFilterskey9.text(), self.lineEdit_upFiltersval9.text()})
            dict_ServiceSet['rsmConfig']['upFilters'].append({self.lineEdit_upFilterskey10.text(), self.lineEdit_upFiltersval10.text()})

            dict['msgData'] = dict_ServiceSet
            sendmsgjson = json.dumps(dict)
            ptopic = self.lineEdit_ptopic.text()

        if tab_index == 3:
            dict['msgType'] = ' RestartRequest'
            dict['tag'] = codeType2Tag(dict['msgType'])
            dict_Restart['restartTime'] = self.is_number(self.label_restartTime.text())
            dict['msgData'] = dict_Restart
            sendmsgjson = json.dumps(dict)
            ptopic = self.lineEdit_ptopic.text()

        if tab_index == 4:
            dict['msgType'] = ' UpdateRequest'
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

        if tab_index == 5:
            self.treeView_Map_tx.setModel(self.model_Map)
            try:
                fp = open("./map.json", "rb")
                fileData = fp.read()
                self.model_Map.loadJson(fileData)
            except:
                return
            sendmsgjson = bytes.decode(fileData)
            ptopic = self.lineEdit_ptopic_2.text() + "map"

        if tab_index == 6:
            self.treeView_Rsi_tx.setModel(self.model_Rsi)
            try:
                fp = open("./rsi.json", "rb")
                fileData = fp.read()
                self.model_Rsi.loadJson(fileData)
            except:
                return
            sendmsgjson = bytes.decode(fileData)
            ptopic = self.lineEdit_ptopic_2.text() + "rsi"

        if tab_index == 7:
            self.treeView_Rsm_tx.setModel(self.model_Rsm)
            try:
                fp = open("./rsm.json", "rb")
                fileData = fp.read()
                self.model_Rsm.loadJson(fileData)
            except:
                return
            sendmsgjson = bytes.decode(fileData)
            ptopic = self.lineEdit_ptopic_2.text() + "rsm"


        print(sendmsgjson)
        self.client.on_publish(ptopic, sendmsgjson, 1)

    def push_query(self):
        self.seqNum += 1
        curtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        dict = {'timeStamp':curtime, 'deviceSN':'', 'seqNum':str(self.seqNum), 'ack':True, 'msgType':'', 'tag':0,
               'msgData':{'deviceId':'', 'deviceName':''}}

        tab_index = self.tabWidget_show.currentIndex()
        if tab_index == 2:
            dict['msgType'] = 'DeviceBaseInfoQuery'
            dict['tag'] = codeType2Tag(dict['msgType'])

        if tab_index == 3:
            dict['msgType'] = 'OpertionConfQuery'
            dict['tag'] = codeType2Tag(dict['msgType'])

        if tab_index == 4:
            dict['msgType'] = 'DeviceStateQuery'
            dict['tag'] = codeType2Tag(dict['msgType'])

        if tab_index == 5:
            dict['msgType'] = 'ServiceStateQuery'
            dict['tag'] = codeType2Tag(dict['msgType'])

        if tab_index == 6:
            dict['msgType'] = 'ServiceConfQuery'
            dict['tag'] = codeType2Tag(dict['msgType'])

        sendmsgjson = json.dumps(dict)
        ptopic = self.lineEdit_ptopic.text()
        self.client.on_publish(ptopic, sendmsgjson, 1)

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
                    'DeviceStateQueryResponse':30004,'ServiceStateQueryResponse':30005}
    for item in enumtypedict.items():
        if type == item[0]:
            return item[1]

def codeTag2Type(tag):
    enumtagdict = {'10001':'DeviceBaseInfo','10002':'OpertionConf','10003':'ServiceConf',
                   '10004':'DeviceStateReport','10005':'ServiceStateReport','10006':'AlarmReport',
                   '10007':'DeviceRegister','10008':'DeviceHeartBeat','20003':'DeviceSet',
                   '20004':'OperationSet','20005':'ServiceSet','20006':'Restart','20007':'Update',
                   '20008':'EventNotifyReport','30001':'DeviceBaseInfo','30002':'OpertionConf',
                   '30003':'ServiceConf','30004':'DeviceState','30005':'ServiceState'}
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

    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())

