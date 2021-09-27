# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ssh_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(758, 391)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMouseTracking(False)
        Form.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_add = QtWidgets.QPushButton(Form)
        self.pushButton_add.setGeometry(QtCore.QRect(40, 120, 101, 23))
        self.pushButton_add.setObjectName("pushButton_add")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(20, 80, 271, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 30, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 281, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.listView = QtWidgets.QListView(Form)
        self.listView.setGeometry(QtCore.QRect(330, 10, 421, 371))
        self.listView.setObjectName("listView")
        self.pushButton_del = QtWidgets.QPushButton(Form)
        self.pushButton_del.setGeometry(QtCore.QRect(170, 120, 101, 23))
        self.pushButton_del.setObjectName("pushButton_del")
        self.pushButton_create = QtWidgets.QPushButton(Form)
        self.pushButton_create.setGeometry(QtCore.QRect(110, 300, 101, 23))
        self.pushButton_create.setObjectName("pushButton_create")
        self.lineEdit_tarver = QtWidgets.QLineEdit(Form)
        self.lineEdit_tarver.setGeometry(QtCore.QRect(130, 190, 121, 21))
        self.lineEdit_tarver.setObjectName("lineEdit_tarver")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(20, 190, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 240, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lineEdit_exver = QtWidgets.QLineEdit(Form)
        self.lineEdit_exver.setGeometry(QtCore.QRect(130, 240, 121, 21))
        self.lineEdit_exver.setObjectName("lineEdit_exver")
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(20, 353, 301, 20))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(Form)
        self.pushButton_add.clicked.connect(Form.push_add)
        self.pushButton_del.clicked.connect(Form.push_del)
        self.pushButton_create.clicked.connect(Form.push_creat)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "升级包制作软件 v1.0"))
        self.pushButton_add.setText(_translate("Form", "添加文件"))
        self.label.setText(_translate("Form", "文件上传路径"))
        self.label_2.setText(_translate("Form", "例：/opt/platform/bin (注:结尾不加/)"))
        self.pushButton_del.setText(_translate("Form", "删除文件"))
        self.pushButton_create.setText(_translate("Form", "制作升级包"))
        self.label_3.setText(_translate("Form", "目标版本号"))
        self.label_4.setText(_translate("Form", "扩展版本号"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
