# -*- coding: utf-8 -*-

import os
import sys
import threading
import time
import paramiko
import hashlib
import shutil
import win32api,win32con
import zipfile

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QEventLoop, QTimer, QStringListModel
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from ssh_form import Ui_Form

class itemfileinfo:
    def __init__(self, orgpath, tarpath, filename, md5sum):
        self.orgpath = orgpath
        self.tarpath = tarpath
        self.filename = filename
        self.md5sum = md5sum

    def __repr__(self):
        return "%s    %s    %s    %s" % (self.orgpath, self.tarpath, self.filename, self.md5sum)

class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):
    showlist = []
    fileinfo = itemfileinfo('','','','')

    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)

        self.listmodel = QStringListModel(self)
        self.listmodel.setStringList(self.showlist)
        self.listView.setModel(self.listmodel)
        self.listmodel.dataChanged.connect(self.lvsave)
        self.rootpath = os.getcwd()

    def lvsave(self):
        self.showlist = self.listmodel.stringList()

    def zipDir(self):
        z = zipfile.ZipFile(self.FinishPath, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
        for dirpath, dirnames, filenames in os.walk(self.Targetdir_path):
            fpath = dirpath.replace(self.Targetdir_path, self.TarDirName)  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for fname in filenames:
                z.write(os.path.join(dirpath, fname), fpath + fname)
                self.pnum += 50 / (self.num + 1)
                self.progressBar.setValue(int(self.pnum))
        z.close()

    def openfile(self):
        if os.path.dirname(self.fileinfo.orgpath) == '':
            ofdefaultpath = self.rootpath
        else:
            ofdefaultpath = os.path.dirname(self.fileinfo.orgpath)

        filepath, filetype = QFileDialog.getOpenFileName(self, '选择文件', ofdefaultpath, '*')
        filepath = filepath.replace("/", "\\")
        return filepath

    def push_del(self):
        index = self.listView.currentIndex()
        self.listmodel.removeRow(index.row())

    def push_add(self):
        while True:
            self.fileinfo.orgpath = self.openfile()
            if self.fileinfo.orgpath == '':
                return
            self.fileinfo.tarpath = self.lineEdit.text()
            if self.fileinfo.tarpath == '':
                self.fileinfo.tarpath = "/home/root"
            self.fileinfo.filename = os.path.basename(self.fileinfo.orgpath)

            fp = open(self.fileinfo.orgpath, 'rb')
            contents = fp.read()
            fp.close()
            md5val = hashlib.md5(contents).hexdigest()
            self.fileinfo.md5sum = md5val

            row = self.listmodel.rowCount()
            self.listmodel.insertRow(row)
            self.listmodel.setData(self.listmodel.index(row), str(self.fileinfo))

    def createconfile(self):
        cfgpath = self.Targetdir_path + "\\upgrade.cfg"
        self.num = self.listmodel.rowCount()
        fo = open(cfgpath, "w")
        strvalue = 'info :\n{\n  num = ' + str(self.num) + ';\n  version = \"' + self.targetversion + '\";\n};\n'

        for i in range(self.num):
            strvalue += 'file' + str(i) + ' :\n{\n  name = \"' + self.showlist[i].split('    ')[2] + '\";\n' \
            + '  md5sum = \"' + self.showlist[i].split('    ')[3] + '\";\n' \
            + '  path = \"' + self.showlist[i].split('    ')[1] + '\";\n};\n'

        fo.write(strvalue)
        fo.close()

    def push_creat(self):
        self.pnum = 0
        self.targetversion = self.lineEdit_tarver.text()
        if len(self.targetversion) == 0:
            win32api.MessageBox(0, "请填写目标版本号", "提醒",win32con.MB_OK)
            return

        self.externversion = self.lineEdit_exver.text()
        if len(self.externversion) == 0:
            win32api.MessageBox(0, "请填写补丁版本号", "提醒", win32con.MB_OK)
            return

        self.TarDirName = self.targetversion + "_sp" + self.externversion
        self.Targetdir_path = self.rootpath + '\\' + self.TarDirName + '\\' + self.TarDirName
        if os.path.exists(self.Targetdir_path):
            shutil.rmtree(self.Targetdir_path)
        #os.mkdir(self.Targetdir_path)
        os.makedirs(self.Targetdir_path)

        self.FinishPath = self.TarDirName + ".img"

        for val in self.showlist:
            self.srcpath = val.split('    ')[0]
            self.tarpath = self.Targetdir_path + "\\" + val.split('    ')[2]
            shutil.copyfile(self.srcpath, self.tarpath)
            if len(self.showlist) == 0:
                self.pnum = 1
            else:
                self.pnum += 50 / len(self.showlist)
            self.progressBar.setValue(int(self.pnum))

        self.createconfile()
        self.zipDir()
        self.progressBar.setValue(100)
        win32api.MessageBox(0, "升级包制作完成", "提醒", win32con.MB_OK)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
